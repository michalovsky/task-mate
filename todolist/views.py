from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist.models import TaskList
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            db_instance = form.save(commit=False)
            db_instance.manage = request.user
            db_instance.save()
            messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        tasks = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(tasks, 5)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'tasks': tasks})


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, ("Task Edited!"))
        return redirect('todolist')
    else:
        task = TaskList.objects.get(pk=task_id)
        context = {'task': task}
        return render(request, 'edit.html', context)


@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access restricted, you are not allowed"))
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, ("Access restricted, you are not allowed"))
    return redirect('todolist')


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ("Access restricted, you are not allowed"))
    return redirect('todolist')


def index(request):
    context = {'index_text': 'Welcome to Home page!'}
    return render(request, 'index.html', context)


def contact(request):
    context = {'contact_text': 'Welcome to Contact page!'}
    return render(request, 'contact.html', context)


def about(request):
    context = {'about_text': 'Welcome to About page!'}
    return render(request, 'about.html', context)
