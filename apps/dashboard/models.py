from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#-------Профиль, в котором будет аватарка------
class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars', blank=False, null=False, default='uploads/avatars/default.jpg')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
#если создается юзер, создается и юзерпрофайл
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Userprofile(user=instance)
        user_profile.save()