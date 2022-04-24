from django.forms import ModelForm
from dashboard.models import Userprofile


class UpdateAvatar(ModelForm):
    class Meta:
        model = Userprofile
        fields = ['avatar']