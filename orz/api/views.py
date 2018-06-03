from django.http import JsonResponse, HttpResponseBadRequest
from orz.api.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import QueryDict


def temp_view(request):
    return JsonResponse({"text":"Hello, World!"})


@csrf_exempt
@require_http_methods(["GET"])
def schools(request):
    if request.method == "GET":
        schools = School.objects.all()

        ctx = [s.toJSON() for s in schools]
        return JsonResponse(ctx, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def school(request, schoolID):
    if request.method == "GET":
        school = get_object_or_404(School, id=schoolID)

        ctx = school.toJSON()
        return JsonResponse(ctx)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def schoolCourses(request, schoolID):
    school = get_object_or_404(School, id=schoolID)

    if request.method == "GET":
        courses = Course.objects.filter(school=school)

        ctx = [c.toJSON() for c in courses]
        return JsonResponse(ctx, safe=False)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def course(request, courseID):
    course = get_object_or_404(Course, id=courseID)

    if request.method == "GET":
        ctx = course.toJSON()
        return JsonResponse(ctx, safe=False)

    elif request.method == "PUT":
        body = QueryDict(request.body)
        try:
            name = body["name"]
            code = body["code"]
            professor = body["professor"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        course.name = name
        course.code = code
        course.professor = professor
        course.save()

        ctx = course.toJSON()
        return JsonResponse(ctx)

    elif request.method == "DELETE":
        course.delete()

        return JsonResponse({})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def courseAssignments(request, courseID):
    course = get_object_or_404(Course, id=courseID)

    if request.method == "GET":
        assignments = course.assignments.all()

        ctx = [a.toJSON() for a in assignments]
        return JsonResponse(ctx, safe=False)

    elif request.method == "POST":
        body = QueryDict(request.body)
        try:
            name = body["name"]
            due = body["due"]
            description = body["description"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        assignment = Assignment.objects.create(
            course = course,
            name = name,
            due = due,
            description = description,
        )

        ctx = assignment.toJSON()
        return JsonResponse(ctx)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def assignment(request, assignmentID):
    assignment = get_object_or_404(Assignment, id=assignmentID)

    if request.method == "GET":
        ctx = assignment.toJSON()
        return JsonResponse(ctx)

    elif request.method == "PUT":
        body = QueryDict(request.body)
        try:
            name = body["name"]
            due = body["due"]
            description = body["description"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        assignment.name = name
        assignment.due = due
        assignment.description = description
        assignment.save()

        ctx = assignment.toJSON()
        return JsonResponse(ctx)

    elif request.method == "DELETE":
        assignment.delete()

        return JsonResponse({})


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def user(request, userID):
    user = get_object_or_404(User, id=userID)

    if request.method == "GET":
        ctx = user.toJSON()
        return JsonResponse(ctx)

    elif request.method == "PUT":
        body = QueryDict(request.body)
        try:
            email = body["email"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        user.email = email
        if "password" in body:
            user.set_password(body["password"])
        user.save()

        ctx = user.toJSON()
        return JsonResponse(ctx)

    elif request.method == "DELETE":
        user.delete()

        return JsonResponse({})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def lecturerCourses(request, userID):
    lecturer = get_object_or_404(Lecturer, user__id=userID)

    if request.method == "GET":
        courses = lecturer.managingCourses.all()

        ctx = [c.toJSON() for c in courses]
        return JsonResponse(ctx, safe=False)

    elif request.method == "POST":
        body = QueryDict(request.body)
        try:
            name = body["name"]
            code = body["code"]
            professor = body["professor"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        course = Course.objects.create(
            lecturer = lecturer,
            school = lecturer.user.school,
            name = name,
            code = code,
            professor = professor,
        )

        ctx = course.toJSON()
        return JsonResponse(ctx)


@csrf_exempt
@require_http_methods(["GET"])
def studentCourses(request, userID):
    if request.method == "GET":
        student = get_object_or_404(Student, user__id=userID)
        courses = student.subscribingCourses.all()

        ctx = [c.toJSON() for c in courses]
        return JsonResponse(ctx, safe=False)


@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def studentCourse(request, userID, courseID):
    student = get_object_or_404(Student, user__id=userID)
    course = get_object_or_404(Course, id=courseID)

    if request.method == "POST":
        student.subscribingCourses.add(course)

        return JsonResponse({})

    elif request.method == "DELETE":
        student.subscribingCourses.remove(course)

        return JsonResponse({})


@csrf_exempt
@require_http_methods(["GET"])
def studentAssignments(request, userID):
    student = get_object_or_404(Student, user__id=userID)

    if request.method == "GET":
        ctx = []
        for c in student.subscribingCourses.all():
            for a in c.assignments.all():
                studentAssignment = StudentAssignment.objects.get_or_create(student=student, assignment=a)[0]
                ctx.append(studentAssignment.toJSON())

        return JsonResponse(ctx, safe=False)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def studentAssignment(request, userID, assignmentID):
    student = get_object_or_404(Student, user__id=userID)
    assignment = get_object_or_404(Assignment, id=assignmentID)
    studentAssignment = StudentAssignment.objects.get_or_create(student=student, assignment=assignment)[0]

    if request.method == "GET":
        ctx = studentAssignment.toJSON()
        return JsonResponse(ctx)

    elif request.method == "PUT":
        body = QueryDict(request.body)
        try:
            timeEstimation = body["timeEstimation"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        studentAssignment.timeEstimation = timeEstimation
        studentAssignment.save()

        assignment.updateAverageTimeEstimation()

        ctx = studentAssignment.toJSON()
        return JsonResponse(ctx)


@csrf_exempt
@require_http_methods(["GET"])
def studentCalendarEvents(request, userID):
    if request.method == "GET":
        student = get_object_or_404(Student, user__id=userID)
        assignments = Assignment.objects.filter(course__students=student)
        personalSchedules = PersonalSchedule.objects.filter(student=student)
        timeForAssignments = TimeForAssignment.objects.filter(student=student)

        ctx = {
            "assignments": [a.toJSON() for a in assignments],
            "personalSchedules": [p.toJSON() for p in personalSchedules],
            "timeForAssignments": [t.toJSON() for t in timeForAssignments],
        }
        return JsonResponse(ctx)
