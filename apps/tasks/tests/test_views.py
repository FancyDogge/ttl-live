from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from ..models import Task

    # def setUp(self):
    #     self.user1 = User.objects.create(username = 'TestUser')
    #     self.task1 = Task.objects.create(
    #         name = 'TestTask1',
    #         created_by = self.user1
    #     )
    #     self.task2 = Task.objects.create(
    #         name = 'TestTask2',
    #         created_by = self.user1
    #     )


#Testing view_tasks view
class TestTasksViews(TestCase):

    def setUp(self):
        #TestUser1
        self.user1 = User.objects.create(username = 'TestUser1')
        #client.login не работал, т.к. если задавать пароль через user.obj.create, он хэшировался
        self.user1.set_password('123456789')
        self.user1.save()

        #TestUser2
        self.user2 = User.objects.create(username = 'TestUser2')
        self.user2.set_password('123456789')
        self.user2.save()

        #Tasks for TestUser1
        self.task1 = Task.objects.create(
            name = 'TestTask1',
            created_by = self.user1
        )
        self.task2 = Task.objects.create(
            name = 'TestTask2',
            created_by = self.user1
        )

        #Client
        self.client = Client()
        self.user_login = self.client.login(username = 'TestUser1', password = '123456789')

    def test_redirect_if_not_logged(self):
        self.client.logout()

        response = self.client.get(reverse('tasks'))

        self.assertEquals(response.status_code, 302)


    def test_get_all_tasks_view(self):
        self.assertTrue(self.user_login)

        response = self.client.get(reverse('tasks'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks.html')

    
    def test_user_cant_access_another_users_tasks(self):
        user2_login = self.client.login(username = 'TestUser2', password = '123456789')
        self.assertTrue(user2_login)
        #task is created by User1, Not User2 that logged in
        response = self.client.get(reverse('task', kwargs={'pk': self.task1.pk}))
        #Из-за редиректа у response нет контекста, так что месседжы приходится искать с list(get_messages(response.wsgi_request))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have no rights to view this task!')
        self.assertEquals(response.status_code, 302)
        

    def test_view_task(self):
        response = self.client.get(reverse('task', kwargs={'pk': self.task1.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task.html')


    def test_create_task_GET(self):
        response = self.client.get(reverse('create_task'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create_task.html')


    def test_create_task_POST(self):

        self.assertFalse(Task.objects.filter(name='TestTask3', id=3).exists())

        response = self.client.post(reverse('create_task'), {
            'name': 'TestTask3',
            'created_by': self.user1
        })
        #Из-за редиректа у response нет контекста, так что месседжы приходится искать с list(get_messages(response.wsgi_request))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Task was successfully created!')
        self.assertTrue(Task.objects.filter(name='TestTask3', id=3).exists())
        self.assertEquals(response.status_code, 302)

    
    def test_create_task_POST_with_no_data(self):

        response = self.client.post(reverse('create_task'))

        #There are 2 tasks in setUp
        self.assertEquals(Task.objects.all().count(), 2)     
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create_task.html')


    def test_change_task_GET(self):

        response = self.client.get(reverse('change_task', kwargs={'pk': self.task1.pk}))
   
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create_task.html')


    def test_change_task_POST(self):
        
        response = self.client.post(reverse('change_task', kwargs={'pk': self.task1.pk}), {
            'name':'ChangedTask1',
            'status': self.task1.status
        })
        
        #нужно обновить таск из дб, иначе, как я понял, в сетапе старая версия инстанса будет
        self.task1.refresh_from_db()

        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEqual(self.task1.name, 'ChangedTask1')
        self.assertEquals(response.status_code, 302)


    def test_change_task_POST_cant_be_used_on_another_users_task(self):
        self.client.login(username = 'TestUser2', password = '123456789')

        response = self.client.post(reverse('change_task', kwargs={'pk': self.task1.pk}), {
            'name':'ChangedTask1',
            'status': self.task1.status
        })
        messages = list(get_messages(response.wsgi_request))

        self.task1.refresh_from_db()

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have no rights to change this task!')
        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEqual(self.task1.name, 'TestTask1')
        self.assertEquals(response.status_code, 302)


    def test_change_task_POST_with_no_data(self):
        
        response = self.client.post(reverse('change_task', kwargs={'pk': self.task1.pk}))

        self.task1.refresh_from_db()

        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEqual(self.task1.name, 'TestTask1')
        self.assertEquals(response.status_code, 200)


    def test_change_task_POST_with_invalid_form_data (self):
        
        response = self.client.post(reverse('change_task', kwargs={'pk': self.task1.pk}), {
            'name': '',
        })

        self.task1.refresh_from_db()

        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEqual(self.task1.name, 'TestTask1')
        self.assertEquals(response.status_code, 200)


    def test_complete_task_view(self):
        
        response = self.client.post(reverse('complete_task', kwargs={'pk': self.task1.pk}))
        messages = list(get_messages(response.wsgi_request))

        self.task1.refresh_from_db()

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Task was completed!')
        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEqual(self.task1.status, Task.TaskCurrentStatus.DONE)
        self.assertEquals(response.status_code, 302)


    def test_complete_task_view_cant_be_used_by_another_user(self):
        self.client.login(username = 'TestUser2', password = '123456789')

        response = self.client.post(reverse('complete_task', kwargs={'pk': self.task1.pk}))
        messages = list(get_messages(response.wsgi_request))

        self.task1.refresh_from_db()

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have no rights to change this task!')
        self.assertEqual(self.task1.status, Task.TaskCurrentStatus.ACTIVE)
        self.assertEquals(response.status_code, 302)


    def test_delete_task(self):
        response = self.client.post(reverse('delete_task', kwargs={'pk': self.task1.pk}))
        messages = list(get_messages(response.wsgi_request))

        #self.task1.refresh_from_db()

        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertEquals(Task.objects.all().count(), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Task was deleted!')
        self.assertEquals(response.status_code, 302)


    def test_delete_task_cant_be_called_by_another_user(self):
        self.client.login(username = 'TestUser2', password = '123456789')

        response = self.client.post(reverse('delete_task', kwargs={'pk': self.task1.pk}))
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This is not your task!')
        self.assertEquals(response.status_code, 302)
