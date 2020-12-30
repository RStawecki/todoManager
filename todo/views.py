from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from todo.models import Todo
from todo.forms import TodoForm
from django.utils import timezone

#todo
def home(request):
    return render(request, 'todo/home.html')

def create_todo(request):
    if request.method == "GET":
        form = TodoForm()
        return render(request, 'todo/create_todo.html', {'form': form})
    else:
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todos')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'todo/create_todo.html', {'form': form, 'error': error})

def detail(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == "GET":
        form = TodoForm(instance = todo)
        return render(request, 'todo/detail.html', {'zadanie': todo, 'form': form})
    else:
        form = TodoForm(request.POST, instance = todo)
        if form.is_valid():
            todo.save()
            return redirect('todos')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'todo/detail.html', {'form': form, 'error': error})


def todos(request):
    current = Todo.objects.filter(user=request.user, compliteDate__isnull=True)
    completed = Todo.objects.filter(user=request.user, compliteDate__isnull=False)
    return render(request, 'todo/todos.html', {'current': current, 'completed': completed})

def complete(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.compliteDate = timezone.now()
        todo.save()
        return redirect('todos')

#auth
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
