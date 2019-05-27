from django import forms
from .models import Image,Profile, Reviews
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ImageForm(forms.ModelForm):
   
    class Meta:
        model = Image
        exclude = ['likes', 'post_date', 'profile','user']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['image', 'user']