from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import Account



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=100, help_text='Required. Add a valid email address')
	is_admin=forms.BooleanField(required=False,widget=forms.CheckboxInput( attrs={'id': 'admin'}))
	is_employee=forms.BooleanField( required=False,widget=forms.CheckboxInput( attrs={'id': 'employee'}))
	is_contractor=forms.BooleanField(required=False, widget=forms.CheckboxInput( attrs={'id': 'contractor'}))



	class Meta:
		model = Account
		fields = ("email", "username", "password1", "password2","is_admin","is_contractor","is_employee")


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")