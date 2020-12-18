from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('apply', views.apply, name='apply'),
    path('logout', views.logout, name='logout'),
]
