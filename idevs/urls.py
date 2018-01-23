from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('branch', views.branch, name='branch'),
    path('bus', views.bus, name='bus'),
    path('map', views.tline_map, name='tline_map'),

]
