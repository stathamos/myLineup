import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
import sql
import datetime

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.display.max_colwidth = 100

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


def get_lda():
    query = pd.read_sql_query('SELECT * FROM Numeric_Dataset_Lineups', conn)
    name = pd.read_sql_query('SELECT LineupsTraditionalStats_GROUP_NAME, '
                             'LineupsTraditionalStats_GROUP_ID, LineupsTraditionalStats_Season FROM '
                             'NonNumeric_Dataset_Lineups', conn)
    query['Score'] = (query['LineupsTraditionalStats_PLUS_MINUS'] * query['LineupsTraditionalStats_GP']) / query[
        'LineupsTraditionalStats_MIN']
    l = []
    for i in query['Score'].to_list():
        if i >= 2:
            l.append('Elite')
        elif i >= 0:
            l.append('High average')
        elif i >= -2:
            l.append('Low average')
        else:
            l.append('Bad')
    query['Class'] = l
    query.insert(0, 'Names', name['LineupsTraditionalStats_GROUP_NAME'])
    query.insert(1, 'Ids', name['LineupsTraditionalStats_GROUP_ID'])
    query.insert(2, 'Season', name['LineupsTraditionalStats_Season'])
    query_num = query.iloc[:, 3:-1]
    query_score = query.iloc[:, -1:]
    query_num_np = query_num.to_numpy()
    query_score_np = query_score.to_numpy()
    query_score_np = query_score_np.reshape(len(query_score_np), )
    lda = LinearDiscriminantAnalysis(n_components=3)
    X_r2 = lda.fit(query_num_np, query_score_np).transform(query_num_np)
    LDA_components = pd.DataFrame.from_records(X_r2)
    LDA_components.rename(columns={0: 'LDA1', 1: 'LDA2', 2: 'LDA3'}, inplace=True)
    LDA_components.insert(0, 'Names', name['LineupsTraditionalStats_GROUP_NAME'])
    LDA_components.insert(1, 'Ids', name['LineupsTraditionalStats_GROUP_ID'])
    LDA_components.insert(2, 'Season', name['LineupsTraditionalStats_Season'])
    LDA_components['Class'] = l
    fig = px.scatter_3d(LDA_components, x=0, y=1, z=2, hover_name='Names', color='Class', opacity=0.5, size='Size')
    html_name = str(datetime.datetime.now()).replace(" ", "").replace("-", "").replace(":", "")[:12] + '_3D_LDA'
    plotly.offline.plot(fig, filename='../Graphs/' + html_name + '.html')
    LDA_components.to_sql('LDA_Dataset_Lineups', conn, if_exists='replace', index=False)
    print('LDA_Dataset_Lineups Created')


def converttuple(tup):
    s = ''.join(tup)
    return s


def get_players_type(player_id, season):
    conn.row_factory = lambda cursor, row: row[0]
    type = c.execute(
        'SELECT Type FROM PCA_Dataset_Players WHERE PlayersBios_Player_ID = "' + player_id + '" and PlayersBios_Season = "' + season + '"').fetchall()
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
    i, imax = 0, 2 ** len(seq) - 1
    while i <= imax:
        s = []
        j, jmax = 0, len(seq) - 1
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


def get_lda_bests_lineups():
    df = pd.read_sql_query('SELECT * FROM LDA_Dataset_Lineups WHERE Class in ("Elite", "High average")', conn)
    conn.row_factory = lambda cursor, row: row[0]
    players_type = c.execute('SELECT DISTINCT Cluster FROM PCA_Dataset_Players ORDER BY Type')
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
    lineups_count = lineups.iloc[:, 7:15].groupby(lineups.iloc[:, 7:15].columns.tolist()).size().reset_index(
        name='Count')
    lineups_count.sort_values(by=['Count'], ascending=False, inplace=True)
    lineups_count.to_sql('Bests_Lineups_count', conn, if_exists='replace', index=False)
    print('The bests lineups have been created')


def get_players_with_type():
    df = pd.read_sql_query('SELECT P.PlayersBios_PLAYER_NAME, P.PlayersBios_PLAYER_ID, P.PlayersBios_Season, P.Type, '
                           'CAST(NP.PlayersBios_TEAM_ID as INT) as Team_ID FROM PCA_Dataset_Players P JOIN '
                           'NonNumeric_Dataset_Players NP on P.PlayersBios_PLAYER_ID = NP.PlayersBios_PLAYER_ID WHERE '
                           'P.PlayersBios_Season = "2020-21" and NP.PlayersBios_Season = "2020-21"', conn)
    df.to_sql('Players_with_type', conn, if_exists='replace', index=False)


def get_distinct_list(li):
    for j in range(0, len(li)):
        li[j].sort()
    li_f = list()
    for sublist in li:
        if sublist not in li_f:
            li_f.append(sublist)
    li_f.sort()
    for j in range(0, len(li_f)):
        li_f[j].sort()
    return li_f


def get_teams_lineups():
    team_list = sql_query_to_list('SELECT TeamsTraditionalStats_TEAM_ID FROM NonNumeric_Dataset_Teams where '
                                  'TeamsTraditionalStats_Season = "2020-21" and TeamsTraditionalStats_SeasonType = '
                                  '"Regular Season"')
    for i in team_list:
        df = pd.read_sql_query('SELECT * FROM Players_with_type WHERE Team_ID = "' + str(i) + '"', conn)
        players_id = df['PlayersBios_PLAYER_ID'].to_list()
        players_name = df['PlayersBios_PLAYER_NAME'].to_list()
        lineups_id = combinliste(players_id, 5)
        lineups_name = combinliste(players_name, 5)
        lineups_name = [[x.replace("'", "") for x in l] for l in lineups_name]
        lineuptype = list()
        for p in lineups_id:
            l = list()
            for pid in p:
                p_type = df['Type'].astype(str).str[0].loc[(df['PlayersBios_PLAYER_ID'] == pid)].to_list()
                l.append(p_type[0])
            lineuptype.append(l)
        for j in range(0, len(lineuptype)):
            lineuptype[j].sort()
        team_lineups = pd.DataFrame()
        team_lineups['LineupName'] = lineups_name
        team_lineups['LineupName'] = team_lineups['LineupName'].str.join(', ')
        team_lineups['LineupID'] = lineups_id
        team_lineups['LineupID'] = team_lineups['LineupID'].str.join(', ')
        team_lineups['LineupType'] = lineuptype
        team_lineups['LineupType'] = team_lineups['LineupType'].str.join(', ')
        team_lineups['Team'] = i
        team_lineups.to_sql('Team_Lineups', conn, if_exists='append', index=False)
    print('All the teams lineups have been inserted')


def weighted_average(df, data_col, weight_col, by_col):
    df['_data_times_weight'] = df[data_col]*df[weight_col]
    df['_weight_where_notnull'] = df[weight_col]*pd.notnull(df[data_col])
    g = df.groupby(by_col)
    result = g['_data_times_weight'].sum() / g['_weight_where_notnull'].sum()
    del df['_data_times_weight'], df['_weight_where_notnull']
    return result.to_frame(name=data_col)


def get_players_boxscore(boxscore):
    boxscore.fillna(value=pd.np.nan, inplace=True)
    col = list(boxscore.columns.values)
    sum_col = col[1:6] + col[7:9] + col[10:12] + col[13:23] + col[34:43] + col[57:59] + col[60:62] + col[63:65]\
              + col[66:]
    mean_col = col[1:3] + col[23:34] + col[43:57]
    pct_col = [col[1]] + [col[6]] + [col[9]] + [col[12]] + [col[59]] + [col[62]] + [col[65]]
    summed_col = boxscore[sum_col].groupby('PlayerName').sum()
    weight_av = pd.DataFrame()
    for a in mean_col[2:]:
        wa = weighted_average(boxscore[mean_col], a, 'Min', 'PlayerName')
        weight_av[a] = wa[a]
    for a in pct_col[1:]:
        if a == 'FG_PCT':
            summed_col[a] = summed_col['FGM'] / summed_col['FGA']
        if a == 'FG3_PCT':
            summed_col[a] = summed_col['FG3M'] / summed_col['FG3A']
        if a == 'FT_PCT':
            summed_col[a] = summed_col['FTM'] / summed_col['FTA']
        if a == 'OPP_FG_PCT':
            summed_col[a] = summed_col['OPP_FGM'] / summed_col['OPP_FGA']
        if a == 'OPP_FG3_PCT':
            summed_col[a] = summed_col['OPP_FG3M'] / summed_col['OPP_FG3A']
        if a == 'OPP_FT_PCT':
            summed_col[a] = summed_col['OPP_FTM'] / summed_col['OPP_FTA']
    boxscore_players = pd.DataFrame(columns=col)
    summed_col[mean_col[2:]] = weight_av
    summed_col.insert(0, 'PlayersBios_TEAM_ABBREVIATION', boxscore.iloc[0][0])
    summed_col.insert(1, 'PlayerName', summed_col.index)
    boxscore_players = boxscore_players.append(summed_col, ignore_index=True)
    return boxscore_players


def optimized_stats_team(data_to_insert):
    col = list(data_to_insert.columns.values)
    serie_to_pivot = pd.Series([data_to_insert.iloc[0][0], 'Lineup'], index=col[:2])
    sum_col = col[3:7] + col[8:10] + col[11:13] + col[14:24] + col[35:44] + col[58:60] + col[61:63] + col[64:66] + col[67:]
    mean_col = col[24:35] + col[44:58]
    pct_col = [col[7]] + [col[10]] + [col[13]] + [col[60]] + [col[63]] + [col[66]]
    wa_serie = pd.Series([])
    pct_serie = pd.Series([])
    summed_col = data_to_insert[sum_col].sum()
    for a in mean_col:
        i = 0
        t = 0
        d = dict()
        while i < len(data_to_insert['Min']):
            t = t + data_to_insert['Min'].iloc[i] * data_to_insert[a].iloc[i]
            i += 1
        d[a] = t/48
        to_append = pd.Series(d)
        wa_serie = wa_serie.append(to_append)
    for a in pct_col:
        d = dict()
        if a == 'FG_PCT':
            d[a] = summed_col['FGM'] / summed_col['FGA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'FG3_PCT':
            d[a] = summed_col['FG3M'] / summed_col['FG3A']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'FT_PCT':
            d[a] = summed_col['FTM'] / summed_col['FTA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'OPP_FG_PCT':
            d[a] = summed_col['OPP_FGM'] / summed_col['OPP_FGA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'OPP_FG3_PCT':
            d[a] = summed_col['OPP_FG3M'] / summed_col['OPP_FG3A']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'OPP_FT_PCT':
            d[a] = summed_col['OPP_FTM'] / summed_col['OPP_FTA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
    serie_to_pivot = serie_to_pivot.append(pct_serie)
    serie_to_pivot = serie_to_pivot.append(summed_col)
    serie_to_pivot = serie_to_pivot.append(wa_serie)
    teams_compare = pd.DataFrame(columns=col)
    teams_compare = teams_compare.append(serie_to_pivot, ignore_index=True)
    return teams_compare


def optimization_lineup():
    team_list = sql_query_to_list('SELECT TeamsTraditionalStats_TEAM_ID FROM NonNumeric_Dataset_Teams where '
                                  'TeamsTraditionalStats_Season = "2020-21" and TeamsTraditionalStats_SeasonType = '
                                  '"Regular Season"')
    for t in team_list:
        optimization_lineup_by_team2(t)
    print('Teams lineups have been optimized')


def optimization_lineup_by_team(team_id):
    minutes = [13, 12, 11, 7, 5]
    bests_lineups = sql_query_to_list('select "Lineup Type" from Bests_Lineups_count')
    for k in range(len(bests_lineups)):
        bests_lineups[k] = bests_lineups[k].split(', ')
    df = pd.read_sql_query('SELECT * FROM Team_Lineups WHERE Team = "' + str(team_id) + '"', conn)
    combi = df['LineupType'].to_list()
    for k in range(len(combi)):
        combi[k] = combi[k].split(', ')
    for j in range(0, len(combi)):
        combi[j].sort()
    data_to_insert = pd.DataFrame()
    boxscore = pd.DataFrame()
    for m in minutes:
        done = False
        for b in bests_lineups:
            for c in combi:
                if b == c:
                    lineup_df = pd.DataFrame()
                    l_id = df['LineupID'].loc[(df['LineupType'] ==
                                               str(c).replace('[', '').replace(']', '').replace("'", ''))]
                    l_id = l_id.to_list()
                    if len(l_id) < 1:
                        break
                    for o in l_id:
                        lineup_df = pd.concat([lineup_df, pd.read_sql_query(sql.optimize(o, m), conn)])
                    lineup_df['+/-'] = lineup_df['PTS'] - lineup_df['OPP_PTS']
                    lineup_df.sort_values(['+/-'], ascending=False, inplace=True)
                    id_to_name = lineup_df['Lineup'].iloc[0]
                    names = df['LineupName'].loc[(df['LineupID'] == id_to_name)].to_string(index=False)
                    lineup_df.insert(2, 'LineupName', names)
                    data_to_insert = pd.concat([data_to_insert, lineup_df.nlargest(1, '+/-')])
                    data_to_insert.sort_values(['Min'], inplace=True)
                    bs = [i.split(', ') for i in data_to_insert['Lineup'].to_list()]
                    for p in bs[0]:
                        boxscore = pd.concat([boxscore, pd.read_sql_query(sql.optimize_players_stats(p, m), conn)])
                    df = df.loc[(df['LineupID'] != data_to_insert['Lineup'].to_list()[0])]
                    check = boxscore.groupby(['PlayerName'])[["Min", "PF"]].sum()
                    check['Count'] = boxscore.groupby(['PlayerName'])[["PlayerName"]].count()
                    if not check.loc[(check.Min > 36) | (check.PF > 6) | (check.Count > 4)].empty:
                        data_to_insert = data_to_insert.iloc[1:]
                        boxscore = boxscore.loc[(boxscore['Min'] != m)]
                        ind = m
                        break
                    done = True
                    break
            if done: break
    if ind != 6 and len(data_to_insert) < 5:
        for m in minutes[minutes.index(ind):]:
            done = False
            for b in bests_lineups:
                for c in combi:
                    if b == c:
                        lineup_df = pd.DataFrame()
                        l_id = df['LineupID'].loc[(df['LineupType'] ==
                                                   str(c).replace('[', '').replace(']', '').replace("'", ''))]
                        l_id = l_id.to_list()
                        if len(l_id) < 1:
                            break
                        for o in l_id:
                            lineup_df = pd.concat([lineup_df, pd.read_sql_query(sql.optimize(o, m), conn)])
                        lineup_df['+/-'] = lineup_df['PTS'] - lineup_df['OPP_PTS']
                        lineup_df.sort_values(['+/-'], inplace=True)
                        id_to_name = lineup_df['Lineup'].iloc[0]
                        names = df['LineupName'].loc[(df['LineupID'] == id_to_name)].to_string(index=False)
                        lineup_df.insert(2, 'LineupName', names)
                        data_to_insert = pd.concat([data_to_insert, lineup_df.nlargest(1, '+/-')])
                        data_to_insert.sort_values(['Min'], inplace=True)
                        bs = [i.split(', ') for i in data_to_insert['Lineup'].to_list()]
                        for p in bs[0]:
                            boxscore = pd.concat([boxscore, pd.read_sql_query(sql.optimize_players_stats(p, m), conn)])
                        df = df.loc[(df['LineupID'] != data_to_insert['Lineup'].to_list()[0])]
                        check = boxscore.groupby(['PlayerName'])[["Min", "PF"]].sum()
                        check['Count'] = boxscore.groupby(['PlayerName'])[["PlayerName"]].count()
                        if not check.loc[(check.Min > 38) | (check.PF > 6) | (check.Count > 4)].empty:
                            data_to_insert = data_to_insert.iloc[1:]
                            boxscore = boxscore.loc[(boxscore['Min'] != m)]
                            break
                        done = True
                        break
                if done: break
    teams_compare = optimized_stats_team(data_to_insert)
    boxscore_players = get_players_boxscore(boxscore)
    teams_compare.to_sql('Optimized_teams', conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized stats have been inserted')
    data_to_insert.to_sql('Optimized_lineups', conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized lineups have been inserted')
    boxscore_players.to_sql('Optimized_boxscores_lineups', conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized boxscores have been inserted')


def optimization_lineup_by_team2(team_id):
    minutes = [13, 12, 11, 7, 5]
    bests_lineups = sql_query_to_list('select "Lineup Type" from Bests_Lineups_count')
    for k in range(len(bests_lineups)):
        bests_lineups[k] = bests_lineups[k].split(', ')
    df = pd.read_sql_query('SELECT * FROM Team_Lineups WHERE Team = "' + str(team_id) + '"', conn)
    combi = df['LineupType'].to_list()
    for k in range(len(combi)):
        combi[k] = combi[k].split(', ')
    for j in range(0, len(combi)):
        combi[j].sort()
    data_to_insert = pd.DataFrame()
    boxscore = pd.DataFrame()
    for m in minutes:
        done = False
        for b in bests_lineups:
            for c in combi:
                if b == c:
                    lineup_df = pd.DataFrame()
                    l_id = df['LineupID'].loc[(df['LineupType'] ==
                                               str(c).replace('[', '').replace(']', '').replace("'", ''))]
                    l_id = l_id.to_list()
                    if len(l_id) < 1:
                        break
                    for o in l_id:
                        lineup_df = pd.concat([lineup_df, pd.read_sql_query(sql.optimize(o, m), conn)])
                    lineup_df['+/-'] = lineup_df['PTS'] - lineup_df['OPP_PTS']
                    z = 0
                    while z < len(lineup_df):
                        lineup_df.sort_values(['+/-'], ascending=False, inplace=True)
                        id_to_name = lineup_df['Lineup'].iloc[0]
                        names = df['LineupName'].loc[(df['LineupID'] == id_to_name)].to_string(index=False, length=False)
                        if z == 0:
                            lineup_df.insert(2, 'LineupName', names)
                        else:
                            lineup_df['LineupName'] = names
                        data_to_insert = pd.concat([data_to_insert, lineup_df.nlargest(1, '+/-')])
                        data_to_insert.sort_values(['Min'], inplace=True)
                        bs = [i.split(', ') for i in data_to_insert['Lineup'].to_list()]
                        for p in bs[0]:
                            boxscore = pd.concat([boxscore, pd.read_sql_query(sql.optimize_players_stats(p, m), conn)])
                        df = df.loc[(df['LineupID'] != data_to_insert['Lineup'].to_list()[0])]
                        check = boxscore.groupby(['PlayerName'])[["Min", "PF"]].sum()
                        check['Count'] = boxscore.groupby(['PlayerName'])[["PlayerName"]].count()
                        if data_to_insert.iloc[0][0] == 'CHA':
                            if not check.loc[(check.Min > 37) | (check.PF > 6) | (check.Count > 4)].empty:
                                data_to_insert = data_to_insert.iloc[1:]
                                lineup_df = lineup_df.iloc[1:]
                                boxscore = boxscore.loc[(boxscore['Min'] != m)]
                                z += 1
                                continue
                            done = True
                            break
                        elif not check.loc[(check.Min > 37) | (check.PF > 6) | (check.Count > 3)].empty:
                            data_to_insert = data_to_insert.iloc[1:]
                            lineup_df = lineup_df.iloc[1:]
                            boxscore = boxscore.loc[(boxscore['Min'] != m)]
                            z += 1
                            continue
                        done = True
                        break
                    break
            if done: break
    teams_compare = optimized_stats_team(data_to_insert)
    boxscore_players = get_players_boxscore(boxscore)
    teams_compare.to_sql('Optimized_teams2', conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized stats have been inserted')
    data_to_insert.to_sql('Optimized_lineups2', conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized lineups have been inserted')
    boxscore_players.to_sql('Optimized_boxscores_lineups2', conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized boxscores have been inserted')

