from django.shortcuts import render
from django.http import HttpResponse

def blogs(request):
    return render(request,'blog/index.html')