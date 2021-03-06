from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import Userprofile
from django.contrib import messages
from .forms import UpdateAvatar


#-------Дэшбоард------
@login_required
def dashboard_view(request):
    user = request.user

    comptleted_tasks = user.tasks.filter(status='Done').order_by('-created_at')
    paused_tasks = user.tasks.filter(status='Paused').order_by('-created_at')

    closest_deadline = user.tasks.filter(status='Active').order_by('deadline')
    
    context = {
        'username': user.username,
        'completed_tasks': comptleted_tasks,
        'paused_tasks': paused_tasks,
        'closest_deadline': closest_deadline
    }

    return render(request, 'dashboard/dashboard.html', context)


#-------Профиль------
@login_required
def userprofile(request):
    # user = get_object_or_404(User, id=request.user.id)

    user_profile = get_object_or_404(Userprofile, user=request.user)
    
    #если в форме есть файлы, нужно это прописать
    form = UpdateAvatar(request.POST or None, request.FILES)
    if form.is_valid():
        #avatar - поле формы
        if 'avatar' in request.FILES:
            user_profile.avatar = request.FILES['avatar']
            user_profile.save()
            messages.success(request, "Your profile picture was successfully updated!")
            return redirect('userprofile')


    return render(request, 'dashboard/profile_page.html', {'user':request.user, 'form':form})