import pandas as pd
import numpy as np
import Database
import Toolbox as tool

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.display.max_colwidth = 100


def get_numeric_data(filename):
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM ' + filename, Database.conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[:columns.index('PlayersBios_GP')], inplace=True)
        df.to_sql('Numeric_' + filename, Database.conn, if_exists='replace', index=False)
        print('Numeric_' + filename + ' inserted')
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM ' + filename, Database.conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['TeamsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[:columns.index('TeamsTraditionalStats_GP')], inplace=True)
        df.to_sql('Numeric_' + filename, Database.conn, if_exists='replace', index=False)
        print('Numeric_' + filename + ' inserted')
    else:
        query = pd.read_sql_query('SELECT * FROM ' + filename, Database.conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['LineupsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[:columns.index('LineupsTraditionalStats_GP')], inplace=True)
        df.to_sql('Numeric_' + filename, Database.conn, if_exists='replace', index=False)
        print('Numeric_' + filename + ' inserted')
    return


def get_non_numeric_data(filename):
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM ' + filename, Database.conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[columns.index('PlayersBios_GP'):], inplace=True)
        df.to_sql('NonNumeric_' + filename, Database.conn, if_exists='replace', index=False)
        print('NonNumeric_' + filename + ' inserted')
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM ' + filename, Database.conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['TeamsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[columns.index('TeamsTraditionalStats_GP'):], inplace=True)
        df.to_sql('NonNumeric_' + filename, Database.conn, if_exists='replace', index=False)
        print('NonNumeric_' + filename + ' inserted')
    else:
        query = pd.read_sql_query('SELECT * FROM ' + filename, Database.conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['LineupsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[columns.index('LineupsTraditionalStats_GP'):], inplace=True)
        df.to_sql('NonNumeric_' + filename, Database.conn, if_exists='replace', index=False)
        print('NonNumeric_' + filename + ' inserted')
    return


def clean_numeric_dataset(filename, missing_rate):
    query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, Database.conn)
    df = pd.DataFrame(query)
    duplicateColumnNames = []
    for x in range(df.shape[1]):  # Iterate over all the columns in dataframe
        col = df.iloc[:, x]  # Select column at xth index.
        for y in range(x + 1, df.shape[1]):  # Iterate over all the columns in DataFrame from (x+1)th index till end
            otherCol = df.iloc[:, y]  # Select column at yth index.
            if col.equals(otherCol):  # Check if two columns at x 7 y index are equal
                duplicateColumnNames.append(df.columns.values[y])
    df.drop(columns=duplicateColumnNames, inplace=True)
    df.dropna(axis=1, thresh=len(df) * missing_rate, inplace=True)
    df.fillna(0, inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    df[indices_to_keep].astype(np.float64)
    df.to_sql('Numeric_' + filename, Database.conn, if_exists='replace', index=False)
    print('Numeric_' + filename + ' cleaned')


def get_players_type(player_id, season):
    Database.conn.row_factory = lambda cursor, row: row[0]
    ty = Database.c.execute(
        'SELECT Type FROM PCA_Dataset_Players WHERE PlayersBios_Player_ID = "' + player_id +
        '" and PlayersBios_Season = "' + season + '"').fetchall()
    return tool.converttuple(ty[0])


def get_simple_player_type():
    df = pd.read_csv('../DB 100h Proj/PlayersType_simple.csv', sep=";")
    df.to_sql('Players_type_simple', Database.conn, if_exists='replace', index=False)
    return df



def get_lda_bests_lineups():
    df_simple = get_simple_player_type()
    df = pd.read_sql_query('SELECT * FROM LDA_Dataset_Lineups WHERE Class in ("Elite", "High average")', Database.conn)
    players_type = Database.c.execute('SELECT DISTINCT Cluster FROM PCA_Dataset_Players ORDER BY Type').fetchall()
    j = 0
    for i in players_type:
        players_type[j] = i[0]
        j += 1
    li = df['Ids'].to_list()
    ye = df['Season'].to_list()
    l = []
    for k in li:
        l.append([k])
    lineups = pd.DataFrame.from_records(l, columns=['Lineup'])
    lineups['Season'] = ye
    lineups[['P1', 'P2', 'P3', 'P4', 'P5']] = lineups.Lineup.str.split(", ", expand=True)
    lineups['Lineup Type'] = None
    for p in players_type:
        lineups['Type ' + str(p)] = 0
    lineups['Lineup Players'] = None
    col = list(lineups)[2:7]
    for index, row in lineups.iterrows():
        append_p_type = []
        append_p_simple_type = []
        for co in col:
            season = row['Season']
            player_id = row[co]
            p_type = get_players_type(player_id, season)
            append_p_type.append(p_type[0])
            append_p_type.sort()
            simple_type = df_simple['Type_name'].iloc[int(p_type[0])]
            append_p_simple_type.append(simple_type)
            append_p_simple_type.sort()
            lineups['Lineup Type'][index] = str(append_p_type).strip("[]").replace("'", "")
            lineups['Type ' + p_type[0]][index] = lineups['Type ' + p_type[0]][index] + 1
        simple_type = tool.count_element_list(append_p_simple_type)
        lineups['Lineup Players'][index] = str(simple_type).strip("[]").replace("'", "")
    lineups['CheckNbPlayer'] = lineups.sum(axis=1)
    lineups.drop(columns=['Type 7'], inplace=True)
    lineups_count = lineups.iloc[:, 7:16].groupby(lineups.iloc[:, 7:16].columns.tolist()).size().reset_index(
        name='Count')
    lineups_count.sort_values(by=['Count'], ascending=False, inplace=True)
    lineups_count.to_sql('Bests_Lineups_count', Database.conn, if_exists='replace', index=False)
    print('The bests lineups have been created')
