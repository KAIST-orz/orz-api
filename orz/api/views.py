from django.http import JsonResponse



def temp_view(request):
    return JsonResponse({"text":"Hello, World!"})

