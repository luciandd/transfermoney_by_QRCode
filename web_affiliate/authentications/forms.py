from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				print("This user does not exist")
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				print("Incorect Password")
				raise forms.ValidationError("Incorect Password")
			if not user.is_active:
				print("This user is not longer active")
				raise forms.ValidationError("This user is not longer active")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	# address = forms.CharField()

	class Meta:
		model = User
		fields = ('username', 'password', 'first_name')