from django.urls import path
from . import views

urlpatterns = [

    path('my-profile/', views.myProfile, name='js-my-profile'),
]
