import pandas as pd
import numpy as np
import sqlite3
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly

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


def scatter_3d(filename, size_pop, size_centroid, opac, html_name):
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM PCA_' + filename, conn)
        df = pd.DataFrame(query)
        col_name = 'PlayerName'
        type = 'Type'
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM PCA_' + filename, conn)
        df = pd.DataFrame(query)
        col_name = 'TeamName'
        type = 'Cluster'
    elif filename == 'Dataset_Lineups':
        query = pd.read_sql_query('SELECT * FROM PCA_' + filename, conn)
        df = pd.DataFrame(query)
        col_name = 'LineupName'
        type = 'Type'
    df['Size'] = None
    df['Size'].loc[(df[col_name] == 'Centroid')] = size_centroid
    df['Size'].loc[(df[col_name] != 'Centroid')] = size_pop
    si = df['Size'].to_list()
    fig = px.scatter_3d(df,
                        x='PCA1',
                        y='PCA2',
                        z='PCA3',
                        color=type,
                        hover_name=col_name,
                        opacity=opac,
                        size=si)
    return plotly.offline.plot(fig, filename='../Graphs/' + html_name + '.html')


def convertTuple(tup):
    s = ''.join(tup)
    return s


def get_bests_lineups():
    df = pd.read_sql_query('SELECT * FROM PCA_Dataset_Lineups', conn)
    conn.row_factory = lambda cursor, row: row[0]
    result = c.execute('SELECT B.Type from Dataset_Lineups A JOIN PCA_Dataset_Lineups B on '
                       'A.LineupsTraditionalStats_GROUP_NAME = B.LineupsTraditionalStats_GROUP_NAME and '
                       'A.LineupsTraditionalStats_GROUP_ID = B.LineupsTraditionalStats_GROUP_ID and '
                       'A.LineupsTraditionalStats_Season = B.LineupsTraditionalStats_Season GROUP BY B.Type ORDER BY '
                       'avg(LineupsTraditionalStats_PLUS_MINUS) DESC LIMIT 4').fetchall()
    bl = pd.DataFrame()
    for i in result:
        j = convertTuple(i)
        bl = pd.concat([bl, df.loc[(df['Type'] == j)]])
    li = bl['LineupsTraditionalStats_GROUP_ID'].to_list()
    ye = bl['LineupsTraditionalStats_Season'].to_list()
    l = []
    for k in li:
        l.append([k])
    lineups = pd.DataFrame.from_records(l, columns=['Lineup'])
    lineups['Season'] = ye
    lineups[['P1', 'P2', 'P3', 'P4', 'P5']] = lineups.Lineup.str.split(", ", expand=True)
    lineups.head()



