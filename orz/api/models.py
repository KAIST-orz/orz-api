from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    school = models.ForeignKey("School", on_delete=models.PROTECT)

    def toJSON(self):
        return {
            "id": self.id,
            "school": self.school.toJSON(),
        }


class Lecturer(models.Model):
    user = models.OneToOneField("User", related_name="lecturerProfile", on_delete=models.CASCADE)

    def toJSON(self):
        return {
            **self.user.toJSON(),
            managingCourses: [c.toJSON for c in self.managingCourses.all()],
        }


class Student(models.Model):
    user = models.OneToOneField("User", related_name="studentProfile", on_delete=models.CASCADE)
    subscribingCourses = models.ManyToManyField("Assignment", related_name="students", through="StudentAssignment")

    def toJSON(self):
        return {
            **self.user.toJSON(),
            managingCourses: [c.toJSON for c in self.subscribingCourses.all()],
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
            "lecturer": self.lecturer.toJSON(),
            "students": [s.toJSON() for s in self.students.all()],
            "school": self.school.toJSON(),
            "assignments": [a.toJSON() for a in self.assignments.all()],
            "name": self.name,
            "code": self.code,
            "professor": self.professor,
        }


class Assignment(models.Model):
    course = models.ForeignKey("Assignment", related_name="assignments", on_delete=models.CASCADE)
    name = models.CharField(max_length = 30)
    due = models.DateTimeField()
    averageTimeEstimation = models.FloatField()
    description = models.CharField(max_length = 200)

    def toJSON(self):
        return {
            "id": self.id,
            "course": self.course.toJSON(),
            "name": self.name,
            "due": self.due,
            "averageTimeEstimation": self.averageTimeEstimation,
            "description": self.description,
        }


class StudentAssignment(models.Model):
    student = models.ForeignKey("Student", related_name="studentAssignments", on_delete=models.CASCADE)
    assignment = models.ForeignKey("Assignment", related_name="studentAssignments", on_delete=models.CASCADE)
    timeEstimation = models.IntegerField()

    def toJSON(self):
        return {
            **self.assignment.toJSON(),
            "id": self.id,
            "timeEstimation": self.timeEstimation,
            "timeForAssignments": self.timeForAssignments,
        }


class Schedule(models.Model):
    student = models.ForeignKey(Student, related_name="%(class)ss", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        abstract = True

    def toJSON(self):
        return {
            "id": self.id,
            "student": self.student.toJSON(),
            "start": self.start,
            "end": self.end,
        }


class PersonalSchedule(models.Model):
    name = models.CharField(max_length = 30)

    def toJSON(self):
        return {
            **super().toJSON(),
            "id": self.id,
            "name": self.name,
        }


class TimeForAssignment(models.Model):
    studentAssignment = models.ForeignKey(StudentAssignment, related_name="timeForAssignments", on_delete=models.CASCADE)

    def toJSON(self):
        return {
            **super().toJSON(),
            "id": self.id,
            "name": self.name,
        }
