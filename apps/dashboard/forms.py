from django.forms import ModelForm
from core.models import Userprofile


class UpdateAvatar(ModelForm):
    class Meta:
        model = Userprofile
        fields = ['avatar']