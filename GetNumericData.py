import pandas as pd
import numpy as np
import sqlite3
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import sql
import itertools


pd.options.mode.chained_assignment = None  # default='warn'

conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.1.db')  # Connection / Creation of the DataBase
c = conn.cursor()
conn.commit()


def get_numeric_data(filename):
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM ' + filename, conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[:columns.index('PlayersBios_GP')], inplace=True)
        df.to_sql('Numeric_' + filename, conn, if_exists='replace', index=False)
        print('Numeric_' + filename + ' inserted')
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM ' + filename, conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['TeamsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[:columns.index('TeamsTraditionalStats_GP')], inplace=True)
        df.to_sql('Numeric_' + filename, conn, if_exists='replace', index=False)
        print('Numeric_' + filename + ' inserted')
    else:
        query = pd.read_sql_query('SELECT * FROM ' + filename, conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['LineupsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[:columns.index('LineupsTraditionalStats_GP')], inplace=True)
        df.to_sql('Numeric_' + filename, conn, if_exists='replace', index=False)
        print('Numeric_' + filename + ' inserted')
    return


def get_non_numeric_data(filename):
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM ' + filename, conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[columns.index('PlayersBios_GP'):], inplace=True)
        df.to_sql('NonNumeric_' + filename, conn, if_exists='replace', index=False)
        print('NonNumeric_' + filename + ' inserted')
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM ' + filename, conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['TeamsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[columns.index('TeamsTraditionalStats_GP'):], inplace=True)
        df.to_sql('NonNumeric_' + filename, conn, if_exists='replace', index=False)
        print('NonNumeric_' + filename + ' inserted')
    else:
        query = pd.read_sql_query('SELECT * FROM ' + filename, conn)
        df = pd.DataFrame(query)
        df = df.loc[(df['LineupsTraditionalStats_SeasonType'] == 'Regular Season')]
        columns = df.columns.to_list()
        df.drop(columns=columns[columns.index('LineupsTraditionalStats_GP'):], inplace=True)
        df.to_sql('NonNumeric_' + filename, conn, if_exists='replace', index=False)
        print('NonNumeric_' + filename + ' inserted')
    return


def clean_numeric_dataset(filename, missing_rate):
    query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, conn)
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
    df.to_sql('Numeric_' + filename, conn, if_exists='replace', index=False)
    print('Numeric_' + filename + ' cleaned')


def get_pca(filename, nb_of_components):
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, conn)
        name = pd.read_sql_query('SELECT PlayersBios_PLAYER_NAME, PlayersBios_PLAYER_ID, '
                                 'PlayersBios_Season FROM NonNumeric_'
                                 + filename, conn)
        df = pd.DataFrame(query)
        get_name = pd.DataFrame(name)
        col_name = 'PlayerName'
        ncluster = 7
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, conn)
        name = pd.read_sql_query('SELECT TeamsTraditionalStats_TEAM_NAME, TeamsTraditionalStats_TEAM_ID, '
                                 ' TeamsTraditionalStats_Season FROM NonNumeric_' + filename, conn)
        df = pd.DataFrame(query)
        get_name = pd.DataFrame(name)
        col_name = 'TeamName'
        ncluster = 4
    elif filename == 'Dataset_Lineups':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, conn)
        name = pd.read_sql_query('SELECT LineupsTraditionalStats_GROUP_NAME, '
                                 'LineupsTraditionalStats_GROUP_ID, LineupsTraditionalStats_Season FROM '
                                 'NonNumeric_' + filename, conn)
        df = pd.DataFrame(query)
        get_name = pd.DataFrame(name)
        col_name = 'LineupName'
        ncluster = 5
    X_std = StandardScaler().fit_transform(df)
    pca = PCA(n_components=nb_of_components)
    principalComponents = pca.fit_transform(X_std)
    PCA_components = pd.DataFrame(principalComponents)
    s = []
    for i in range(0, nb_of_components):
        s.append('PCA' + str(i + 1))
    PCA_components.columns = s
    model = KMeans(n_clusters=ncluster)
    model.fit(PCA_components.iloc[:, :nb_of_components])
    labels = model.predict(PCA_components.iloc[:, :nb_of_components])
    PCA_components['Cluster'] = labels
    if filename == 'Dataset_Players':
        PCA_components['SubCluster'] = None
        centroids_df2 = pd.DataFrame()
        for i in PCA_components['Cluster'].unique():
            PCA_components_w = PCA_components.loc[(PCA_components['Cluster'] == i)]
            model = KMeans(n_clusters=3)
            model.fit(PCA_components_w.iloc[:, :nb_of_components])
            labels = model.predict(PCA_components_w.iloc[:, :nb_of_components])
            centroids = model.cluster_centers_
            centroids_df = pd.DataFrame.from_records(centroids)
            centroids_df.columns = s
            centroids_df['Cluster'] = ncluster
            centroids_df['SubCluster'] = 3
            PCA_components_w['SubCluster'] = labels
            PCA_components['SubCluster'].loc[(PCA_components['Cluster'] == i)] = PCA_components_w['SubCluster']
            centroids_df2 = pd.concat([centroids_df2, centroids_df])
        centroids_df2.insert(0, 'PlayersBios_PLAYER_NAME', 'Centroid')
        centroids_df2.insert(1, 'PlayersBios_PLAYER_ID', 'Centroid')
        centroids_df2.insert(2, 'PlayersBios_Season', 'Centroid')
        PCA_components.insert(0, 'PlayersBios_PLAYER_NAME', get_name['PlayersBios_PLAYER_NAME'])
        PCA_components.insert(1, 'PlayersBios_PLAYER_ID', get_name['PlayersBios_PLAYER_ID'])
        PCA_components.insert(2, 'PlayersBios_Season', get_name['PlayersBios_Season'])
        PCA_components = pd.concat([PCA_components, centroids_df2])
        PCA_components['Type'] = PCA_components['Cluster'].astype(str) + ' - ' + PCA_components['SubCluster'].astype(
            str)
        PCA_components.to_sql('PCA_' + filename, conn, if_exists='replace', index=False)
    elif filename == 'Dataset_Teams':
        PCA_components.insert(0, 'TeamsTraditionalStats_TEAM_NAME', get_name['TeamsTraditionalStats_TEAM_NAME'])
        PCA_components.insert(1, 'TeamsTraditionalStats_TEAM_ID', get_name['TeamsTraditionalStats_TEAM_ID'])
        PCA_components.insert(2, 'TeamsTraditionalStats_Season', get_name['TeamsTraditionalStats_Season'])
        PCA_components.to_sql('PCA_' + filename, conn, if_exists='replace', index=False)
    elif filename == 'Dataset_Lineups':
        PCA_components['SubCluster'] = None
        centroids_df2 = pd.DataFrame()
        for i in PCA_components['Cluster'].unique():
            PCA_components_w = PCA_components.loc[(PCA_components['Cluster'] == i)]
            model = KMeans(n_clusters=3)
            model.fit(PCA_components_w.iloc[:, :nb_of_components])
            labels = model.predict(PCA_components_w.iloc[:, :nb_of_components])
            centroids = model.cluster_centers_
            centroids_df = pd.DataFrame.from_records(centroids)
            centroids_df.columns = s
            centroids_df['Cluster'] = ncluster
            centroids_df['SubCluster'] = 3
            PCA_components_w['SubCluster'] = labels
            PCA_components['SubCluster'].loc[(PCA_components['Cluster'] == i)] = PCA_components_w['SubCluster']
            centroids_df2 = pd.concat([centroids_df2, centroids_df])
        centroids_df2.insert(0, 'LineupsTraditionalStats_GROUP_NAME', 'Centroid')
        centroids_df2.insert(0, 'LineupsTraditionalStats_GROUP_ID', 'Centroid')
        centroids_df2.insert(0, 'LineupsTraditionalStats_Season', 'Centroid')
        PCA_components.insert(0, 'LineupsTraditionalStats_GROUP_NAME', get_name['LineupsTraditionalStats_GROUP_NAME'])
        PCA_components.insert(1, 'LineupsTraditionalStats_GROUP_ID', get_name['LineupsTraditionalStats_GROUP_ID'])
        PCA_components.insert(2, 'LineupsTraditionalStats_Season', get_name['LineupsTraditionalStats_Season'])
        PCA_components = pd.concat([PCA_components, centroids_df2])
        PCA_components['Type'] = PCA_components['Cluster'].astype(str) + ' - ' + PCA_components['SubCluster'].astype(
            str)
        PCA_components.to_sql('PCA_' + filename, conn, if_exists='replace', index=False)
    print('PCA_' + filename + ' Created')


def converttuple(tup):
    s = ''.join(tup)
    return s


def get_players_type(player_id, season):
    conn.row_factory = lambda cursor, row: row[0]
    type = c.execute('SELECT Type FROM PCA_Dataset_Players WHERE PlayersBios_Player_ID = "' + player_id + '" and PlayersBios_Season = "' + season + '"').fetchall()
    return converttuple(type[0])


def sql_query_to_list(query):
    conn.row_factory = sqlite3.Row
    list_of_tuple = c.execute(query).fetchall()
    li = []
    for i in list_of_tuple:
        li.append(i[0])
    return li


def combinliste(seq, k):
    p = []
    i, imax = 0, 2**len(seq)-1
    while i <= imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j <= jmax:
            if (i >> j) & 1 == 1:
                s.append(seq[j])
            j += 1
        if len(s) == k:
            p.append(s)
        i += 1
    return p


def listtostring(s):
    s.sort()
    str1 = ""
    for ele in s:
        str1 += ele + ', '
    return str1[:-2]


def get_bests_lineups():
    df = pd.read_sql_query('SELECT * FROM PCA_Dataset_Lineups', conn)
    conn.row_factory = lambda cursor, row: row[0]
    result = c.execute('SELECT B.Type from Dataset_Lineups A '
                       'JOIN PCA_Dataset_Lineups B on A.LineupsTraditionalStats_GROUP_NAME = '
                       'B.LineupsTraditionalStats_GROUP_NAME and A.LineupsTraditionalStats_GROUP_ID = '
                       'B.LineupsTraditionalStats_GROUP_ID and A.LineupsTraditionalStats_Season = '
                       'B.LineupsTraditionalStats_Season GROUP BY B.Type ORDER BY '
                       'avg(LineupsTraditionalStats_PLUS_MINUS) DESC LIMIT 2').fetchall()
    players_type = c.execute('SELECT DISTINCT Cluster FROM PCA_Dataset_Players ORDER BY Type')
    bl = pd.DataFrame()
    for i in result:
        bl = pd.concat([bl, df.loc[(df['Type'] == converttuple(i))]])
    li = bl['LineupsTraditionalStats_GROUP_ID'].to_list()
    ye = bl['LineupsTraditionalStats_Season'].to_list()
    l = []
    for k in li:
        l.append([k])
    lineups = pd.DataFrame.from_records(l, columns=['Lineup'])
    lineups['Season'] = ye
    lineups[['P1', 'P2', 'P3', 'P4', 'P5']] = lineups.Lineup.str.split(", ", expand=True)
    lineups['Lineup Type'] = None
    for p in players_type:
        lineups['Type ' + str(p[0])] = 0
    col = list(lineups)[2:7]
    for index, row in lineups.iterrows():
        append_p_type = []
        for co in col:
            season = row['Season']
            player_id = row[co]
            p_type = get_players_type(player_id, season)
            append_p_type.append(p_type[0])
            append_p_type.sort()
            lineups['Lineup Type'][index] = str(append_p_type).strip("[]").replace("'", "")
            lineups['Type ' + p_type[0]][index] = lineups['Type ' + p_type[0]][index] + 1
    lineups['CheckNbPlayer'] = lineups.sum(axis=1)
    lineups_count = lineups.iloc[:, 7:15].groupby(lineups.iloc[:, 7:15].columns.tolist()).size().reset_index(name='Count')
    lineups_count.sort_values(by=['Count'], ascending=False, inplace=True)
    lineups_count.to_sql('Bests_Lineups_count', conn, if_exists='replace', index=False)
    print('The bests lineups have been created')


def get_bests_lineups_detailed():
    df = pd.read_sql_query('SELECT * FROM PCA_Dataset_Lineups', conn)
    conn.row_factory = lambda cursor, row: row[0]
    result = c.execute('SELECT B.Type from Dataset_Lineups A '
                       'JOIN PCA_Dataset_Lineups B on A.LineupsTraditionalStats_GROUP_NAME = '
                       'B.LineupsTraditionalStats_GROUP_NAME and A.LineupsTraditionalStats_GROUP_ID = '
                       'B.LineupsTraditionalStats_GROUP_ID and A.LineupsTraditionalStats_Season = '
                       'B.LineupsTraditionalStats_Season GROUP BY B.Type ORDER BY '
                       'avg(LineupsTraditionalStats_PLUS_MINUS) DESC LIMIT 5').fetchall()
    players_type = c.execute('SELECT DISTINCT Type FROM PCA_Dataset_Players ORDER BY Type')
    bl = pd.DataFrame()
    for i in result:
        bl = pd.concat([bl, df.loc[(df['Type'] == converttuple(i))]])
    li = bl['LineupsTraditionalStats_GROUP_ID'].to_list()
    ye = bl['LineupsTraditionalStats_Season'].to_list()
    l = []
    for k in li:
        l.append([k])
    lineups = pd.DataFrame.from_records(l, columns=['Lineup'])
    lineups['Season'] = ye
    lineups[['P1', 'P2', 'P3', 'P4', 'P5']] = lineups.Lineup.str.split(", ", expand=True)
    lineups['Lineup Type'] = None
    for p in players_type:
        lineups['Type ' + str(converttuple(p))] = 0
    col = list(lineups)[2:7]
    for index, row in lineups.iterrows():
        append_p_type = []
        for co in col:
            season = row['Season']
            player_id = row[co]
            p_type = get_players_type(player_id, season)
            append_p_type.append(p_type)
            append_p_type.sort()
            lineups['Lineup Type'][index] = str(append_p_type).strip("[]").replace("'", "")
            lineups['Type ' + p_type][index] = lineups['Type ' + p_type][index] + 1
    lineups['CheckNbPlayer'] = lineups.sum(axis=1)
    lineups_count = lineups.iloc[:, 7:29].groupby(lineups.iloc[:, 7:29].columns.tolist()).size().reset_index(name='Count')
    lineups_count.sort_values(by=['Count'], ascending=False, inplace=True)
    lineups_count.to_sql('Bests_Lineups_count_detailed', conn, if_exists='replace', index=False)
    print('The bests lineups detailed have been created')


def get_players_with_type():
    df = pd.read_sql_query('SELECT P.PlayersBios_PLAYER_NAME, P.PlayersBios_PLAYER_ID, P.PlayersBios_Season, P.Type, '
                           'CAST(NP.PlayersBios_TEAM_ID as INT) as Team_ID FROM PCA_Dataset_Players P JOIN '
                           'NonNumeric_Dataset_Players NP on P.PlayersBios_PLAYER_ID = NP.PlayersBios_PLAYER_ID WHERE '
                           'P.PlayersBios_Season = "2020-21" and NP.PlayersBios_Season = "2020-21"', conn)
    df.to_sql('Players_with_type', conn, if_exists='replace', index=False)


def optimization_lineup():
    team_list = sql_query_to_list('SELECT TeamsTraditionalStats_TEAM_ID FROM NonNumeric_Dataset_Teams where '
                                  'TeamsTraditionalStats_Season = "2020-21" and TeamsTraditionalStats_SeasonType = '
                                  '"Regular Season"')
    minutes = [20, 10, 8, 5, 5]
    for i in team_list:
        bests_lineups = sql_query_to_list('select "Lineup Type" from Bests_Lineups_count')
        for k in range(len(bests_lineups)):
            bests_lineups[k] = bests_lineups[k].split(', ')
        df = pd.read_sql_query('SELECT * FROM Players_with_type WHERE Team_ID = "' + str(i) + '"', conn)
        combi = combinliste(df['Type'].astype(str).str[0].tolist(), 5)
        for j in range(0, len(combi)):
            combi[j].sort()
        combi_f = list()
        for sublist in combi:
            if sublist not in combi_f:
                combi_f.append(sublist)
        combi_f.sort()
        data_to_insert = pd.DataFrame()
        counter = 0
        for b in bests_lineups:
            if counter == 5:
                break
            else:
                for m in minutes:
                    if counter == 5:
                        break
                    else:
                        for c in combi_f:
                            if b == c:
                                lineup = []
                                lineup_with_player_id = []
                                for p in c:
                                    list_players_group_by = df['PlayersBios_PLAYER_NAME'].loc[(df['Type'].astype(str).str[0] ==
                                                                                               p[0])].to_list()
                                    lineup.append(list_players_group_by)
                                for p in c:
                                    list_players_id_group_by = df['PlayersBios_PLAYER_ID'].loc[(df['Type'].astype(str).str[0] ==
                                                                                                p[0])].to_list()
                                    lineup_with_player_id.append(list_players_id_group_by)
                                combi_lineup = [i for i in itertools.product(*lineup) if len(set(i)) == 5]
                                combi_lineup_with_id = [i for i in itertools.product(*lineup_with_player_id) if len(set(i)) == 5]
                                for j in range(0, len(combi_lineup)):
                                    combi_lineup[j] = list(combi_lineup[j])
                                for j in range(0, len(combi_lineup_with_id)):
                                    combi_lineup_with_id[j] = list(combi_lineup_with_id[j])
                                lineup_df = pd.DataFrame()
                                for j in range(0, len(combi_lineup_with_id)):
                                    combi_lineup_with_id[j].sort()
                                combi_lineup_with_id.sort()
                                combi_lineup_distinct_with_id = list()
                                for sublist in combi_lineup_with_id:
                                    if sublist not in combi_lineup_distinct_with_id:
                                        combi_lineup_distinct_with_id.append(sublist)
                                for j in combi_lineup_distinct_with_id:
                                    lineup_df = pd.concat([lineup_df,
                                                           pd.read_sql_query(sql.optimize(listtostring(j), m), conn)])
                                lineup_df['+/-'] = lineup_df['PTS'] - lineup_df['OPP_PTS']
                                data_to_insert = pd.concat([data_to_insert, lineup_df[lineup_df['+/-'] == lineup_df['+/-'].max()]])
                                counter += 1
                                break
                    # data_to_insert.to_sql('Optimized_lineups', conn, if_exists='append', index=False)


