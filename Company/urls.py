from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name='company-home'),
    path('profile', views.Profile, name='company-profile'),
    path('job-post/', views.jobPosting, name='job-post'),
    path('applications/', views.view_applications, name='applications'),
    path('job/<int:job_id>/applicants/',views.job_applicants,name='job_applicants'),
    path('api/jobs/', views.job_list_api),
    path('api/jobs/<int:job_id>/applicants/', views.job_applicants_api),
]

