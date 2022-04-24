from django.test import TestCase
from django.urls import reverse, resolve
from apps.core.views import register_user, login_user, about_page


class TestCoreUrls(TestCase):

    def test_registration_url_is_resoled(self):
        url = reverse('registration')
        self.assertEquals(resolve(url).func, register_user)


    def test_login_url_is_resoled(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_user)


    def test_about_page_url_is_resoled(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, about_page)