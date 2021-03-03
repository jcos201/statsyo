from django.shortcuts import render
import requests

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

def teams(request):
    teamsData = requests.get("http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2020'")
    team = teamsData.json()
    all_season = team['team_all_season']
    results = all_season['queryResults']

    return render(request, 'teams/index.html', {
        'teams': results['row']
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