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

@login_required
def roster(request, team_id):
    rosterData = requests.get("http://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id='{}'".format(team_id))
    teamRoster = rosterData.json()
    roster = teamRoster['roster_40']
    rosterResults = roster['queryResults']
    row = rosterResults['row']
    user = request.user
    favs = user.fav_list_set.first().fav_player_set.all().values_list('player_id', flat=True)
    
    return render(request, 'teams/detail.html', {
        'players': rosterResults['row'],
        'team': row[0]['team_name'],
        'team_logo': row[0]['team_abbrev'],
        'fav_players': favs
    })
#user.fav_list_set.first().fav_player_set.all().values_list('player_id', flat=True)

def playerStats(request, player_id):
    playerData = requests.get("http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2020'&player_id='{}'".format(player_id))
    hittingResults = playerData.json()
    hitting = hittingResults['sport_hitting_tm']
    results = hitting['queryResults']

    playerInfo = requests.get("http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{}'".format(player_id))
    nameLookup = playerInfo.json()
    info = nameLookup['player_info']
    infoResults = info['queryResults']

    if 'row' in results:
        return render(request, 'players/detail.html', {
            'stats': results['row'],
            'playerDetails': infoResults['row']
        })
    else:
        return render(request, 'players/detail.html', {
            'playerDetails': infoResults['row']
        })

def pitcherStats(request, player_id):
    pitcherData = requests.get("http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam?league_list_id='mlb'&game_type='R'&season='2020'&player_id='{}'".format(player_id))
    pitchingResults = pitcherData.json()
    pitching = pitchingResults['sport_pitching_tm']
    pitchResults = pitching['queryResults']

    playerInfo = requests.get("http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{}'".format(player_id))
    nameLookup = playerInfo.json()
    info = nameLookup['player_info']
    infoResults = info['queryResults']

    if 'row' in pitchResults:
        return render(request, 'players/pitchers.html', {
            'pitcherStats': pitchResults['row'],
            'playerDetails': infoResults['row']
        })
    else:
        return render(request, 'players/pitchers.html', {
            'playerDetails': infoResults['row']
        })

def battingLeaders(request, year):
    bLeaderData = requests.get("http://lookup-service-prod.mlb.com/json/named.leader_hitting_repeater.bam?sport_code=%27mlb%27&results=10&game_type=%27R%27&season='{}'&sort_column=%27hr%27&leader_hitting_repeater.col_in=name_display_first_last,hr,team_abbrev,avg,rbi,h,sb,player_id".format(year))
    bLeaderResults = bLeaderData.json()
    hitting_repeater = bLeaderResults['leader_hitting_repeater']

    return render(request, 'players/battingLeaders.html', {
        'bLeaders': hitting_repeater['leader_hitting_mux'],
        'year':year
    })

def pitchingLeaders(request, year):
    pLeaderData = requests.get("http://lookup-service-prod.mlb.com/json/named.leader_pitching_repeater.bam?sport_code='mlb'&results=10&game_type='R'&season='{}'&sort_column='era'&leader_pitching_repeater.col_in=name_display_first_last,era,team_abbrev".format(year))
    pLeaderResults = pLeaderData.json()
    pitching_repeater = pLeaderResults['leader_pitching_repeater']

    return render(request, 'players/pitchingLeaders.html', {
        'eraLeaders': pitching_repeater['leader_pitching_mux'],
        'year':year
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

class FavPlayerDelete(LoginRequiredMixin, DeleteView):
    model = Fav_Player
    
    success_url = '/fav_lists/'

@login_required
def favlist_List(request):
    lists = Fav_List.objects.filter(user=request.user)
    return render(request, 'main_app/fav_list_list.html', { 'lists': lists })


@login_required
def add_player(request, list_id, player_id):
    playerInfo = requests.get("http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{}'".format(player_id))
    nameLookup = playerInfo.json()
    info = nameLookup['player_info']
    infoResults = info['queryResults']
    details = infoResults['row']
    position = details['primary_position_txt']
    team = details['team_abbrev']
    name = details['name_display_first_last']

    Fav_Player.objects.create(player_id=player_id, fav_list_id=list_id, pos=position, team=team, name=name)
    lists = Fav_List.objects.filter(user=request.user)
    return redirect('favlist_detail', pk = list_id)
    