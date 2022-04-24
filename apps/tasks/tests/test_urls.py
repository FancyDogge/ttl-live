from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task
from django.urls import reverse, resolve
from apps.tasks.views import view_tasks, view_task, create_task, change_task, complete_task, delete_task


class TestTasksUrls(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username = 'TestUser')
        self.task1 = Task.objects.create(
            name = 'TestTask1',
            created_by = self.user1
        )

    def test_tasks_url_is_resoled(self):
        url = reverse('tasks')
        #.ResolverMatch(func=apps.tasks.views.view_tasks, args=(), kwargs={}, url_name='tasks', app_names=[], namespaces=[], route='')
        self.assertEquals(resolve(url).func, view_tasks)


    def test_single_task_url_is_resoled(self):
        url = reverse('task', kwargs={'pk': self.task1.pk})
        self.assertEquals(resolve(url).func, view_task)


    def test_create_task_url_is_resoled(self):
        url = reverse('create_task')
        self.assertEquals(resolve(url).func, create_task)


    def test_change_task_url_is_resoled(self):
        url = reverse('change_task', kwargs={'pk': self.task1.pk})
        self.assertEquals(resolve(url).func, change_task)


    def test_complete_task_url_is_resoled(self):
        url = reverse('complete_task', kwargs={'pk': self.task1.pk})
        self.assertEquals(resolve(url).func, complete_task)


    def test_delete_task_url_is_resoled(self):
        url = reverse('delete_task', kwargs={'pk': self.task1.pk})
        self.assertEquals(resolve(url).func, delete_task)