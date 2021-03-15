import Functions2 as f
import sqlite3
import pandas as pd
import GetNumericData as g


"""f.get_players_data('https://stats.nba.com/stats/leaguedashplayerbiostats', '')  # OK 1
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

conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.0.db')  # Connection / Creation of the DataBase
c = conn.cursor()
update_col_name = ['ALTER TABLE Players2ptsDefense RENAME COLUMN Players2ptsDefense_CLOSE_DEF_PERSON_ID to '
                   'Players2ptsDefense_CLOSE_DEF_PLAYER_ID;',
                   'ALTER TABLE Players3ptsDefense RENAME COLUMN '
                   'Players3ptsDefense_CLOSE_DEF_PERSON_ID to '
                   'Players3ptsDefense_CLOSE_DEF_PLAYER_ID;',
                   'ALTER TABLE PlayersFarFromBasketDefense RENAME COLUMN '
                   'PlayersFarFromBasketDefense_CLOSE_DEF_PERSON_ID to '
                   'PlayersFarFromBasketDefense_CLOSE_DEF_PLAYER_ID;',
                   'ALTER TABLE PlayersOutsidePaintDefense RENAME COLUMN '
                   'PlayersOutsidePaintDefense_CLOSE_DEF_PERSON_ID  to '
                   'PlayersOutsidePaintDefense_CLOSE_DEF_PLAYER_ID;',
                   'ALTER TABLE PlayersPaintDefense RENAME COLUMN PlayersPaintDefense_CLOSE_DEF_PERSON_ID to '
                   'PlayersPaintDefense_CLOSE_DEF_PLAYER_ID; ']
for i in update_col_name:
    c.execute(i)
conn.commit()

i = 0
list_players = f.sql_column_to_list('player')
full_join = 'SELECT * FROM PlayersBios P0'
for x in list_players:
    if x == 'PlayersBios':
        print('Step over')
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        columns = [w.replace('PERSON_ID', 'PLAYER_ID') for w in columns]
        left_index = [s for s in columns if "PLAYER_ID" in s]
        left_index.extend([s for s in columns if "Season" in s])
        left_index.extend([s for s in columns if "TEAM_ID" in s])
        left_index = ['P' + str(i) + '.' + col for col in left_index]
        i += 1
        print(str(i) + ' / ' + str(len(list_players)))
    else:
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        columns = [w.replace('PERSON_ID', 'PLAYER_ID') for w in columns]
        right_index = [s for s in columns if "PLAYER_ID" in s]
        playtype_index = [s for s in columns if "TEAM_ID" in s]
        playtype_index = ['P' + str(i) + '.' + col for col in playtype_index]
        PlayersGeneralStatsDetailed_index = ['P' + str(i) + '.PlayersGeneralStatsDetailed_TEAM_ID']
        right_index.extend([s for s in columns if "Season" in s])
        right_index.extend([s for s in columns if "TEAM_ID" in s])
        right_index = ['P' + str(i) + '.' + col for col in right_index]
        if "Playtypes" in x:
            full_join = full_join + ' \nLEFT JOIN ' + x + ' P' + str(i) + ' on ' + left_index[0] + ' = ' + right_index[
                0] + \
                        ' and ' + left_index[1] + ' = ' + right_index[1] + ' and ' + left_index[2] + ' = ' \
                        + right_index[2] + ' and ' + 'P0.PlayersBios_TEAM_ID = ' + playtype_index[0]
        elif "PlayersGeneralStatsDetailed" in x:
            full_join = full_join + ' \nLEFT JOIN ' + x + ' P' + str(i) + ' on ' + left_index[0] + ' = ' + right_index[
                0] + \
                        ' and ' + left_index[1] + ' = ' + right_index[1] + ' and ' + left_index[2] + ' = ' \
                        + right_index[2] + ' and ' + 'P0.PlayersBios_TEAM_ID = ' + PlayersGeneralStatsDetailed_index[0]
        else:
            full_join = full_join + ' \nLEFT JOIN ' + x + ' P' + str(i) + ' on ' + left_index[0] + ' = ' + right_index[
                0] + \
                        ' and ' + left_index[1] + ' = ' + right_index[1] + ' and ' + left_index[2] + ' = ' \
                        + right_index[2] + ' and ' + left_index[3] + ' = ' \
                        + right_index[3]
        i += 1
        print(str(i) + ' / ' + str(len(list_players)))
full_query = pd.read_sql_query(full_join, conn)
df = pd.DataFrame(full_query)
df.to_sql('Dataset_Players', conn, if_exists='replace', index=False)

i = 0
list_teams = f.sql_column_to_list('team')
full_join = 'SELECT * FROM TeamsTraditionalStats T0'
for x in list_teams:
    if x == 'TeamsTraditionalStats':
        print('Step over')
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        left_index = [s for s in columns if "TEAM_ID" in s]
        left_index.extend([s for s in columns if "Season" in s])
        left_index = ['T' + str(i) + '.' + col for col in left_index]
        i += 1
        print(str(i) + ' / ' + str(len(list_teams)))
    else:
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        right_index = [s for s in columns if "TEAM_ID" in s]
        right_index.extend([s for s in columns if "Season" in s])
        right_index = ['T' + str(i) + '.' + col for col in right_index]
        full_join = full_join + ' \nJOIN ' + x + ' T' + str(i) + ' on ' + left_index[0] + ' = ' + right_index[0] + \
                    ' and ' + left_index[1] + ' = ' + right_index[1] + ' and ' + left_index[2] + ' = ' \
                    + right_index[2]
        i += 1
        print(str(i) + ' / ' + str(len(list_teams)))
full_query = pd.read_sql_query(full_join, conn)
df = pd.DataFrame(full_query)
df.to_sql('Dataset_Teams', conn, if_exists='append', index=False)

i = 0
list_teams = f.sql_column_to_list('Lineup')
full_join = 'SELECT * FROM LineupsTraditionalStats L0'
for x in list_teams:
    if x == 'LineupsTraditionalStats':
        print('Step over')
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        left_index = [s for s in columns if "GROUP_ID" in s]
        left_index.extend([s for s in columns if "Season" in s])
        left_index = ['L' + str(i) + '.' + col for col in left_index]
        i += 1
        print(str(i) + ' / ' + str(len(list_teams)))
    else:
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        right_index = [s for s in columns if "GROUP_ID" in s]
        right_index.extend([s for s in columns if "Season" in s])
        right_index = ['L' + str(i) + '.' + col for col in right_index]
        full_join = full_join + ' \nJOIN ' + x + ' L' + str(i) + ' on ' + left_index[0] + ' = ' + right_index[0] + \
                    ' and ' + left_index[1] + ' = ' + right_index[1] + ' and ' + left_index[2] + ' = ' \
                    + right_index[2]
        i += 1
        print(str(i) + ' / ' + str(len(list_teams)))
full_query = pd.read_sql_query(full_join, conn)
df = pd.DataFrame(full_query)
df.to_sql('Dataset_Lineups', conn, if_exists='append', index=False)

f.clean_dataset('Players')
f.clean_dataset('Teams')
f.clean_dataset('Lineups')


conn2 = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.1.db')  # Creation of new database that will have only the 3 datasets
c2 = conn2.cursor()  # the db will be "lighter"
conn2.commit()

query_players = pd.read_sql_query('SELECT * FROM Dataset_Players_2', conn)  # Get players stats
query_teams = pd.read_sql_query('SELECT * FROM Dataset_Teams_2', conn)  # Get teams stats
query_lineups = pd.read_sql_query('SELECT * FROM Dataset_Lineups_2', conn)  # Get lineups stats

df_players = pd.DataFrame(query_players)  # convert the query into a dataframe
df_players = df_players[['PlayersBios_Season', 'PlayersBios_SeasonType'] +
                        [c for c in df_players if c not in ['PlayersBios_Season', 'PlayersBios_SeasonType']]]
df_teams = pd.DataFrame(query_teams)  # convert the query into a dataframe
df_teams = df_teams[['TeamsTraditionalStats_Season', 'TeamsTraditionalStats_SeasonType'] +
                    [c for c in df_teams if c not in ['TeamsTraditionalStats_Season',
                                                      'TeamsTraditionalStats_SeasonType']]]
df_lineups = pd.DataFrame(query_lineups)  # convert the query into a dataframe
df_lineups = df_lineups[['LineupsTraditionalStats_Season', 'LineupsTraditionalStats_SeasonType'] +
                        [c for c in df_lineups if c not in ['LineupsTraditionalStats_Season',
                                                            'LineupsTraditionalStats_SeasonType']]]

df_players.to_sql('Dataset_Players', conn2, if_exists='replace', index=False)  # insert dataframe into new db
print('Dataset Players cleaned')
df_teams.to_sql('Dataset_Teams', conn2, if_exists='replace', index=False)
print('Dataset Teams cleaned')
df_lineups.to_sql('Dataset_Lineups', conn2, if_exists='replace', index=False)
print('Dataset Lineups cleaned')

c2.execute('CREATE INDEX "Index_Dataset_Players" ON "Dataset_Players" ("PlayersBios_PLAYER_ID"	ASC, '
           '"PlayersBios_Season" ASC, "PlayersBios_SeasonType"	ASC);')
c2.execute('CREATE INDEX "Index_Dataset_Teams" ON "Dataset_Teams" ("TeamsTraditionalStats_TEAM_ID"	ASC, '
           '"TeamsTraditionalStats_Season" ASC, "TeamsTraditionalStats_SeasonType"	ASC);')
c2.execute('CREATE INDEX "Index_Dataset_Lineups" ON "Dataset_Lineups" ("LineupsTraditionalStats_PLAYER_ID"	ASC, '
           '"LineupsTraditionalStats_Season" ASC, "LineupsTraditionalStats_SeasonType"	ASC);')"""

"""g.get_numeric_data('Dataset_Players')
g.get_numeric_data('Dataset_Teams')
g.get_numeric_data('Dataset_Lineups')

g.get_non_numeric_data('Dataset_Players')
g.get_non_numeric_data('Dataset_Teams')
g.get_non_numeric_data('Dataset_Lineups')

g.clean_numeric_dataset('Dataset_Players', 0.8)
g.clean_numeric_dataset('Dataset_Teams', 0.8)
g.clean_numeric_dataset('Dataset_Lineups', 0.8)"""

"""g.get_pca('Dataset_Players', 30)
g.get_pca('Dataset_Teams', 10)
g.get_pca('Dataset_Lineups', 15)"""

"""g.scatter_3d('Dataset_Players', 0.2, 0.8, 0.7, 'test_p3d')
g.scatter_3d('Dataset_Teams', 0.2, 0.8, 0.7, 'test_t3d')
g.scatter_3d('Dataset_Lineups', 0.2, 0.8, 0.7, 'test_l3d')"""

"""g.get_bests_lineups_detailed()"""

"""g.get_bests_lineups()"""

"""g.get_players_with_type()"""

g.optimization_lineup()
