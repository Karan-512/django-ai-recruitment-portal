from django.urls import path
from . import views

urlpatterns = [

    path('my-profile/', views.myProfile, name='js-my-profile'),
    path('home/', views.Home, name='js-home'),
    path('job-detail/<int:pk>/', views.job_detail_page, name='js-job-detail'),
    path("api/dashboard-stats/", views.dashboard_stats, name="dashboard-stats"),
]