from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "lecturer"),
        (2, "student"),
    )

    name = models.CharField(max_length=30)
    type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    school = models.ForeignKey("School", on_delete=models.PROTECT)

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name":self.name,
            "type": self.type,
            "schoolID": self.school.id,
            "schoolName": self.school.name,
        }


class Lecturer(models.Model):
    user = models.OneToOneField("User", related_name="lecturerProfile", on_delete=models.CASCADE)

    def toJSON(self):
        return {
            **self.user.toJSON(),
            "managingCourses": [c.toJSON() for c in self.managingCourses.all()],
        }


class Student(models.Model):
    user = models.OneToOneField("User", related_name="studentProfile", on_delete=models.CASCADE)
    subscribingCourses = models.ManyToManyField("Course", related_name="students")
    assignmentDueAlarm = models.IntegerField(default=15)
    personalScheduleAlarm = models.IntegerField(default=15)
    timeForAssignmentAlarm = models.IntegerField(default=15)

    def toJSON(self):
        return {
            **self.user.toJSON(),
            "subscribingCourses": [c.toJSON() for c in self.subscribingCourses.all()],
        }


class School(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class Course(models.Model):
    lecturer = models.ForeignKey("Lecturer", related_name="managingCourses", on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey("School", on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    professor = models.CharField(max_length = 30)

    def toJSON(self):
        return {
            "id": self.id,
            "lecturerID": self.lecturer.id if (self.lecturer is not None) else None,
            "studentIDs": [s.id for s in self.students.all()],
            "schoolID": self.school.id,
            "assignmentIDs": [a.id for a in self.assignments.all()],
            "name": self.name,
            "code": self.code,
            "professor": self.professor,
        }


class Assignment(models.Model):
    course = models.ForeignKey("Course", related_name="assignments", on_delete=models.CASCADE)
    name = models.CharField(max_length = 30)
    due = models.DateTimeField()
    averageTimeEstimation = models.FloatField(null=True)
    description = models.CharField(max_length = 200)

    def toJSON(self):
        return {
            "id": self.id,
            "courseID": self.course.id,
            "courseName": self.course.name,
            "name": self.name,
            "due": self.due,
            "averageTimeEstimation": self.averageTimeEstimation,
            "description": self.description,
        }

    def updateAverageTimeEstimation(self):
        studentAssignments = StudentAssignment.objects.filter(assignment=self)
        num = 0
        sum = 0
        for a in studentAssignments:
            if a.timeEstimation != None and a.timeEstimation > 0:
                num += 1
                sum += a.timeEstimation
        self.averageTimeEstimation = sum/num if num>0 else None
        self.save()


class StudentAssignment(models.Model):
    student = models.ForeignKey("Student", related_name="studentAssignments", on_delete=models.CASCADE)
    assignment = models.ForeignKey("Assignment", related_name="studentAssignments", on_delete=models.CASCADE)
    timeEstimation = models.IntegerField(null=True)
    significance = models.IntegerField(null=True)
    alarms = models.ManyToManyField("ScheduleAlarm")

    class Meta:
        unique_together = (("student", "assignment"))

    def toJSON(self):
        return {
            **self.assignment.toJSON(),
            "timeEstimation": self.timeEstimation,
            "significance": self.significance,
            "timeForAssignments": [t.toJSON() for t in self.timeForAssignments.all()],
            "timeForAssignmentsSum": sum((t.end-t.start).total_seconds()/3600 for t in self.timeForAssignments.all()),
            "alarms": [a.minutes for a in self.alarms.all()],
        }


class Schedule(models.Model):
    student = models.ForeignKey(Student, related_name="%(class)ss", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    alarms = models.ManyToManyField("ScheduleAlarm")

    class Meta:
        abstract = True

    def toJSON(self):
        return {
            "id": self.id,
            "studentID": self.student.id,
            "start": self.start,
            "end": self.end,
            "alarms": [a.minutes for a in self.alarms.all()],
        }


class PersonalSchedule(Schedule):
    name = models.CharField(max_length = 30)

    def toJSON(self):
        return {
            **super().toJSON(),
            "id": self.id,
            "name": self.name,
        }


class TimeForAssignment(Schedule):
    studentAssignment = models.ForeignKey(StudentAssignment, related_name="timeForAssignments", on_delete=models.CASCADE)

    def toJSON(self):
        return {
            **super().toJSON(),
            "id": self.id,
            "assignmentID": self.studentAssignment.assignment.id,
            "assignmentName": self.studentAssignment.assignment.name,
            "courseID": self.studentAssignment.assignment.course.id,
            "courseName": self.studentAssignment.assignment.course.name,
        }


class ScheduleAlarm(models.Model):
    minutes = models.IntegerField()
