from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.blogs,name="blogs")
]