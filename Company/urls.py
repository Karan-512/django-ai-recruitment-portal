from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.Home, name='company-home'),
    path('profile', views.Profile, name='company-profile'),
    path('job-post/', views.jobPosting, name='job-post'),
    path('view-applications/', views.ViewApplications, name='applications'),
]
