import pandas as pd
import Database
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
import datetime
import plotly.express as px
import plotly


def get_pca(filename, nb_of_components):
    """Get the PCA Dataframe with normalized data based on type of data selected (Player/Team/Lineup)"""
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, Database.conn)
        name = pd.read_sql_query('SELECT PlayersBios_PLAYER_NAME, PlayersBios_PLAYER_ID, '
                                 'PlayersBios_Season FROM NonNumeric_'
                                 + filename, Database.conn)
        df = pd.DataFrame(query)
        get_name = pd.DataFrame(name)
        col_name = 'PlayerName'
        ncluster = 7
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, Database.conn)
        name = pd.read_sql_query('SELECT TeamsTraditionalStats_TEAM_NAME, TeamsTraditionalStats_TEAM_ID, '
                                 ' TeamsTraditionalStats_Season FROM NonNumeric_' + filename, Database.conn)
        df = pd.DataFrame(query)
        get_name = pd.DataFrame(name)
        col_name = 'TeamName'
        ncluster = 4
    elif filename == 'Dataset_Lineups':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, Database.conn)
        name = pd.read_sql_query('SELECT LineupsTraditionalStats_GROUP_NAME, '
                                 'LineupsTraditionalStats_GROUP_ID, LineupsTraditionalStats_Season FROM '
                                 'NonNumeric_' + filename, Database.conn)
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
        PCA_components.to_sql('PCA_' + filename, Database.conn, if_exists='replace', index=False)
    elif filename == 'Dataset_Teams':
        PCA_components.insert(0, 'TeamsTraditionalStats_TEAM_NAME', get_name['TeamsTraditionalStats_TEAM_NAME'])
        PCA_components.insert(1, 'TeamsTraditionalStats_TEAM_ID', get_name['TeamsTraditionalStats_TEAM_ID'])
        PCA_components.insert(2, 'TeamsTraditionalStats_Season', get_name['TeamsTraditionalStats_Season'])
        PCA_components.to_sql('PCA_' + filename, Database.conn, if_exists='replace', index=False)
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
        PCA_components.to_sql('PCA_' + filename, Database.conn, if_exists='replace', index=False)
    print('PCA_' + filename + ' Created')


def get_lda():
    """Get the LDA Dataframe with normalized lineup data"""
    query = pd.read_sql_query('SELECT * FROM Numeric_Dataset_Lineups', Database.conn)
    name = pd.read_sql_query('SELECT LineupsTraditionalStats_GROUP_NAME, '
                             'LineupsTraditionalStats_GROUP_ID, LineupsTraditionalStats_Season FROM '
                             'NonNumeric_Dataset_Lineups', Database.conn)
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
    LDA_components['Size'] = 0.25
    fig = px.scatter_3d(LDA_components, x='LDA1', y='LDA2', z='LDA3', hover_name='Names', color='Class', opacity=0.5,
                        size='Size')
    html_name = str(datetime.datetime.now()).replace(" ", "").replace("-", "").replace(":", "")[:12] + '_3D_LDA'
    plotly.offline.plot(fig, filename='../Graphs/' + html_name + '.html')
    LDA_components.to_sql('LDA_Dataset_Lineups', Database.conn, if_exists='replace', index=False)
    print('LDA_Dataset_Lineups Created')
