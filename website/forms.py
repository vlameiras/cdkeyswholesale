from django import forms
from django.forms import ModelForm
from website.models import Customer

class RegisterForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = Customer
		exclude = ('username', 'user','availableBalance','customerLevel','customerStatus')

class ProfileForm(forms.ModelForm):

	class Meta:
		model = Customer
		exclude = ('defaultCurrency','user', 'paypalAccount', 'iban', 'customerStatus', 'customerLevel', )
