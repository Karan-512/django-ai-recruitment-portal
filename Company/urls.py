from django.urls import path
from Company import views

urlpatterns = [
    path('home/', views.Home, name='company-home'),
    path('profile', views.Profile, name='company-profile'),
    path('job-post/', views.jobPosting, name='job-post'),
    path('view-applications/', views.view_applications, name='applications'),
    path('api/jobs/', views.job_list_api),

    # for job seeker
    path('api/all-jobs/', views.get_jobs, name='get-jobs'),
    path('job-detail/<int:job_id>/', views.JobDetail, name='company_job_detail'),
    path('edit-job/<int:job_id>/', views.jobPosting, name='edit_job'),
    path('toggle-job/<int:job_id>/', views.ToggleJobStatus, name='toggle_job_status'),
    path("api/jobs/<int:pk>/", views.get_job_detail, name="get-job-detail"),

    #Company View Applicants
    path("job/<int:job_id>/applicants/", views.view_applicants, name="view_applicants"),
    path("applicant-profile/<int:job_id>/",views.applicant_profile,name="view-applicant-profile"),
]
