# django needs to keep track of all the endpoints
from django.urls import path

# Get all the functionality to be executed upon reaching endpoint
from . import views

# All the endpoints with there respected view mappings.
urlpatterns = [
    path('', views.index, name='index'),
    path('automated_testing/', views.automate, name="automate"),
    path('statdisp/', views.stats_disp, name="hot"),
    path('statistics/', views.statistics, name='stats'),
    path('home/', views.home, name='home'),
    path('query/', views.query, name='testing_form'),
]