from django.test import TestCase
from django.urls import reverse, resolve
from apps.dashboard.views import dashboard_view, userprofile


class TestDashboardUrls(TestCase):

    def test_dashboard_url_is_resoled(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func, dashboard_view)


    def test_dashboard_url_is_resoled(self):
        url = reverse('userprofile')
        self.assertEquals(resolve(url).func, userprofile)