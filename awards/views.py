from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
import datetime as dt
from .models import Project,Profile,Reviews
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db import models
from django.http import Http404

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Rest Api
# from .permissions import IsAdminOrReadOnly
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializer import ProjectSerializer,ProfileSerializer
# from rest_framework import status


def index(request):
    profile = Profile.objects.all()
    projects = Project.get_projects()
    form = ReviewForm()
    return render(request, 'index.html', {'projects':projects,"profile":profile, "form":form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Awards account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('index')
        return HttpResponse('Thank you for your email confirmation. Now you can now <a href="/accounts/login/">Login</a> your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def loader(request):
    return render(request, 'loader.html')

# def index(request):
#     date = dt.date.today()
#     photos = Project.objects.all()
#     # print(photos)
#     comm = ReviewForm()
#     profiles = Profile.objects.all()
#     # print(profiles)
#     form = ReviewForm()
#     return render(request, 'all-posts/index.html', {"date": date,"comm":comm, "photos":photos, "profiles":profiles, "form":form})

def new_project(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.profile = profile
            project.save()
        return redirect('index')

    else:
        form = ProjectForm()
    return render(request, 'new_project.html', {"form": form})
 
def edit_profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    posts = Project.objects.filter(user=current_user)
    if request.method == 'POST':
        signup_form = EditForm(request.POST, request.FILES,instance=request.user.profile) 
        if signup_form.is_valid():
            signup_form.save()
            return redirect('profile')
    else:
        signup_form =EditForm() 
        

    
    return render(request, 'profile/edit_profile.html', {"date": date, "form":signup_form,"profile":profile, "posts":posts})

def profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    posts = Project.objects.filter(user=current_user)
    return render(request, 'profile/profile.html', {"date": date, "profile":profile, "posts":posts})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username=search_term)
        message = f"{search_term}"
        profiles=  Profile.objects.all( )
        # profile = Profile.objects.get(user_id=id)
        # post=Project.objects.filter(user_id=id)
        return render(request, 'all-posts/search.html',{"message":message,"users": searched_users,'profiles':profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-posts/search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def review(request,image_id):
    #Getting comment form data
    image =  Project.objects.get(id=image_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
    return redirect('index')
# Create your views here.
