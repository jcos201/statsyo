from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams_index, name='index'),
    path('stats/', views.stats, name='stats'),
    path('teams/roster/<int:team_id>/', views.roster, name='roster'),
    # FavList Paths
    path('favlist/create/', views.ListCreate.as_view(), name='favlist_create'),
    path('favlist/<int:pk>/update/', views.ListUpdate.as_view(), name='favlist_update'),
    path('favlist/<int:pk>/delete/', views.ListDelete.as_view(), name='favlist_delete'),
    path('favlist/<int:pk>/', views.ListDetail.as_view(), name='favlist_detail'),
    path('fav_lists/', views.favlist_List, name='favlist_index'),
    
    path('players/<int:player_id>/', views.playerStats, name='playerStats'),
    path('players/pitchers/<int:player_id>/', views.pitcherStats, name='pitcherStats'),
    
    # User signup URL
    path('accounts/signup/', views.signup, name='signup')
]