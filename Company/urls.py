from django.urls import path
from . import views

urlpatterns = [

    path('home/', views.Home, name='company-home'),
]
