import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


def app():

    def sort_list(li):
        if li[1] == 'Other players':
            li[1] = li[0]
            li[0] = 'Other players'
        return li



    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v5.db')  # Connection / Creation of the DataBase
    c = conn.cursor()
    conn.commit()

    logo = open(file='../Logo.png')

    st.image('../Logo.png')

    st.text('My first idea was to find clusters in players types. With all of these informations, can we define and\n'
            'group players based on their statistics?\n'
            'In order to that, I had to link all the tables thanks to three columns which are on every tables :\n'
            '- Player_ID\n'
            '- Season\n'
            '- SeasonType\n'
            'It allowed me to get a big dataset with every columns per players in it.\n'
            'To be able to exploit these data, I had to use dimension reduction on the new made dataset\n'
            'From almost 1000 columns, I could reduce it to 30 columns thanks to Principal Component Analysis\n'
            'technic and still managed to have 75% of the datas in it.\n\n'
            'Once I had my numeric dataset, I was able to use K-Means algorithm on it in order to get clusters\n'
            'on players. I found 7 clusters, but I thought I could be more precise and find more "type of \n'
            'players". To do that, I used again K-means on each clusters which gave me 3 subcluters per cluster.\n'
            'In total, 21 clusters have been found. Each clusters has his own specific characteristics which\n'
            'will be explained later.\n\n'
            'Here is the result we get when we plot it into the PCA axis. You can try to find some players\n')

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
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] != 'Centroid')] = 0.2
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == 'Centroid')] = 0.8
    elif pca_players[0] is None:
        df_pca['Size'] = 0
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] != 'Centroid')] = 0.2
        df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == 'Centroid')] = 0.8
    else:
        df_pca['Size'] = 0
        for p in pca_players:
            df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == p)] = 0.8
            df_pca['Size'].loc[(df_pca['PlayersBios_PLAYER_NAME'] != p)] = 0.2
            df_pca['Cluster'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == p)] = '7 - 0'
            df_pca['Player type'].loc[(df_pca['PlayersBios_PLAYER_NAME'] == p)] = 'Selected player'
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
