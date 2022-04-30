from django.forms import ModelForm
from dashboard.models import Userprofile


#-------Форма Аплоада Аватарки------
class UpdateAvatar(ModelForm):
    class Meta:
        model = Userprofile
        fields = ['avatar']