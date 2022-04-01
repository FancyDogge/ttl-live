from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    #нужно указать какую модель использовать с помощью мета класса
    class Meta:
        model = Task

        #теперь поля, которые будут использоваться
        fields = [
            'name',
            'description',
            'deadline'
        ]
        #ураа, вот как добавлять виджет дял даты
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }


class ChangeTaskForm(forms.ModelForm):
    class Meta:      
        model = Task

        fields = [
            'name',
            'description',
            'status',
            'deadline'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }