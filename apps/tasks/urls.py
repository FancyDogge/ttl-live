from asyncio import tasks
from django.urls import path
from .views import *

urlpatterns = [
    path('', view_tasks, name='tasks'),
    path('task/<int:pk>/', view_task, name='task'),
    path('create/', create_task, name='create_task'),
    path('delete/<int:pk>', delete_task, name='delete_task'),
    path('complete/<int:pk>', complete_task, name='complete_task'),
    path('task/<int:pk>/change', change_task, name='change_task'),
]