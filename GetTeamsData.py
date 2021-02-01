import Functions2 as f

f.get_teams_data('https://stats.nba.com/stats/leaguedashteamstats', '')  # 1 OK
f.get_teams_data('https://stats.nba.com/stats/teamestimatedmetrics', '')  # 2 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashteamclutch', '')  # 3 OK
f.get_teams_data('https://stats.nba.com/stats/synergyplaytypes', '')  # 4 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashptstats', '')  # 5 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashptteamdefend', '')  # 6 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashteamptshot', 'GeneralRange')  # 7 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashteamptshot', 'DribbleRange')  # 8 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashteamptshot', 'TouchTimeRange')  # 9 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashteamptshot', 'CloseDefDistRange')  # 10 OK
f.get_teams_data('https://stats.nba.com/stats/leaguedashteamshotlocations', '')  # 11 OK
f.get_teams_data('https://stats.nba.com/stats/leaguehustlestatsteam', '')  # 12 OK

