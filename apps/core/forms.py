from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


#-------Форма Регистрации------
class RegisterForm(UserCreationForm):
	#email = forms.EmailField(required=True)
	def __init__(self, *args, **kwargs):
		#отключение подсказок в наследуемом классе
		super().__init__(*args, **kwargs)
		self.fields['password1'].help_text = None
		self.fields['password2'].help_text = None
		self.fields['username'].help_text = None

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")


#-------Форма Атуентификации------
class AuthForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].help_text = None
		self.fields['username'].help_text = None

	class Meta:
		model = User
		fields = ("username", "password")