from time import sleep
from django.shortcuts import render, redirect
from django.db import connection as db, connections
from .models import Todo


def new(request):
    error = None
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            todo = Todo(content=content)
            Todo.APP_PORT = request.get_port()
            todo.save()
            # sleep(15)
            return redirect('todo-new')
        else:
            error = 'Content cant be blank'
    return render(request, 'todo/new.html', {'error': error})

