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
    
    teamData = requests.get("http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season='2020'")
    team = teamData.json()
    


    
    return render(request, 'stats.html', {
        'name': row['name_display_first_last'],
        'position': row['position'],
        'team': row['team_full'],
        'teamPh': team['team_all_season']


    })

