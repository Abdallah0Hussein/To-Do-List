from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from . forms import *
import time
from django.db.models.functions import Lower
from django.db.models import Q

# Create your views here.


def sort_tasks_by_priority(tasks):
    dict_map = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
    }
    # The sorting is based on the key
    # we use a lambda function as the key
    # lambda function takes each task as input and returns an int value that will be used for sorting
    # (converts each Task object's to an int value for sorting)
    return sorted(tasks, key=lambda task: dict_map.get(task.priority, 0))


def search_tasks(tasks, search_query):
    if search_query:
        return tasks.filter(title__icontains=search_query)
    return tasks


def index(request):
    form = TaskForm()
    # request.GET >>> is a dictionary that contains all the GET parameters passed view via the URL.

    # get the value of the 'sort_by' parameter from the GET request which is in the URL.
    # should ensure that the name attribute of the select element in HTML is "sort_by" (the same)
    # as the selected value will be sent as a parameter named "sort_by" in the GET request
    sort_by = request.GET.get('sort_by', 'priority')
    search = request.GET.get('search', '')

    # assign all records from the associated database table.
    # tasks here is a list
    tasks = Task.objects.all()
    tasks = search_tasks(tasks, search)
    if sort_by == 'priority':
        tasks = sort_tasks_by_priority(tasks)
    elif sort_by == 'name':
        tasks = Task.objects.all().order_by(Lower('title'))
    else:
        tasks = tasks.order_by('deadline')

    error_message = 'Deadline input is not valid. Check your input.'
    err = {'error_message': error_message}
    context = {'tasks': tasks, 'form': form}

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'tasks/list.html', err)
        return redirect('/')
    # rendering an HTML template with a given context
    # then returning an HTTP response with the rendered content
    return render(request, 'tasks/list.html', context)

# The pk argument is passed in, from the URL when you access a specific task's update page. from urls.py
# this <str:pk> specifies an integer value, which will be the (pk) of the task you wanna update.
# /update.html/1/ >> so 1 is the pk


def updateTask(request, pk):
    # Retrieve the task to be updated from the database using its primary key (pk)
    task = Task.objects.get(id=pk)
    # Initialize a TaskForm instance with the existing task data
    form = TaskForm(instance=task)
    # If The form is submitted
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'tasks/delete_task.html', context)


def clear_all_tasks(request):
    Task.objects.all().delete()
    return redirect('list')
