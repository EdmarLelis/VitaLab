from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

@login_required
def solicitar_exames(request):
    if request.method == 'GET':
        return render(request, 'solicitar_exames.html')
#2. 00:18:20 ...