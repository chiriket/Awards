from django import forms
from .models import Profile, Reviews
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Profile

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'pub_date', 'profile']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ['image', 'user']