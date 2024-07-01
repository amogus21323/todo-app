from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Tasks
from .forms import TasksForm
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskEditForm

@login_required
def task_list(request):
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, 'task/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TasksForm()
    return render(request, 'task/add_task.html', {"form": form})

@login_required
def completed_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if not task.is_completed:
        task.is_completed = True
        task.save()
    return redirect('task_list')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'task/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('task_list')

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = SignUpForm()
    return render(request, 'task/register.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskEditForm(instance=task)
    return render(request, 'task/edit_task.html', {'form': form, 'task': task})