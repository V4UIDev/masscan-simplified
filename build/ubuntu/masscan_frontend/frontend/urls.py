from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('help/', views.index, name='help'),
    path('about/', views.about, name='about')
]