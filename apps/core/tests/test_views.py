from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from core.views import login_user, register_user, about_page
from django.core.files.uploadedfile import SimpleUploadedFile


class TestCoreViews(TestCase):

    def setUp(self):
        #TestUser1
            self.user1 = User.objects.create(username = 'TestUser1')
            self.user1.set_password('123456789')
            self.user1.save()

            self.client = Client()


    def test_register_user_view_POST_correct_data(self):

        response = self.client.post(reverse('registration'), data={
            "username": 'Test',
            "email": 'test@gmail.com',
            'password1': '123456789Ss',
            'password2': '123456789Ss'
        })
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have been successfully registered!')
        self.assertTrue(User.objects.filter(username='Test').exists())
        self.assertEquals(response.status_code, 302)


    def test_register_user_view_POST_invalid_data(self):

        response = self.client.post(reverse('registration'), data={
            "username": 'Test',
            "email": 'testmail.com',
            'password1': '12345',
            'password2': '12345'
        })

        self.assertEquals(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='Test').exists())
        self.assertTemplateUsed(response, 'core/registration.html')


    def test_register_user_view_GET(self):

        response = self.client.get(reverse('registration'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/registration.html')


    def test_register_user_view_GET_if_already_logged(self):
        self.client.login(username = 'TestUser1', password = '123456789')

        response = self.client.get(reverse('registration'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You are already logged in!')
        self.assertEquals(response.status_code, 302)


    def test_about_view(self):

        response = self.client.get(reverse('about'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
