from django.urls import include, path
from . import views


urlpatterns = [
    # List of schools
    # Allowed methods : GET
    path('schools', views.schools),

    # A specific school
    # Allowed methods : GET
    path('schools/<int:schoolID>', views.school),

    # List of courses in a specific school
    # Allowed methods : GET, POST
    path('schools/<int:schoolID>/courses', views.schoolCourses),



    # A specific course
    # Allowed methods : GET, PUT, DELETE
    path('courses/<int:courseID>', views.course),

    # List of assignments of a specific course
    # Allowed methods : GET, POST
    path('courses/<int:courseID>/assignments', views.courseAssignments),



    # A specific assignment
    # Allowed methods : GET, PUT, DELETE
    path('assignments/<int:assignmentID>', views.assignment),



    # A specific lecturer
    path('lecturers/<int:userID>', views.temp_view),

    # List of courses managed by a specific lecturer
    path('lecturers/<int:userID>/courses', views.temp_view),



    # A specific student
    path('students/<int:userID>', views.temp_view),

    # List of courses subscribed by a specific student
    path('students/<int:userID>/courses', views.temp_view),

    # List of assignments of a specific student
    path('students/<int:userID>/assignments', views.temp_view),

    # A specific assignment of a specific student
    path('students/<int:userID>/assignments/<int:AssignmentID>', views.temp_view),

    # List of personal schedules of a specific student
    path('students/<int:userID>/personal-schedules', views.temp_view),

    # A specific personal schedule of a specific student
    path('students/<int:userID>/personal-schedules/<int:scheduleID>', views.temp_view),

    # List of time for assignments of a specific student
    path('students/<int:userID>/time-for-assignments', views.temp_view),

    # A specific time for assignment of a specific student
    path('students/<int:userID>/time-for-assignments/<int:scheduleID>', views.temp_view)

]
