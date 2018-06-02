from django.http import JsonResponse
from orz.api.models import *
from django.shortcuts import get_object_or_404



def temp_view(request):
    return JsonResponse({"text":"Hello, World!"})


def schools(request):
    if request.method == "GET":
        schools = School.objects.all()
        ctx = [s.toJSON() for s in schools]
        return JsonResponse(ctx, safe=False)


def school(request, schoolID):
    if request.method == "GET":
        school = get_object_or_404(School, id=schoolID)
        ctx = school.toJSON()
        return JsonResponse(ctx)


def schoolCourses(request, schoolID):
    if request.method == "GET":
        school = get_object_or_404(School, id=schoolID)
        courses = Course.objects.filter(school=school)
        print(courses)
        ctx = [c.toJSON() for c in courses]
        return JsonResponse(ctx, safe=False)
