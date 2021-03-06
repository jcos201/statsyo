from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

import requests


# Imports for creating User Signup Page
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Imports login_required decorator for custom defined views
from django.contrib.auth.decorators import login_required

# Imports LoginRequiredMixin for class based views
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Fav_List, Fav_Player, Fav_Team

def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
        else:
            error_message = 'The data you have entered is invalide, please try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'home.html')

def stats(request):
    playerData = requests.get("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='cespedes%25'")
    player = playerData.json()
    search = player['search_player_all']
    query = search['queryResults']
    row = query['row']

    

    
    return render(request, 'stats.html', {
        'name': row['name_display_first_last'],
        'position': row['position'],
        'team': row['team_full'],
        # 'players': rosterResults['row']

    })

def teams_index(request):
    teamsData = requests.get("http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2020'")
    team = teamsData.json()
    all_season = team['team_all_season']
    results = all_season['queryResults']

    return render(request, 'teams/index.html', {
        'teams': results['row'],
        
    })


def roster(request, team_id):
    # teamsData = requests.get("http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2020'")
    # team = teamsData.json()
    # all_season = team['team_all_season']
    # results = all_season['queryResults']
    
    rosterData = requests.get("http://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id='{}'".format(team_id))
    teamRoster = rosterData.json()
    roster = teamRoster['roster_40']
    rosterResults = roster['queryResults']
    row = rosterResults['row']
    

    

    return render(request, 'teams/detail.html', {
        'players': rosterResults['row'],
        'team': row[0]['team_name']

    })


# Everything under this line is Stuart's new code:
def playerStats(request, player_id):
    playerData = requests.get("http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2020'&player_id='{}'".format(player_id))
    hittingResults = playerData.json()
    hitting = hittingResults['sport_hitting_tm']
    results = hitting['queryResults']

    return render(request, 'players/detail.html', {
        'stats': results['row']
        
    })




##### Authorization 

class ListCreate(LoginRequiredMixin, CreateView):
    model = Fav_List
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    #success_url = '/fav_lists'

class ListUpdate(LoginRequiredMixin, UpdateView):
    model = Fav_List

class ListDelete(LoginRequiredMixin, DeleteView):
    model = Fav_List

    success_url = '/fav_lists/'

class ListDetail(LoginRequiredMixin, DetailView):
    model = Fav_List

def favlist_List(request):
    list = Fav_List.objects.filter(user=request.user)
<<<<<<< HEAD
    return render(request, 'main_app/fav_list_list.html', { 'list': list })
=======
    return render(request, 'main_app/fav_list_list.html', { 'lists': list })
>>>>>>> 433ad561c43272aeb6578d9c82bfd6c53b989db5
