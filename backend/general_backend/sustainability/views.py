from django.shortcuts import render
from django.http import HttpResponse

#sustainability/views.py - maintains all logic to handle backend-frontend interaction

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


