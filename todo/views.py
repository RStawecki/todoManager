from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'todo/home.html')

def signupUser(request):
    if request.method == "GET":
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], "", request.POST['password1'])
            except IntegrityError:
                error = "Username exist. Try again."
                return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': error})
            else: 
                user.save()
                login(request, user)
                return redirect('home')

        else:
            error = "Password didn't match. Try again."
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': error})

def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Username or password is incorrect."
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': error})

def logoutUser(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')
