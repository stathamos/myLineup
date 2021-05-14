import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


def app():

    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v6.db')  # Connection / Creation of the DataBase
    c = conn.cursor()
    conn.commit()


    st.image('../Logo.png')

    st.subheader('II.    Optimizing Team lineups.')

    st.text('Based on the information we have now, my idea was to use the players type found\n'
            'in order to see what are the bests lineups possible.\n'
            'In the table "LineupTraditionalStats we have a variable called "+/-" which gives\n'
            'us the differential of this lineup when they are on the floor.\n\n'
            'I divided the lineup type into 4 types based on this column : \n'
            '   - Elite lineup (> 2 +/-)\n'
            '   - Above average (> 0 +/-)\n'
            '   - Below average (< 0 +/-)\n'
            '   - Bad average (< 2 +/-)\n'
            'The next step was to check every "Elite" and "Above average" lineups to see what\n'
            'type of player it composes it. My idea was to see if a pattern appears in order\n'
            'to use it to create the bests lineups for each team.\n'
            'At first, I tried to find patterns with the 20 types of players but there were\n'
            'no evident pattern. So I chose the firsts 7 clusters I found and now I have some\n'
            'interesting patterns. \n\n'
            'After that, I could write my algorithm following some simple rules :\n'
            '   - Select a team\n'
            '   - See every combination possible\n'
            '   - See what types of players it composes it\n'
            '   - Iterate over the bests patterns and lineups possible\n'
            'And of course, every final lineups must respect some rules too : \n'
            '   - No more than 36min per player\n'
            '   - No more than 4 fouls per player\n'
            '   - No more than 3 lineups per player\n\n'
            'Some results are really interesting because the lineups have never been used in real life.')

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

    st.text('Here is the real "boxscore" of the team selected. You can go through\n'
             'the statistics of every player on the team.')

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
    df_team_scatter['Hover'] = df_team_scatter['Teams'] + ' - ' + df_team_scatter['Season']

    fig = px.scatter(df_team_scatter.sort_values('Cluster')
                     , x="Average PTS Scored"
                     , y="Average PTS Opponent Scored"
                     , color="Identifier"
                     , hover_name='Hover')

    st.text('In order to make it more visual, I plotted a simple graph which \n'
            'shows the average points scored by the average point the opponent\n'
            'scored for every team. You can find the selected team with the \n'
            'red dot.\n\n'
            'If the dot is located on the bottom right of the graph, it means \n'
            'that it has a positive "+/-" which is good. \n')

    st.write(fig)

    df_optimized_roster_stats = pd.read_sql_query('select T.Team_Name, T.Team_ID, "2020-21*" as Season, "4" as "Cluster", '
                                                  'O.PTS as "Average PTS Scored", O.OPP_PTS as "Average PTS Opponent '
                                                  'Scored", "' + team_selected + '" as "Identifier" from '
                                                                                 '"Optimized_teams" O '
                                                                                 'JOIN Team_Correspondence T on T."PlayersBios_TEAM_ABBREVIATION" = '
                                                                                 'O.PlayersBios_TEAM_ABBREVIATION WHERE T.Team_ID = '
                                                  + str(team_id_selected), conn)
    df_optimized_roster_stats['Hover'] = df_optimized_roster_stats['Team_Name'] + ' - ' \
                                         + df_optimized_roster_stats['Season']

    df_team_scatter = pd.concat([df_team_scatter, df_optimized_roster_stats])

    fig2 = px.scatter(df_team_scatter.sort_values('Cluster')
                      , x="Average PTS Scored"
                      , y="Average PTS Opponent Scored"
                      , color="Identifier"
                      , hover_name='Hover')

    st.text('Then, I launched the optimizer, to seek for the bests possible\n'
            'lineups. You will see a second red dot on the graph.\n'
            'If the second dot is either :\n'
            '   - Lower\n'
            '   - More to the right\n'
            'Then I consider the optimizer as a success, because it would have\n'
            'increase either the offense or the defense of the team (or both).\n'
            'Here is the new graph and the new statistics of the optimized team.')

    st.write(fig2)

    df_optimized_roster_stats = pd.read_sql_query('select O.PlayerName, O.Min, O.PTS, O.FGM, O.FGA, O.FG_PCT, O.FG3M, '
                                                  'O.FG3A, O.FG3_PCT, O.FTM, O.FTA, O.FT_PCT, O.REB, O.AST, O.TOV, O.STL, '
                                                  'O.BLK, O.PF from "Optimized_boxscores_lineups" O JOIN '
                                                  'Team_Correspondence T on T."PlayersBios_TEAM_ABBREVIATION" = '
                                                  'O.PlayersBios_TEAM_ABBREVIATION WHERE T."Team_ID" = ' +
                                                  str(team_id_selected), conn)

    st.dataframe(data=df_optimized_roster_stats.round(2))
