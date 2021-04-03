import streamlit as st
import pandas as pd
import numpy as np
import Database
import plotly.express as px
import plotly.figure_factory as ff
import sqlite3


conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v5.db')  # Connection / Creation of the DataBase
c = conn.cursor()
conn.commit()

st.title('myLineup')
st.subheader('Optimizing NBA Lineups using unsupervised machine learning')
st.text('Explaining what is the goal of the application, and how did I do ?')

st.subheader('I.    Select the team you want to optimize.')

df_team = pd.read_sql_query('select TeamsTraditionalStats_TEAM_ID as Team_ID, TeamsTraditionalStats_TEAM_NAME as Team '
                            'from "TeamsTraditionalStats" WHERE TeamsTraditionalStats_Season = "2020-21" and '
                            'TeamsTraditionalStats_SeasonType = "Regular Season"', conn)

team_list = df_team['Team'].to_list()
team_selected = st.selectbox('Choose one team :', team_list)
team_id_selected = df_team['Team_ID'].loc[df_team['Team'] == team_selected][0]

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
                                              'Scored", "' + team_selected + '" as "Identifier" from "Optimized_teams" O '
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
                                              'O.BLK, O.PF from "Optimized_boxscores_lineups" O JOIN '
                                              'Team_Correspondence T on T."PlayersBios_TEAM_ABBREVIATION" = '
                                              'O.PlayersBios_TEAM_ABBREVIATION WHERE T."Team_ID" = ' + str(
                                               team_id_selected), conn)

st.dataframe(data=df_optimized_roster_stats.round(2))

