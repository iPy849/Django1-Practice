from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms

tasks = []

class NewTaskForm(forms.Form):
    task = forms.CharField(max_length=200, label='New Task')

# Create your views here.
def index(request):
    return render(request, 'todo/index.html', {
        'tasks': tasks
    })

@csrf_exempt
def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            tasks.append(form.cleaned_data['task'])

    return render(request, 'todo/add.html', {
        'form': NewTaskForm()
    })