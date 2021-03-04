from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams_index, name='index'),
    path('stats/', views.stats, name='stats'),
    path('teams/roster/<int:team_id>/', views.roster, name='roster'),
    # FavList Paths
    path('favlist/create/', views.FavlistCreate.as_view(), name='favlist_create'),
    path('favlist/update/', views.FavlistUpdate.as_view(), name='favlist_update'),
    #path('favlist/delete/', views.FavlistDelete.as_view(), name='favlist_delete'),
    path('fav_lists/', views.favlist_List, name='favlist_index'),
    # everything below this line is Stuart’s new code
    
    path('players/<int:player_id>/', views.playerStats, name='playerStats'),
    
    # User signup URL
    path('accounts/signup/', views.signup, name='signup')
]
