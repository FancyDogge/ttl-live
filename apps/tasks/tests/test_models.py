from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task
from datetime import datetime


class TestTasksModels(TestCase):
    def setUp(self):
        User.objects.create(username='user1')
        Task.objects.create(
            name = '1TestTask',
            created_by = User.objects.get(id=1)
        )
        Task.objects.create(
            name = '2TaskWithDeadline',
            created_by = User.objects.get(id=1),
            deadline = datetime.strptime('2023-12-12 11:44:59', '%Y-%m-%d %H:%M:%S')
        )

    def test_default_status_is_active(self):
        task = Task.objects.get(id=1)
        self.assertEqual(task.status, 'Active')