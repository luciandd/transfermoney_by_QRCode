from .models import Profile
from django import forms

	
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('id', 'id_auth_user', 'role', 'status', 'email', 'mobile_phone')