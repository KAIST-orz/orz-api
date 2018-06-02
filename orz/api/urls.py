from django.urls import include, path
from . import views


urlpatterns = [
    path('some_url', views.temp_view),
]
