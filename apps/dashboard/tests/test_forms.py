from django.test import TestCase
from dashboard.forms import UpdateAvatar
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import skip


class TestDahboardForms(TestCase):
    @skip("Don't want to test right now")
    def test_dashboard_form_with_valid_data(self):
        form = UpdateAvatar(data={
            "avatar": SimpleUploadedFile(name='test_image.jpg', content=b'photo', content_type='image/jpeg')
        })

        self.assertTrue(form.is_valid())


    @skip("Don't want to test right now")
    def test_dashboard_form_with_wrong_data(self):
        form = UpdateAvatar(data={
            'avatar': SimpleUploadedFile(name='test.txt', content=b'', content_type='text/plain')
        })

        self.assertFalse(form.is_valid())


    @skip("Don't want to test right now")
    def test_dashboard_form_with_no_data(self):
        form = UpdateAvatar(data={})
        self.assertFalse(form.is_valid())