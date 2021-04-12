import streamlit as st
import pandas as pd
import numpy as np
import Database
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import sqlite3
import app_sql


def get_table(table_name):
    df = pd.read_sql_query('SELECT * FROM ' + table_name, conn)
    return df


def get_player_picture(id, player_name, player_type):
    img = open(file='../Players Pictures/' + id + '.png')
    return st.image(img, caption=player_name + ' : ' + player_type)


conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v5.db')  # Connection / Creation of the DataBase
c = conn.cursor()
conn.commit()

"""st.title('myLineup')
st.subheader('Optimizing NBA Lineups using unsupervised machine learning')
st.text('After getting all stats possible on the NBA.com website, my main idea was to create clusters \nof players '
        'based on their statistics using unsupervised machine learning. Then after that, the goal is to\nsee what are '
        'the types of players that compose the bests lineups.')

st.subheader('I.    Clustering NBA players.')
st.text('Using request python library, I managed to get datas from the last 7 years. In total, I got 123\n'
        'tables on statistics of : \n'
        '- Players\n'
        '- Teams\n'
        '- Lineups\n\n'
        'Here is a first tool that allow you to go through all the differents tables I have in the database. \n')

df_tables = pd.read_sql_query('SELECT name as "Tables" FROM sqlite_master WHERE type ="table" AND name NOT LIKE '
                             '"sqlite_%" AND (name like "Players%"	OR name like "Teams%" OR name like "Lineups%") '
                             'AND name <> "Players_with_type"', conn)

list_tables = df_tables['Tables'].to_list()
table_selection = st.selectbox('Select the table you want to go through : ', list_tables)
df_tables_selected = get_table(table_selection)
st.dataframe(data=df_tables_selected)"""

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

st.text("The next step in my analysis is to look for specifics on each type of player. By doing this I will be \n"
        "able to identify what field each type of player is good at / bad at. Whether for the player's coach or \n"
        "for the opposing coach, this information is very interesting because it allows: either to put his player \n"
        "in the best possible attack / defense position, or to prevent an opponent from getting into a comfort\n "
        "zone.\n\n"
        "For each type of player I summerized briefly what are his strength, and put it into this little tool :\n")

characteristic_selection = st.selectbox('Do you want to search a player or a type of player ?'
                                        , ['Player', 'Type of player'])

if characteristic_selection == 'Player':
    df_characteristic = pd.read_sql_query('SELECT PlayersBios_PLAYER_NAME as Name, PlayersBios_PLAYER_ID as Player_ID, '
                                          'P.Type, "Type name" as Type_name, Characteristics FROM Players_with_type P '
                                          'JOIN Type_description T on T.Type = P.Type', conn)
    list_player_current_season = df_characteristic['Name'].to_list()
    characteristic_player_selection = st.selectbox('Select the player you and see his characteristics : '
                                                   , list_player_current_season)
    player_id = df_characteristic.loc[df_characteristic['Name'] ==
                                      characteristic_player_selection].Player_ID.values[0]
    type_name = df_characteristic.loc[df_characteristic['Name'] ==
                                      characteristic_player_selection].Type_name.values[0]
    characteristic = df_characteristic.loc[df_characteristic['Name'] ==
                                           characteristic_player_selection].Characteristics.values[0]
    img, graph = st.beta_columns(2)

    with img:
        st.subheader(characteristic_player_selection)
        st.image('../Players Pictures/' + player_id + '.png', caption=characteristic_player_selection
                                                                      + ' : ' + type_name)
        st.write(characteristic)
    with graph:
        df_top_guard = pd.read_sql_query('select CASE WHEN T.Type = "1 - 0" THEN "Top guards" ELSE "Other" END as Type,'
                               '"PlayersShot7DribbleRange_FGM" from "PlayersShot7DribbleRange" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersShot7DribbleRange_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersShot7DribbleRange_Season = "2020-21" AND '
                               'PlayersShot7DribbleRange_SeasonType = "Regular Season"', conn)

        dft = df_top_guard['PlayersShot7DribbleRange_FGM'].loc[df_top_guard['Type'] == 'Top guards']
        dfo = df_top_guard['PlayersShot7DribbleRange_FGM'].loc[df_top_guard['Type'] == 'Other']
        a = [dft.to_numpy(), dfo.to_numpy()]
        li = ['Top guards', 'Other']
        fig6 = ff.create_distplot(a, group_labels=li, curve_type='normal')
        fig6.update_xaxes(title_text='Number of basket scored after 7 or more dribbles')
        fig6.update_yaxes(title_text='Density')
        st.write(fig6)

st.subheader('II.    Optimizing Team lineups.')

df_team = pd.read_sql_query('select TeamsTraditionalStats_TEAM_ID as Team_ID, TeamsTraditionalStats_TEAM_NAME as Team '
                            'from "TeamsTraditionalStats" WHERE TeamsTraditionalStats_Season = "2020-21" and '
                            'TeamsTraditionalStats_SeasonType = "Regular Season"', conn)

team_list = df_team['Team'].to_list()
team_selected = st.selectbox('Choose one team :', team_list)
team_id_selected = df_team.loc[df_team['Team'] == team_selected].Team_ID.values[0]

df_current_roster_stats = pd.read_sql_query('SELECT PlayersGeneralStats_PLAYER_NAME, PlayersGeneralStats_GP, '
                                         'PlayersGeneralStats_MIN, PlayersGeneralStats_REB, PlayersGeneralStats_AST, '
                                         'PlayersGeneralStats_PTS, PlayersGeneralStats_TOV, PlayersGeneralStats_STL, '
                                         'PlayersGeneralStats_BLK, PlayersGeneralStats_PF FROM "PlayersGeneralStats" '
                                         'WHERE PlayersGeneralStats_Season = "2020-21" and '
                                         'PlayersGeneralStats_SeasonType = "Regular Season" and '
                                         'PlayersGeneralStats_TEAM_ID = ' + str(team_id_selected), conn)

st.dataframe(data=df_current_roster_stats.round(2))

df_team_scatter = pd.read_sql_query('select T.TeamsTraditionalStats_TEAM_NAME as Teams, '
                                    'T.TeamsTraditionalStats_Team_ID as Teams_ID, T.TeamsTraditionalStats_Season as '
                                    'Season, Cluster, T.TeamsTraditionalStats_PTS '
                                    'as "Average PTS Scored", (T.TeamsTraditionalStats_PTS + (-'
                                    'T.TeamsTraditionalStats_PLUS_MINUS)) as "Average PTS Opponent Scored" from '
                                    '"PCA_Dataset_Teams" P JOIN "TeamsTraditionalStats" T on '
                                    'P.TeamsTraditionalStats_TEAM_ID = T.TeamsTraditionalStats_TEAM_ID and '
                                    'P.TeamsTraditionalStats_Season = T.TeamsTraditionalStats_Season WHERE '
                                    'T.TeamsTraditionalStats_SeasonType = "Regular Season"', conn)

df_team_scatter['Cluster'] = df_team_scatter['Cluster'].astype(str)
df_team_scatter['Identifier'] = 0
df_team_scatter['Identifier'].loc[(df_team_scatter['Teams_ID'] == team_id_selected) & (df_team_scatter['Season'] ==
                                                                                       '2020-21')] = team_selected
df_team_scatter['Identifier'].loc[(df_team_scatter['Identifier'] == 0)] = 'Other'
df_team_scatter['Hover'] = df_team_scatter['Teams'] + df_team_scatter['Season']

fig = px.scatter(df_team_scatter.sort_values('Cluster')
                 , x="Average PTS Scored"
                 , y="Average PTS Opponent Scored"
                 , color="Identifier"
                 , symbol='Cluster'
                 , hover_name='Hover')

st.write(fig)

df_optimized_roster_stats = pd.read_sql_query('select T.Team_Name, T.Team_ID, "2020-21*" as Season, "4" as "Cluster", '
                                              'O.PTS as "Average PTS Scored", O.OPP_PTS as "Average PTS Opponent '
                                              'Scored", "' + team_selected + '" as "Identifier" from '
                                                                             '"Optimized_teams" O '
                                              'JOIN Team_Correspondence T on T."PlayersBios_TEAM_ABBREVIATION" = '
                                              'O.PlayersBios_TEAM_ABBREVIATION WHERE T.Team_ID = '
                                              + str(team_id_selected), conn)
df_optimized_roster_stats['Hover'] = df_optimized_roster_stats['Team_Name'] + df_optimized_roster_stats['Season']

df_team_scatter = pd.concat([df_team_scatter, df_optimized_roster_stats])

fig2 = px.scatter(df_team_scatter.sort_values('Cluster')
                  , x="Average PTS Scored"
                  , y="Average PTS Opponent Scored"
                  , color="Identifier"
                  , symbol='Cluster'
                  , hover_name='Hover')

st.write(fig2)


df_optimized_roster_stats = pd.read_sql_query('select O.PlayerName, O.Min, O.PTS, O.FGM, O.FGA, O.FG_PCT, O.FG3M, '
                                              'O.FG3A, O.FG3_PCT, O.FTM, O.FTA, O.FT_PCT, O.REB, O.AST, O.TOV, O.STL, '
                                              'O.BLK, O.PF from "Optimized_boxscores_lineups2" O JOIN '
                                              'Team_Correspondence T on T."PlayersBios_TEAM_ABBREVIATION" = '
                                              'O.PlayersBios_TEAM_ABBREVIATION WHERE T."Team_ID" = ' + str(
                                               team_id_selected), conn)

st.dataframe(data=df_optimized_roster_stats.round(2))

df = pd.read_sql_query('select CASE WHEN T.Type = "1 - 0" THEN "Top guards" ELSE "Other" END as Type, '
                                  '"PlayersShot7DribbleRange_FGM" from "PlayersShot7DribbleRange" P LEFT JOIN '
                                  '"Players_with_type" T on P."PlayersShot7DribbleRange_PLAYER_ID" = '
                                  'T.PlayersBios_PLAYER_ID WHERE PlayersShot7DribbleRange_Season = "2020-21" AND '
                                  'PlayersShot7DribbleRange_SeasonType = "Regular Season"', conn)

dft = df['PlayersShot7DribbleRange_FGM'].loc[df['Type'] == 'Top guards']
dfo = df['PlayersShot7DribbleRange_FGM'].loc[df['Type'] == 'Other']
a = [dft.to_numpy(), dfo.to_numpy()]
li = ['Top guards', 'Other']
fig6 = ff.create_distplot(a, group_labels=li, curve_type='normal')
st.write(fig6)

df2 = pd.read_sql_query('select CASE WHEN T.Type = "1 - 1" THEN "TraditionalPointGuards" ELSE "Other" END as Type,'
                                  '"PlayersGeneralStats_AST" from "PlayersGeneralStats" P LEFT JOIN '
                                  '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                                  'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                                  'PlayersGeneralStats_SeasonType = "Regular Season"', conn)

dft2 = df2['PlayersGeneralStats_AST'].loc[df2['Type'] == 'TraditionalPointGuards']
dfo2 = df2['PlayersGeneralStats_AST'].loc[df2['Type'] == 'Other']
b = [dft2.to_numpy(), dfo2.to_numpy()]
li2 = ['TraditionalPointGuards', 'Other']
fig7 = ff.create_distplot(b, group_labels=li2, curve_type='normal')


st.write(fig7)