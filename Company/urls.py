from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name='company-home'),
    path('profile', views.Profile, name='company-profile'),
    path('job-post/', views.jobPosting, name='job-post'),
    path('view-applications/', views.view_applications, name='applications'),
    path('job/<int:job_id>/applicants/',views.job_applicants,name='job_applicants'),
    path('api/jobs/', views.job_list_api),
    path('api/jobs/<int:job_id>/applicants/', views.job_applicants_api),
    # path('view-applications/', views.ViewApplications, name='applications'),
    path('job-detail/<int:job_id>/', views.JobDetail, name='job_detail'),
    path('edit-job/<int:job_id>/', views.jobPosting, name='edit_job'),
    path('toggle-job/<int:job_id>/', views.ToggleJobStatus, name='toggle_job_status'),

    # for job seeker
    path('api/all-jobs/', views.get_jobs, name='get-jobs'),
    path("api/jobs/<int:pk>/", views.get_job_detail, name="get-job-detail"),
]
