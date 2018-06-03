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
        print(courses)
        ctx = [c.toJSON() for c in courses]
        return JsonResponse(ctx, safe=False)
    elif request.method == "POST":
        body = request.POST
        try:
            name = body["name"]
            code = body["code"]
            professor = body["professor"]
        except KeyError:
            return HttpResponseBadRequest('Missing fields in request data')

        course = Course.objects.create(
            school = school,
            name = name,
            code = code,
            professor = professor,
        )

        return JsonResponse(course.toJSON())


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
        print(body)
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
