import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


def app():
    """Showing the players on PCA Axis, and explaining to what are linked the PCA variables"""

    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v6.db')  # Connection / Creation of the DataBase
    conn.commit()

    st.image('../Logo.png')

    st.markdown("In order to group players based on their statistics, we had to link all\n"
                "'Player's' table thanks to three columns we find in every tables :\n"
                "- Player_ID\n"
                "- Season\n"
                "- SeasonType\n\n"
                "It allowed us to get a big dataset containing every column per players\n"
                "in it. From more than **1000 columns** we could reduce it to **30 columns**\n"
                "and still managed to have **75% of the data** thanks to **PCA**.\n"
                "After getting this numeric dataset, the next step was to use **K-Means algorithm**\n"
                "to look for similarities between player's statistics.\n"
                "We found **7 clusters**, each one divided in **3 sub-clusters** which give us a total\n"
                "of **21 clusters**. Each clusters have specific characteristics which will\n"
                "be explained in the next part.\n\n"
                "We decided to plot our result on the **3 PCA axis**. Those axis allows us\n"
                "to know with which variables the players are linked. Here is a quick recap :\n"
                "- **PCA1 rewards** players that score a lot of points and play big minutes\n"
                "   and **penalizes** the opposite\n"
                "- **PCA2 rewards** players that defend near the rim and **penalizes** \n"
                "   players that shoot a lot of three points\n"
                "-  **PCA3 rewards** players that do a lot of dribbles and **penalizes**\n"
                "   catch and shooters\n")

    df_pca = pd.read_sql_query('select PlayersBios_PLAYER_NAME, Playersbios_player_id, PlayersBios_Season, PCA1, PCA2, '
                               'PCA3, T."Type name", P.Type as Cluster, CASE WHEN PlayersBios_PLAYER_NAME = "Centroid" '
                               'THEN "Centroid" ELSE T."Type name" END as "Player type" from "PCA_Dataset_Players" P '
                               'LEFT JOIN Type_description T on T.Type = P.Type', conn)

    c1 = px.colors.sequential.Viridis
    c2 = px.colors.sequential.Plasma
    c3 = px.colors.sequential.Blues
    c2.reverse()
    c3.reverse()
    c = c1 + c2 + c3
    c[20] = '#EF553B'
    list_player = df_pca['PlayersBios_PLAYER_NAME'].to_list()
    list_player = list(set(list_player))
    df_pca['Hover'] = df_pca['PlayersBios_PLAYER_NAME'] + ' - ' + df_pca['PlayersBios_Season']
    pca_players = st.multiselect('Select a specific player and see his evolution through the years', list_player)
    if not pca_players:
        df_pca['Size'] = 0
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] != 'Centroid')] = 0.1
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == 'Centroid')] = 0.8
    elif pca_players[0] is None:
        df_pca['Size'] = 0
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] != 'Centroid')] = 0.1
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == 'Centroid')] = 0.8
    else:
        df_pca['Size'] = 0
        for p in pca_players:
            df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == p)] = 0.8
            df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] != p)] = 0.1
            df_pca['Cluster'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == p)] = '7 - 0'
            df_pca['Player type'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == p)] = \
                'Selected player' + ' - ' + df_pca['Player type'].loc[(df_pca['PlayersBios_PLAYER_NAME'] ==
                                                                     p)].astype(str)
            index_names = df_pca[df_pca['PlayersBios_PLAYER_NAME'] == 'Centroid'].index
            df_pca.drop(index_names, inplace=True)

    fig_pca = px.scatter_3d(df_pca.sort_values('Cluster'),
                            x='PCA1',
                            y='PCA2',
                            z='PCA3',
                            color='Player type',
                            color_discrete_sequence=c,
                            hover_name='Hover',
                            opacity=0.9,
                            size='Size')
    st.write(fig_pca)
