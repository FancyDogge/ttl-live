from django.forms import ModelForm, ImageField
from dashboard.models import Userprofile


#-------Форма Аплоада Аватарки------
class UpdateAvatar(ModelForm):
    avatar = ImageField(required=True)
    class Meta:
        model = Userprofile
        fields = ['avatar',]