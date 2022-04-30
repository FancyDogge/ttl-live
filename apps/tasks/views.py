from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from django.contrib import messages
from tasks.forms import TaskForm, ChangeTaskForm
from django_q.tasks import schedule
from django_q.models import Schedule
from django.db.models import F
from .external_APIs import *


# scheduled deadline mail
def deadline_mail(request, task):

    schedule('django.core.mail.send_mail',
             'Your task is reaching a deadline!',
             f'Please be sure to finish your {task.name} task before {task.deadline}',
             'djnagotestmailkek@gmail.com',
             [request.user.email],
             schedule_type=Schedule.ONCE,
             # След. или первое время запуска ф-ции
             next_run=task.deadline - timedelta(days=3)
             )
    print(task.deadline - timedelta(days=3))



# -------Отобразить все task--------
@login_required
def view_tasks(request):
    # F класс помогает сортануть query,т.к в нем есть метод, сортирующий нулевые позиции в конец
    tasks = Task.objects.filter(created_by=request.user.id).order_by(
        F('deadline').desc(nulls_last=True))

    for task in tasks:
        if task.deadline:
            if task.status != task.TaskCurrentStatus.PAUSED and task.status != task.TaskCurrentStatus.DONE:
                if timezone.now() - task.deadline >= timedelta(days=0, hours=0, seconds=0):
                    task.status = task.TaskCurrentStatus.OVERDUE
                    task.save()
                elif timezone.now() - task.deadline >= timedelta(days=-3):
                    task.status = task.TaskCurrentStatus.DEADLINE
                    task.save()
                else:
                    task.status = task.TaskCurrentStatus.ACTIVE
                    task.save()

    # GETTING IP ADRESS, THEN GEOCODER GETS LAT LONG
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        users_ip = x_forwarded_for.split(',')[0]
    else:
        users_ip = request.META.get('REMOTE_ADDR')

    all_weather_info = weather_api_call(users_ip)
    if type(all_weather_info) is not dict:
        temperature = None
        feels_like = None
        wind = None
        country_and_city = None
        icon_url = None
    else:
        temperature = all_weather_info['temperature']
        feels_like = all_weather_info['feels like']
        wind = all_weather_info['wind']
        country_and_city = all_weather_info['country and city']
        icon_url = all_weather_info['icon_url']

    currency_excgange = get_rubusd_rate()
    usd_rub = currency_excgange[0]
    eur_rub = currency_excgange[1]

    bitcoin_price = get_bitcoin_price()

    cat_img = get_cat_img()

    context = {
        'tasks': tasks,
        'usd_rub': usd_rub,
        'eur_rub': eur_rub,
        'temperature': temperature,
        'feels_like': feels_like,
        'wind': wind,
        'country_and_city': country_and_city,
        'icon_url': icon_url,
        'bitcoin_price': bitcoin_price,
        'cat_img': cat_img,
    }
    return render(request, 'tasks/tasks.html', context)


# -------Отобразить определенный taks--------
@login_required
def view_task(request, pk):
    task = get_object_or_404(Task, id=pk)

    if task.created_by == request.user:
        return render(request, 'tasks/task.html', {'task': task, 'exchange_rate': get_rubusd_rate, 'weather': weather_api_call})
    else:
        messages.error(request, 'You have no rights to view this task!')
        return redirect('tasks')

# --------Создать task-=------


@login_required
def create_task(request):
    # указываем форму
    form = TaskForm(request.POST or None)
    # чекаем правильность заполнения и сохраняем, если все ок
    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.save()
        if task.deadline is not None:
            deadline_mail(request, task)
        messages.success(request, 'Task was successfully created!')
        return redirect('tasks')
    return render(request, 'tasks/create_task.html', {'form': form})


# --------Изменить существующий task---------
@login_required
def change_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task.created_by == request.user:
        # чтобы изменить существующий объект, нужно передать форме параметр instance, с указанием объекта для изменений
        # иначе джанго попытается с помощью формы создать новый объкт
        form = ChangeTaskForm(request.POST or None, instance=task)
        form.initial['name'] = task.name
        form.initial['description'] = task.description
        form.initial['deadline'] = task.deadline
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Task was successfully changed!')
                return redirect('task', pk=task.pk)

        return render(request, 'tasks/create_task.html', {'form': form})
    else:
        messages.error(request, 'You have no rights to change this task!')
        return redirect('tasks')


#--------Поставить task на паузу---------        
@login_required
def pause_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task.created_by == request.user:
        if task.status == task.TaskCurrentStatus.PAUSED:
            task.status = task.TaskCurrentStatus.ACTIVE
            task.save()
            messages.success(request, 'Task was successfully unpaused!')
            return redirect('tasks')
        else:
            task.status = task.TaskCurrentStatus.PAUSED
            task.save()
            messages.success(request, 'Task was successfully paused!')
            return redirect('tasks')
    else:
        messages.error(request, 'You have no rights to change this task!')
        return redirect('tasks')


# -------Завершить task-------
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task.created_by == request.user:
        task.status = task.TaskCurrentStatus.DONE
        task.save()
        messages.success(request, 'Task was completed!')

        return redirect('tasks')
    else:
        messages.error(request, 'You have no rights to change this task!')
        return redirect('tasks')


# -------Удаление task-------
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.user == task.created_by:
        task.delete()
        messages.success(request, 'Task was deleted!')
        return redirect('tasks')
    messages.error(request, "This is not your task!")
    return redirect('tasks')
