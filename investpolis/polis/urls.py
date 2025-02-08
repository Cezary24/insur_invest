from django.shortcuts import render
from django.urls import path



from . import views
# Create your views here.
urlpatterns = [
    path("", view=views.create_polisy_file, name="create_polisy_file"),
]