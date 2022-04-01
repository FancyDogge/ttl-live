from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    #path('', frontpage, name='frontpage'),
    path('', include('apps.tasks.urls')),
    path('registration/', register_user, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', about_page, name='about'),
]