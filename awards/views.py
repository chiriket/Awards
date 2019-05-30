from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
import datetime as dt
from .models import Project,Profile,Reviews
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db import models
from django.http import Http404
from .forms import ProjectForm,ProfileForm,ReviewForm

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def index(request):
    profile = Profile.objects.all()
    project = Project.objects.all()
    # project = Project.objects.filter(Profile__pk = profile)
    form = ReviewForm()
    return render(request, 'index.html', {'project':project,"profile":profile, "form":form})

@login_required(login_url='/accounts/login/')
def profile(request, username):
    projo = Project.objects.all()
    profile = User.objects.get(username=username)
    # print(profile.id)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    projo = Project.get_profile_projects(profile.id)
    title = f'@{profile.username} awwward projects and screenshots'

    return render(request, 'profile.html', locals())

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

# @login_required(login_url='/accounts/login')
def upload_project(request):
    if request.method == 'POST':
        uploadform = ProjectForm(request.POST, request.FILES)
        if uploadform.is_valid():
            upload = uploadform.save(commit=False)
            upload.profile = request.user.profile
            upload.save()
            return redirect('index')
    else:
        uploadform = ProjectForm()
    return render(request,'upload_project.html',locals())


def loader(request):
    return render(request, 'loader.html')

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

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile/edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})


def view_project(request):
    project = Project.objects.get_all()
    return render(request,'home.html', locals())

@login_required(login_url='/accounts/login/')
def vote(request,project_id):
   try:
       project = Project.objects.get(pk=project_id)
       rate = Rate.objects.filter(project_id=project_id).all()
       print([r.project_id for r in rate])
       rateform = RateForm()
   except DoesNotExist:
       raise Http404()
   return render(request,"project.html", locals())


@login_required(login_url='/accounts/login')
def rate_project(request,project_id):
    project = Project.objects.get(pk=project_id)
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        rateform = RateForm(request.POST, request.FILES)
        print(rateform.errors)
        if rateform.is_valid():
            rating = rateform.save(commit=False)
            rating.project = project
            rating.user = request.user
            rating.save()
            return redirect('vote',project_id)
    else:
        rateform = RateForm()
    return render(request,'rate.html',locals())