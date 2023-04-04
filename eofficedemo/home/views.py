from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def home(request):
    return render(request, 'home.html')