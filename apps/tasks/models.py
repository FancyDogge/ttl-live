from turtle import back
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    class TaskCurrentStatus(models.TextChoices):
        ACTIVE = 'Active', ('Active')
        DEADLINE = 'Deadline Soon', ('Deadline')
        OVERDUE = 'Overdue', ('Overdue')
        PAUSED = 'Paused', ('Paused')
        DONE = 'Done', ('Done')

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=15,choices=TaskCurrentStatus.choices, default=TaskCurrentStatus.ACTIVE)
    created_by = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name