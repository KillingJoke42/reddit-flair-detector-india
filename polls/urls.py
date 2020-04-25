from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automated_testing/', views.automate, name="automate"),
    path('statdisp/', views.stats_disp, name="hot"),
    path('statistics/', views.statistics, name='stats'),
    path('home/', views.home, name='home'),
    path('query/', views.query, name='testing_form'),
]