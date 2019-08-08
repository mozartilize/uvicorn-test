from django.urls import path
from . import views

urlpatterns = [
    path('todos/new', views.new, name='todo-new')
]