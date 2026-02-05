from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing_page, name='landing'),

    path('login/', views.login_view, name='login'),
    
    path('jobseeker/home/', views.jobseeker_home, name='jobseeker_home'),

    path('company/home/', views.company_home, name='company_home'),
]
