from django.test import TestCase
from tasks.forms import TaskForm


class TestTasksForms(TestCase):

    def test_task_form_with_valid_data(self):
        form = TaskForm(data={
            'name': 'Testname',
            'description': 'whatever',
            'deadline': '2022-09-12 12:00:00'
        })

        self.assertTrue(form.is_valid())


    def test_task_form_with_wrong_data(self):
        form = TaskForm(data={
            'name': '',
            'description': '',
            'deadline': ''
        })

        self.assertFalse(form.is_valid())