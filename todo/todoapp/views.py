from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import task
from .forms import todoform
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView


class Tasklistview(ListView):
    model = task
    template_name = 'home.html'
    context_object_name = 'tasks'

class TaskDetailview(DetailView):
    model = task
    template_name = 'detail.html'
    context_object_name = 'tasks'

class TaskUpdateview(UpdateView):
    model = task
    template_name = 'update.html'
    context_object_name = 'tasks'
    fields = ('Task', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetail', kwargs={'pk': self.object.id})

class TaskDeleteview(DeleteView):
    model = task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')


def add(request):
    tasks = task.objects.all()
    if request.method == "POST":
        Tasks = request.POST.get('task')
        prioritys = request.POST.get('priority')
        dates = request.POST.get('date')
        lst = task(Task=Tasks, priority=prioritys, date=dates)
        lst.save()
        return redirect('todoapp:add')  # Redirect to the 'add' view

    return render(request, 'home.html', {"tasks": tasks})


def detail(request):
    tasks = task.objects.all()
    return render(request, 'detail.html', {"tasks": tasks})


def deleted(request, taskid):
    taskss = task.objects.get(id=taskid)
    if request.method == "POST":
        taskss.delete()
        return redirect('todoapp:add')  # Redirect to the 'add' view

    return render(request, 'delete.html')


def update(request, id):
    tasks = task.objects.get(id=id)
    f = todoform(request.POST or None, instance=tasks)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request, 'edit.html', {'f': f, 'tasks': tasks})
