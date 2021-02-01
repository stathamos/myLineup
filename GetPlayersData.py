import Functions2 as f

f.get_players_data('https://stats.nba.com/stats/leaguedashplayerbiostats', '')  # OK 1
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerstats', '')  # OK 2
f.get_players_data('https://stats.nba.com/stats/leagueplayerondetails', '')  # OK 3
f.get_players_data('https://stats.nba.com/stats/playerestimatedmetrics', '')  # OK 4
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerclutch', '')  # OK 5
f.get_players_data('https://stats.nba.com/stats/synergyplaytypes', '')  # OK 6
f.get_players_data('https://stats.nba.com/stats/leaguedashptstats', '')  # OK 7
f.get_players_data('https://stats.nba.com/stats/leaguedashptdefend', '')  # OK 8
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerptshot', 'GeneralRange')  # OK 9
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerptshot', 'DribbleRange')  # OK 10
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerptshot', 'TouchTimeRange')  # OK 11
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerptshot', 'CloseDefDistRange')  # OK 12
f.get_players_data('https://stats.nba.com/stats/leaguedashplayershotlocations', '')  # OK 13
f.get_players_data('https://stats.nba.com/stats/leaguehustlestatsplayer', '')  # OK 14

