import GetData as f
import GetNumericData as g
import Optimize as o
import GetGraphs as graphs
import MergeTables as merge
import PCA_LDA
import TableQuery as q


f.get_players_data('https://stats.nba.com/stats/leaguedashplayerbiostats', '')  # OK 1
f.get_players_data('https://stats.nba.com/stats/leaguedashplayerstats', '')  # OK 2
f.get_players_data('https://stats.nba.com/stats/leagueplayerondetails', '')  # OK 3
# f.get_players_data('https://stats.nba.com/stats/playerestimatedmetrics', '')  # OK 4
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

f.get_lineups_data('https://stats.nba.com/stats/leaguedashlineups')

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

merge.merge_tables()

f.clean_dataset('Players')
f.clean_dataset('Teams')
f.clean_dataset('Lineups')

g.get_numeric_data('Dataset_Players')
g.get_numeric_data('Dataset_Teams')
g.get_numeric_data('Dataset_Lineups')

g.get_non_numeric_data('Dataset_Players')
g.get_non_numeric_data('Dataset_Teams')
g.get_non_numeric_data('Dataset_Lineups')

g.clean_numeric_dataset('Dataset_Players', 0.8)
g.clean_numeric_dataset('Dataset_Teams', 0.8)
g.clean_numeric_dataset('Dataset_Lineups', 0.8)

PCA_LDA.get_pca('Dataset_Players', 30)
PCA_LDA.get_pca('Dataset_Teams', 10)
PCA_LDA.get_pca('Dataset_Lineups', 15)

PCA_LDA.get_lda()

graphs.scatter_3d('Dataset_Players', 0.2, 0.8, 0.7)
graphs.scatter_3d('Dataset_Teams', 0.2, 0.8, 0.7)
graphs.scatter_3d('Dataset_Lineups', 0.2, 0.8, 0.7)
graphs.plot_histo('Dataset_Players', 'exp_var', 30)
graphs.plot_histo('Dataset_Teams', 'exp_var', 30)
graphs.plot_histo('Dataset_Lineups', 'exp_var', 30)
graphs.plot_histo('Dataset_Players', 'nb_clus', 30)
graphs.plot_histo('Dataset_Teams', 'nb_clus', 30)
graphs.plot_histo('Dataset_Lineups', 'nb_clus', 30)


g.get_lda_bests_lineups()


o.get_players_with_type()

o.get_teams_lineups()

o.optimization_lineup()

o.get_type_description()

f.get_team_corres()

q.get_queries()
