from django.test import TestCase
from dashboard.forms import UpdateAvatar
from django.core.files.uploadedfile import SimpleUploadedFile


class TestDahboardForms(TestCase):

    def test_dashboard_form_with_valid_data(self):
        form = UpdateAvatar(data={
            "avatar": SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        })

        self.assertTrue(form.is_valid())


    def test_dashboard_form_with_wrong_data(self):
        form = UpdateAvatar(data={
            'avatar': 'uploads/avatars/default.jpg'
        })

        self.assertFalse(form.is_valid())