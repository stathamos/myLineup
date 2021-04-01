import Database
import pandas as pd
import Functions2 as f


def merge_tables():
    """update_col_name = ['ALTER TABLE Players2ptsDefense RENAME COLUMN Players2ptsDefense_CLOSE_DEF_PERSON_ID to '
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
        Database.c.execute(i)
    Database.conn.commit()"""

    i = 0
    list_players = f.sql_column_to_list('player')
    full_join = 'SELECT * FROM PlayersBios P0'
    for x in list_players:
        if x == 'PlayersBios':
            print('Step over')
            query = pd.read_sql_query("SELECT * FROM " + x, Database.conn)
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
            query = pd.read_sql_query("SELECT * FROM " + x, Database.conn)
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
    full_query = pd.read_sql_query(full_join, Database.conn)
    df = pd.DataFrame(full_query)
    df.drop(['PlayersBios_Season', 'PlayersBios_SeasonType'], axis=1, inplace=True)
    df.insert(1, 'PlayersBios_Season', full_query['PlayersBios_Season'])
    df.insert(2, 'PlayersBios_SeasonType', full_query['PlayersBios_SeasonType'])
    df.to_sql('Dataset_Players', Database.conn, if_exists='replace', index=False)

    i = 0
    list_teams = f.sql_column_to_list('team')
    full_join = 'SELECT * FROM TeamsTraditionalStats T0'
    for x in list_teams:
        if x == 'TeamsTraditionalStats':
            print('Step over')
            query = pd.read_sql_query("SELECT * FROM " + x, Database.conn)
            df = pd.DataFrame(query)
            columns = df.columns.to_list()
            left_index = [s for s in columns if "TEAM_ID" in s]
            left_index.extend([s for s in columns if "Season" in s])
            left_index = ['T' + str(i) + '.' + col for col in left_index]
            i += 1
            print(str(i) + ' / ' + str(len(list_teams)))
        else:
            query = pd.read_sql_query("SELECT * FROM " + x, Database.conn)
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
    full_query = pd.read_sql_query(full_join, Database.conn)
    df = pd.DataFrame(full_query)
    df.drop(['TeamsTraditionalStats_Season', 'TeamsTraditionalStats_SeasonType'], axis=1, inplace=True)
    df.insert(1, 'TeamsTraditionalStats_Season', full_query['TeamsTraditionalStats_Season'])
    df.insert(2, 'TeamsTraditionalStats_SeasonType', full_query['TeamsTraditionalStats_SeasonType'])
    df.to_sql('Dataset_Teams', Database.conn, if_exists='replace', index=False)

    i = 0
    list_teams = f.sql_column_to_list('Lineup')
    full_join = 'SELECT * FROM LineupsTraditionalStats L0'
    for x in list_teams:
        if x == 'LineupsTraditionalStats':
            print('Step over')
            query = pd.read_sql_query("SELECT * FROM " + x, Database.conn)
            df = pd.DataFrame(query)
            columns = df.columns.to_list()
            left_index = [s for s in columns if "GROUP_ID" in s]
            left_index.extend([s for s in columns if "Season" in s])
            left_index = ['L' + str(i) + '.' + col for col in left_index]
            i += 1
            print(str(i) + ' / ' + str(len(list_teams)))
        else:
            query = pd.read_sql_query("SELECT * FROM " + x, Database.conn)
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
    full_query = pd.read_sql_query(full_join, Database.conn)
    df = pd.DataFrame(full_query)
    df.drop(['LineupsTraditionalStats_Season', 'LineupsTraditionalStats_SeasonType'], axis=1, inplace=True)
    df.insert(1, 'LineupsTraditionalStats_Season', full_query['LineupsTraditionalStats_Season'])
    df.insert(2, 'LineupsTraditionalStats_SeasonType', full_query['LineupsTraditionalStats_SeasonType'])
    df.to_sql('Dataset_Lineups', Database.conn, if_exists='replace', index=False)
