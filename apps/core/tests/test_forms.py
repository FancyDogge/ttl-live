from django.test import TestCase
from core.forms import RegisterForm, AuthForm
from django.contrib.auth.models import User


class TestCoreForms(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username = 'TestUser2')
        self.user1.set_password('123456789Ss')
        self.user1.save()


    def test_registration_form_with_valid_data(self):
        form = RegisterForm(data = {
            "username": 'TestUser',
            "email": 'testuser@gmail.com',
            'password1': '123456789Ss',
            'password2': '123456789Ss'
        })

        self.assertTrue(form.is_valid())


    def test_registration_form_with_usecure_password(self):
        form = RegisterForm(data = {
            "username": 'TestUser',
            "email": 'testuser@gmail.com',
            'password1': '123456789',
            'password2': '123456789'
        })

        self.assertFalse(form.is_valid())


    def test_registration_form_with_no_data(self):
        form = RegisterForm(data = {
            "username": '',
            "email": '',
            'password1': '',
            'password2': ''
        })

        self.assertFalse(form.is_valid())


    def test_auth_form_with_valid_data(self):
        form = AuthForm(data = {
            "username": 'TestUser2',
            'password': '123456789Ss',
        })

        self.assertTrue(form.is_valid())


    def test_auth_form_with_wrong_data(self):
        form = AuthForm(data = {
            "username": 'Test',
            'password': '12345',
        })

        self.assertFalse(form.is_valid())


    def test_auth_form_with_no_data(self):
        form = AuthForm(data = {
            "username": '',
            'password': '',
        })

        self.assertFalse(form.is_valid())