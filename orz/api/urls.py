from django.urls import include, path
from . import views


urlpatterns = [
    # List of schools
    path('schools', views.schools),

    # A specific school
    path('schools/<int:schoolID>', views.school),

    # List of courses in a specific school
    path('schools/<int:schoolID>/courses', views.schoolCourses),



    # A specific course
    path('courses/<int:courseID>', views.temp_view),

    # List of assignments of a specific course
    path('courses/<int:courseID>/assignments', views.temp_view),



    # A specific assignment
    path('assignments/<int:assignmentID>', views.temp_view),



    # A specific lecturer
    path('lecturer/<int:lecturerID>', views.temp_view),

    # List of courses managed by a specific lecturer
    path('lecturer/<int:lecturerID>/courses', views.temp_view),



    # A specific student
    path('student/<int:studentID>', views.temp_view),

    # List of courses subscribed by a specific student
    path('student/<int:studentID>/courses', views.temp_view),

    # List of assignments of a specific student
    path('student/<int:studentID>/assignments', views.temp_view),

    # A specific assignment of a specific student
    path('student/<int:studentID>/assignments/<int:AssignmentID>', views.temp_view),

    # List of personal schedules of a specific student
    path('student/<int:studentID>/personal-schedules', views.temp_view),

    # A specific personal schedule of a specific student
    path('student/<int:studentID>/personal-schedules/<int:scheduleID>', views.temp_view),

    # List of time for assignments of a specific student
    path('student/<int:studentID>/time-for-assignments', views.temp_view),

    # A specific time for assignment of a specific student
    path('student/<int:studentID>/time-for-assignments/<int:scheduleID>', views.temp_view)

]
