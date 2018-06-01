from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    school = models.ForeignKey("School", on_delete=models.PROTECT)



class Lecturer(models.Model):
    user = models.OneToOneField("User", related_name="lecturerProfile", on_delete=models.CASCADE)



class Student(models.Model):
    user = models.OneToOneField("User", related_name="studentProfile", on_delete=models.CASCADE)
    subscribingCourses = models.ManyToManyField("Assignment", related_name="students", through="StudentAssignment")



class School(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)



class Course(models.Model):
    lecturer = models.ForeignKey("Lecturer", related_name="managingCourses", on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey("School", on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    professor = models.CharField(max_length = 30)



class Assignment(models.Model):
    course = models.ForeignKey("Assignment", related_name="assignments", on_delete=models.CASCADE)
    name = models.CharField(max_length = 30)
    due = models.DateTimeField()
    averageTimeEstimation = models.FloatField()
    description = models.CharField(max_length = 200)



class StudentAssignment(models.Model):
    student = models.ForeignKey("Student", related_name="studentAssignments", on_delete=models.CASCADE)
    assignment = models.ForeignKey("Assignment", related_name="studentAssignments", on_delete=models.CASCADE)
    timeEstimation = models.IntegerField()



class Schedule(models.Model):
    student = models.ForeignKey(Student, related_name="%(class)ss", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        abstract = True



class PersonalSchedule(models.Model):
    name = models.CharField(max_length = 30)



class TimeForAssignment(models.Model):
    studentAssignment = models.ForeignKey(StudentAssignment, related_name="timeForAssignments", on_delete=models.CASCADE)

