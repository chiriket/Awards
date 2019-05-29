from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile',blank=True, null=True)
    Bio = models.TextField(max_length = 50,null = True)
    profile_pic = models.ImageField(upload_to='profile/')
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles
    
    @classmethod
    def search_by_username(cls,search_term):
        profiles = cls.objects.filter(title__icontains=search_term)
        return profiles
    

    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    # screenshot = models.ImageField(upload_to = 'images/')
    project_name = models.CharField(max_length =10)
    project_url = models.CharField(max_length =50)
    # location = models.CharField(max_length =10)
    profile = models.ForeignKey(Profile, null = True,related_name='project')
    # pub_date = models.DateTimeField(auto_now_add=True, null=True)
    # user= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()
    
   
    
    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_profile(cls,search_term):
        projo = cls.objects.filter(profile__name__icontains=search_term)
        return projo

    @classmethod
    def get_profile_projects(cls, profile):
        project = Project.objects.filter(profile__pk = profile)
        return project

    @classmethod
    def find_project_id(cls, id):
        identity = Project.objects.get(pk=id)
        return identity

class Reviews(models.Model):
    comment = models.CharField(max_length = 300)
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments_by_projects(cls, id):
        comments = Comments.objects.filter(project__pk = id)
        return comments

# Create your models here.

class Rate(models.Model):
    design = models.CharField(max_length=30)
    usability = models.CharField(max_length=8)
    creativity = models.CharField(max_length=8,blank=True,null=True)
    average = models.FloatField(max_length=8)
    user = models.ForeignKey(User,null = True)
    project = models.ForeignKey(Project,related_name='rate',null=True)


    def __str__(self):
        return self.design

    class Meta:
        ordering = ['-id']

    def save_rate(self):
        self.save()

    @classmethod
    def get_rate(cls, profile):
        rate = Rate.objects.filter(Profile__pk = profile)
        return rate
    
    @classmethod
    def get_all_rating(cls):
        rating = Rate.objects.all()



