from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import skip


class TestViews(TestCase):

    def setUp(self):
        #TestUser1
        self.user1 = User.objects.create(username = 'TestUser1')
        #client.login не работал, т.к. если задавать пароль через user.obj.create, он хэшировался
        self.user1.set_password('123456789')
        self.user1.save()

        #Client
        self.client = Client()
        self.user_login = self.client.login(username = 'TestUser1', password = '123456789')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEquals(response.status_code, 200)


    def test_userprofile_view_GET(self):
        response = self.client.get(reverse('userprofile'))

        self.assertEquals(response.status_code, 200) 


    @skip("Don't want to test right now")
    def test_userprofile_view_POST(self):
        response = self.client.post(reverse('userprofile'), data={
            "avatar": SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        })
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your profile picture was successfully updated!')
        self.assertEquals(response.status_code, 302)
