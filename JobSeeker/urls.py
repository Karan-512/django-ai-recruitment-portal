from django.urls import path
from . import views

urlpatterns = [

    path('my-profile/', views.my_profile, name='js-my-profile'),
    path('home/', views.Home, name='js-home'),
    path('job-detail/<int:pk>/', views.job_detail_page, name='js-job-detail'),
    path("api/dashboard-stats/", views.dashboard_stats, name="dashboard-stats"),
    path("my-applications/", views.MyApplications, name='js-my-applications'),
    path("api/my-applications/", views.get_my_applications, name="get-my-applications"),
    path("api/jobs/<int:pk>/apply/", views.apply_to_job, name="apply_to_job")
]