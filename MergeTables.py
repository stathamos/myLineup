import sqlite3
import pandas as pd
import Functions2 as f

conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v2.8.db')  # Connection / Creation of the DataBase
c = conn.cursor()
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
        left_index = [s for s in columns if "PLAYER_ID" in s]
        left_index.extend([s for s in columns if "Season" in s])
        left_index = ['P' + str(i) + '.' + col for col in left_index]
        i += 1
        print(str(i) + ' / ' + str(len(list_players)))
    else:
        query = pd.read_sql_query("SELECT * FROM " + x, conn)
        df = pd.DataFrame(query)
        columns = df.columns.to_list()
        right_index = [s for s in columns if "PLAYER_ID" in s]
        playtype_index = [s for s in columns if "TEAM_ID" in s]
        playtype_index = ['P' + str(i) + '.' + col for col in playtype_index]
        PlayersGeneralStatsDetailed_index = ['P' + str(i) + '.PlayersGeneralStatsDetailed_TEAM_ID']
        right_index.extend([s for s in columns if "Season" in s])
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
                        + right_index[2]
        i += 1
        print(str(i) + ' / ' + str(len(list_players)))
full_query = pd.read_sql_query(full_join, conn)
df = pd.DataFrame(full_query)
df.to_sql('Dataset_Players', conn, if_exists='append', index=False)

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
