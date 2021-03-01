from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('stats/', views.stats, name='stats'),
    path('teams/roster/<int:team_id>/', views.roster, name='roster')
]
