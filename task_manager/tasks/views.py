from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib import messages

def index(request):
    return render(request, 'index.html')


@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})
from django.shortcuts import render, redirect
from .forms import TaskForm


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return redirect('task_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})