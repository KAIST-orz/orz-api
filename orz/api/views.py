from django.http import JsonResponse, HttpResponseBadRequest
from orz.api.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods



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
