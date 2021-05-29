import pandas as pd
import plotly.express as px
import plotly
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import datetime
import Database
import numpy as np


def scatter_3d(filename, size_pop, size_centroid, opac):
    """Plot players on PCA 3D Axis"""
    if filename == 'Dataset_Players':
        query = pd.read_sql_query('SELECT * FROM PCA_' + filename, Database.conn)
        df = pd.DataFrame(query)
        df['Hover'] = df["PlayersBios_PLAYER_NAME"] + ' - ' + df["PlayersBios_Season"]
        col_name = 'PlayersBios_PLAYER_NAME'
        type = 'Type'
    elif filename == 'Dataset_Teams':
        query = pd.read_sql_query('SELECT * FROM PCA_' + filename, Database.conn)
        df = pd.DataFrame(query)
        df['Hover'] = df["TeamsTraditionalStats_TEAM_NAME"] + ' - ' + df["TeamsTraditionalStats_Season"]
        col_name = 'TeamsTraditionalStats_TEAM_NAME'
        type = 'Type'
    elif filename == 'Dataset_Lineups':
        query = pd.read_sql_query('SELECT * FROM PCA_' + filename, Database.conn)
        df = pd.DataFrame(query)
        df['Hover'] = df["LineupsTraditionalStats_GROUP_NAME"] + ' - ' + df["LineupsTraditionalStats_Season"]
        col_name = 'LineupsTraditionalStats_GROUP_NAME'
        type = 'Cluster'
    df['Size'] = None
    df['Symbol'] = None
    df['Size'].loc[(df[col_name] == 'Centroid')] = size_centroid
    df['Symbol'].loc[(df[col_name] == 'Centroid')] = 'circle'
    df['Size'].loc[(df[col_name] != 'Centroid')] = size_pop
    df['Symbol'].loc[(df[col_name] != 'Centroid')] = 'cross'
    si = df['Size'].to_list()
    html_name = str(datetime.datetime.now()).replace(" ", "").replace("-", "").replace(":", "")[:12] + '_3d_' + filename
    c1 = px.colors.sequential.Viridis
    c2 = px.colors.sequential.Plasma
    c3 = px.colors.sequential.Blues
    c2.reverse()
    c3.reverse()
    c = c1+c2+c3
    fig = px.scatter_3d(df.sort_values('Type'),
                        x='PCA1',
                        y='PCA2',
                        z='PCA3',
                        color='Type',
                        color_discrete_sequence=c,
                        symbol='Symbol',
                        hover_name='Hover',
                        opacity=opac,
                        size=si,
                        title='PCA ' + filename)
    return plotly.offline.plot(fig, filename='../Graphs/' + html_name + '.html')


def plot_histo(filename, type, nb_of_components):
    """Plot PCA explained variance by the number of components"""
    ks = range(1, nb_of_components)
    inertias = []
    if type == 'exp_var':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, Database.conn)
        df = pd.DataFrame(query)
        X_std = StandardScaler().fit_transform(df)
        pca = PCA(n_components=nb_of_components)
        principalComponents = pca.fit_transform(X_std)
        exp_var_cumul = np.cumsum(pca.explained_variance_ratio_)
        html_name = str(datetime.datetime.now()).replace(" ", "").replace("-", "").replace(":", "")[
                    :12] + '_' + filename + '_' + type
        fig = px.area(
            x=range(1, exp_var_cumul.shape[0] + 1),
            y=exp_var_cumul,
            labels={"x": "# Components", "y": "Explained Variance"})
        return plotly.offline.plot(fig, filename='../Graphs/' + html_name + '.html')
    elif type == 'nb_clus':
        query = pd.read_sql_query('SELECT * FROM Numeric_' + filename, Database.conn)
        df = pd.DataFrame(query)
        X_std = StandardScaler().fit_transform(df)
        pca = PCA(n_components=nb_of_components)
        principalComponents = pca.fit_transform(X_std)
        PCA_components = pd.DataFrame(principalComponents)
        for k in ks:
            model = KMeans(n_clusters=k)  # Create a KMeans instance with k clusters: model
            model.fit(PCA_components.iloc[:, :3])  # Fit model to samples
            inertias.append(model.inertia_)
        html_name = str(datetime.datetime.now()).replace(" ", "").replace("-", "").replace(":", "")[
                    :12] + '_' + filename + '_' + type
        fig = px.area(
            y=inertias,
            x=ks,
            labels={"x": "Number of cluster", "y": "Inertia"})
        return plotly.offline.plot(fig, filename='../Graphs/' + html_name + '.html')