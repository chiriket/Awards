from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
   url('^$',views.index, name = 'home'),
   url(r'^profile/$',views.profile,name='profile'),
   url(r'^search/', views.search_results, name='search_results'),
   url(r'^reviews/$',views.review,name = 'reviews'),
   url(r'^accounts/edit/',views.edit_profile, name='edit_profile'),
   url(r'^signup/$', views.signup, name='signup') 
  
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)