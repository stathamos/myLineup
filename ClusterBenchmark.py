import pandas as pd
import numpy as np
import seaborn as sns
import sklearn.cluster as cluster
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly
import hdbscan
import sqlite3


conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.1.db')  # Connection / Creation of the DataBase
c = conn.cursor()
conn.commit()


def plot_clusters(algo_name, algorithm, args, kwds):
    df = pd.read_sql_query('Select * FROM PCA_Dataset_Players', conn)
    labels = algorithm(*args, **kwds).fit_predict(df.iloc[:, 3:6])
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    fig2 = px.scatter_3d(df, x='PCA1', y='PCA2', z='PCA3', color=colors, hover_name='PlayersBios_PLAYER_NAME'
                         , opacity=0.7)
    return plotly.offline.plot(fig2, filename='../Graphs/test ' + str(algo_name) + '.html')


def get_numeric_data(filename):
      df=pd.read_csv('../DB 100h Proj/'+filename+'.csv', sep=';') #read csv file
      df=df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season') & (df['PlayersBios_Season'] != '2020-21')]  # Excluding playoff games and current season because there are not enough games played
      columns = df.columns.to_list()
      df.drop(columns=columns[:columns.index('PlayersBios_GP')], inplace=True)
      return df


def get_non_numeric_data(filename):
      df=pd.read_csv('../DB 100h Proj/'+filename+'.csv', sep=';') #read csv file
      df = df.loc[(df['PlayersBios_SeasonType'] == 'Regular Season') & (df['PlayersBios_Season'] != '2020-21')]  # Excluding playoff games and current season because there are not enough games played
      columns = df.columns.to_list()
      df.drop(columns=columns[columns.index('PlayersBios_GP'):], inplace=True)
      df.reset_index(inplace=True)
      return df


def get_duplicate_columns(df):
    duplicateColumnNames = set()
    for x in range(df.shape[1]): # Iterate over all the columns in dataframe
        col = df.iloc[:, x] # Select column at xth index.
        for y in range(x + 1, df.shape[1]): # Iterate over all the columns in DataFrame from (x+1)th index till end
            otherCol = df.iloc[:, y] # Select column at yth index.
            if col.equals(otherCol): # Check if two columns at x 7 y index are equal
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
    df.dropna(axis=1,thresh=len(df)*missing_rate, inplace=True)
    return df


def get_pca(df, nb_of_components):
    X_std = StandardScaler().fit_transform(df)
    pca = PCA(n_components=nb_of_components)
    principalComponents = pca.fit_transform(X_std)
    PCA_components = pd.DataFrame(principalComponents)
    PCA_components.drop(columns=list(PCA_components.columns)[3:], inplace=True)
    return PCA_components


'''df_numeric = get_numeric_data('Dataset_Players')

df_non_numeric = get_non_numeric_data('Dataset_Players')

df_numeric = delete_columns_with_missing_values(df_numeric, 0.8)

# df_numeric = df_numeric.drop(columns=get_duplicate_columns(df_numeric))

df_numeric = clean_dataset(df_numeric)

PCA_components = get_pca(df_numeric, 30)'''



# plot_clusters('Kmeans', cluster.KMeans, (), {'n_clusters':7})

plot_clusters('Affinity propagation', cluster.AffinityPropagation, (), {'damping': 0.95})

plot_clusters('MeanShift', cluster.MeanShift, (6,), {'cluster_all': True})

# plotly.offline.plot(plot_clusters(PCA_components.to_numpy(), cluster.SpectralClustering, (), {'n_clusters':7}), filename='../Graphs/test_SpectralClustering.html')

plot_clusters('AgglomerativeClustering', cluster.AgglomerativeClustering, (), {'n_clusters':7, 'linkage':'average'})

plot_clusters('HDBSCAN', hdbscan.HDBSCAN, (), {'min_cluster_size':15})
