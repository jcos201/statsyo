from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams_index, name='index'),
    path('stats/', views.stats, name='stats'),
    path('teams/roster/<int:team_id>/', views.roster, name='roster'),
    path('favlist/create/', views.FavlistCreate.as_view(), name='favlist_create'),
    # everything below this line is Stuart’s new code
    
    path('players/<int:player_id>/', views.playerStats, name='playerStats'),
    
    # User signup URL
    path('accounts/signup/', views.signup, name='signup')
]
