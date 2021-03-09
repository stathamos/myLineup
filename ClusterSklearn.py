import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly


def get_numeric_data(filename):
    df = pd.read_csv('../DB 100h Proj/' + filename + '.csv', sep=';')  # read csv file
    df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season') & (df[
                                                                          'PlayersBios_Season'] != '2020-21')]  # Excluding playoff games and current season because there are not enough games played
    columns = df.columns.to_list()
    df.drop(columns=columns[:columns.index('PlayersBios_GP')], inplace=True)
    return df


def get_non_numeric_data(filename):
    df = pd.read_csv('../DB 100h Proj/' + filename + '.csv', sep=';')  # read csv file
    df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season') & (df[
                                                                          'PlayersBios_Season'] != '2020-21')]  # Excluding playoff games and current season because there are not enough games played
    columns = df.columns.to_list()
    df.drop(columns=columns[columns.index('PlayersBios_GP'):], inplace=True)
    df.reset_index(inplace=True)
    return df


def get_duplicate_columns(df):
    duplicateColumnNames = set()
    for x in range(df.shape[1]):  # Iterate over all the columns in dataframe
        col = df.iloc[:, x]  # Select column at xth index.
        for y in range(x + 1, df.shape[1]):  # Iterate over all the columns in DataFrame from (x+1)th index till end
            otherCol = df.iloc[:, y]  # Select column at yth index.
            if col.equals(otherCol):  # Check if two columns at x 7 y index are equal
                duplicateColumnNames.add(df.columns.values[y])
                print(y)
    return list(duplicateColumnNames)


def clean_dataset(df):
    """This function is to get rid of the "NaN" values / "inf" values"""
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.fillna(0, inplace=True)  # Replace null values by 0
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)  # Take off NaN and inf values
    return df[indices_to_keep].astype(np.float64)  # Return the "clean" dataset


def delete_columns_with_missing_values(df, missing_rate):
    df.dropna(axis=1, thresh=len(df) * missing_rate, inplace=True)
    return df


def plot_histo(type, df, nb_of_components):
    ks = range(1, nb_of_components)
    inertias = []
    if type == 'exp_var':
        X_std = StandardScaler().fit_transform(df)
        pca = PCA(n_components=nb_of_components)
        principalComponents = pca.fit_transform(X_std)
        exp_var_cumul = np.cumsum(pca.explained_variance_ratio_)
        return px.area(
            x=range(1, exp_var_cumul.shape[0] + 1),
            y=exp_var_cumul,
            labels={"x": "# Components", "y": "Explained Variance"}
        )
    elif type == 'nb_clus':
        X_std = StandardScaler().fit_transform(df)
        pca = PCA(n_components=nb_of_components)
        principalComponents = pca.fit_transform(X_std)
        PCA_components = pd.DataFrame(principalComponents)
        for k in ks:
            model = KMeans(n_clusters=k)  # Create a KMeans instance with k clusters: model
            model.fit(PCA_components.iloc[:, :3])  # Fit model to samples
            inertias.append(model.inertia_)
    return px.area(
        y=inertias,
        x=ks,
        labels={"x": "Number of cluster", "y": "Inertia"}
    )


def get_pca(df, nb_of_components):
    X_std = StandardScaler().fit_transform(df)
    pca = PCA(n_components=nb_of_components)
    principalComponents = pca.fit_transform(X_std)
    PCA_components = pd.DataFrame(principalComponents)
    return PCA_components


def get_cluster_labels(nb_clus):
    model = KMeans(n_clusters=nb_clus)  # Selecting the number of clusters
    model.fit(PCA_components.iloc[:, :3])  # Fit the PCA Component in order to plot them
    labels = model.predict(PCA_components.iloc[:, :3])
    return labels  # Associate each player with a cluster


def get_pca_with_cluster():
    PCA_components.drop(columns=list(PCA_components.columns)[3:], inplace=True)
    PCA_components['Cluster'] = labels
    PCA_components['Name'] = df_non_numeric['PlayersBios_PLAYER_NAME']
    return PCA_components


def get_centroids(nb_clus):
    model = KMeans(n_clusters=nb_clus)  # Selecting the number of clusters
    model.fit(PCA_components.iloc[:, :3])  # Fit the PCA Component in order to plot them
    centroids = model.cluster_centers_
    return centroids


def get_centroids_df(nb_clus):
    centroids_df = pd.DataFrame.from_records(centroids)
    centroids_df['Cluster'] = nb_clus
    centroids_df['Name'] = None
    for i in range(len(centroids_df) + 1):
        centroids_df['Name'][i] = 'Cluster - ' + str(i)
    return centroids_df


def get_pca_components_with_centroids():
    PCA_components_with_centroids = pd.concat([PCA_components, centroids_df])
    PCA_components_with_centroids.rename(columns={0: 'PCA1', 1: 'PCA2', 2: 'PCA3'}, inplace=True)
    return PCA_components_with_centroids


def get_pca_components_with_distances():
    for i in range(len(centroids_df)):
        centroids_df['Cluster'][i] = i
    PCA_components_with_distances = pd.merge(PCA_components_with_centroids, centroids_df, how='inner', on='Cluster')
    PCA_components_with_distances.rename(columns={0: 'cx', 1: 'cy', 2: 'cz'}, inplace=True)
    return PCA_components_with_distances


def scatter_3d(size_pop, size_centroid, opac):
    PCA_components['Size'] = size_pop
    centroids_df['Size'] = size_centroid
    fig = px.scatter_3d(PCA_components_with_centroids,
                        x='PCA1',
                        y='PCA2',
                        z='PCA3',
                        color='Cluster',
                        hover_name='Name',
                        opacity=opac,
                        size='Size')
    return fig


def get_dist_from_centroid():
    distances = []
    for i in range(len(PCA_components_with_distances)):
        distances.append(
            np.sqrt((PCA_components_with_distances['PCA1'][i] - PCA_components_with_distances['cx'][i]) ** 2
                    + (PCA_components_with_distances['PCA2'][i] - PCA_components_with_distances['cy'][i]) ** 2
                    + (PCA_components_with_distances['PCA3'][i] - PCA_components_with_distances['cz'][i]) ** 2))
    PCA_components_with_distances['Distances'] = distances
    avg_dist = PCA_components_with_distances.groupby('Cluster').mean()['Distances']
    avg_dist_by_cluster_df = avg_dist.to_frame()
    PCA_components_with_avg_distances = pd.merge(PCA_components_with_distances, avg_dist_by_cluster_df, how='inner',
                                                 on='Cluster')
    PCA_components_with_avg_distances.rename(columns={'Name_x': 'Name', 'Distances_x': 'Distance from centroid',
                                                      'Distances_y': 'Average distance from centroid'}, inplace=True)
    PCA_components_with_avg_distances['Diff distance'] = abs(
        PCA_components_with_avg_distances['Distance from centroid'] - PCA_components_with_avg_distances[
            'Average distance from centroid'])
    PCA_components_with_avg_distances['Ratio'] = abs(
        PCA_components_with_avg_distances['Distance from centroid'] / PCA_components_with_avg_distances[
            'Average distance from centroid'])
    return PCA_components_with_avg_distances


def plot_dist_from_centroid():
    fig2 = px.scatter(PCA_components_with_avg_distances, x='Diff distance', y='Cluster', color='Ratio',
                      hover_name='Name')
    return fig2


df_numeric = get_numeric_data('Dataset_Players')

df_non_numeric = get_non_numeric_data('Dataset_Players')

df_numeric = delete_columns_with_missing_values(df_numeric, 0.8)

# df_numeric = df_numeric.drop(columns=get_duplicate_columns(df_numeric))

df_numeric = clean_dataset(df_numeric)

PCA_components = get_pca(df_numeric, 30)

labels = get_cluster_labels(7)

PCA_components = get_pca_with_cluster()

centroids = get_centroids(7)

centroids_df = get_centroids_df(7)

PCA_components_with_centroids = get_pca_components_with_centroids()

PCA_components_with_distances = get_pca_components_with_distances()

# plotly.offline.plot(plot_histo('exp_var', df_numeric, 30), filename='../Graphs/exp_var.html')

# plotly.offline.plot(plot_histo('nb_clus', df_numeric, 30), filename='../Graphs/nb_clus.html')

# plotly.offline.plot(scatter_3d(7, 0.5, 1, 1), filename='../Graphs/3d_pca_players.html')

PCA_components_with_avg_distances = get_dist_from_centroid()

# plotly.offline.plot(plot_dist_from_centroid(), filename='../Graphs/dist_from_centroid.html')
