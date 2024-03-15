from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'linkedin_password', 'indeed_password','profession', 'interests', 'location', 'resume', 'avatar']
