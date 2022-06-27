from django.shortcuts import  render, redirect
from .forms import RegisterForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from dashboard.models import Userprofile
from django.core.mail import send_mail


#-------Email при регистрации и логине------
def send_registration_email(user):

    send_mail(
    subject = f"Your TTL Account Was Successfully Created!",
    message = f"Greetings, {user.username}, I'm glad that you joined my little project! \n You can start tracking your tasks now!",
    from_email = 'djnagotestmailkek@gmail.com',
    recipient_list = [f'{user.email}'],
    )

def login_email(user):

    send_mail(
    subject = f"You've logged in to your TTL account",
    message = f"Hello, {user.username}, if it wasnt you, please follow this link and change your password!",
    from_email = 'djnagotestmailkek@gmail.com',
    recipient_list = [f'{user.email}'],
    )


#-------Регистрация------
def register_user(request):
	if request.user.is_authenticated:
		messages.error(request, 'You are already logged in!')
		return redirect('tasks')
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()

		#создание юзерпрофиля с аватаркой
		# user_profile = Userprofile.objects.create(
		# 	user=user,
		# 	avatar='uploads/avatars/default.jpg'
		# )
		# user_profile.save()

		login(request, user)
		send_registration_email(user)
		messages.success(request, 'You have been successfully registered!')
		return redirect('tasks')
		
	return render(request, 'core/registration.html', {'form':form})


#-------Логин------
def login_user(request):
	if request.user.is_authenticated:
		return redirect('tasks')
	else:
		form = AuthenticationForm(request.POST or None)
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				login_email(user)
				return redirect('tasks')
			else:
				messages.info(request, 'Username OR password is incorrect')

	return render(request, 'core/login.html', {'form':form})


#-------Логин как демо юзер------
def login_demo_user(request):
	if request.user.is_authenticated:
		return redirect('tasks')

	user = authenticate(request, username='DemoUser', password='123456789Ss')
	login(request, user)
	return redirect('tasks')


def about_page(request):
	return render(request, 'core/about.html')
