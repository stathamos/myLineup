import Database
import pandas as pd

data = [['0 - 0', 'select CASE WHEN T.Type = "0 - 0" THEN "Traditional power forward" ELSE "Other players" END as Type,'
                  '"PlayersPlaytypes_Cut_POSS" from "PlayersPlaytypes_Cut" P LEFT JOIN '
                  '"Players_with_type" T on P."PlayersPlaytypes_Cut_PLAYER_ID" = '
                  'T.PlayersBios_PLAYER_ID WHERE PlayersPlaytypes_Cut_SeasonYear = "2020-21" AND ' 
                               'PlayersPlaytypes_Cut_SeasonType = "Regular Season"', 'Number of cut to the basket made'],
     ['0 - 1', 'select CASE WHEN T.Type = "0 - 1" THEN "Traditional center" ELSE "Other players" END as Type,'
                               '"PlayersPlaytypes_PRRollman_POSS" from "PlayersPlaytypes_PRRollman" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersPlaytypes_PRRollman_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersPlaytypes_PRRollman_SeasonYear = "2020-21" AND ' 
                               'PlayersPlaytypes_PRRollman_SeasonType = "Regular Season"', 'Number of screens sets'],
     ['0 - 2', 'select CASE WHEN T.Type = "0 - 2" THEN "Back-up center" ELSE "Other players" END as Type,'
                               '"PlayersPlaytypes_PRRollman_POSS" from "PlayersPlaytypes_PRRollman" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersPlaytypes_PRRollman_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersPlaytypes_PRRollman_SeasonYear = "2020-21" AND ' 
                               'PlayersPlaytypes_PRRollman_SeasonType = "Regular Season"', 'Number of screens sets'],
     ['1 - 0', 'select CASE WHEN T.Type = "1 - 0" THEN "Top guards" ELSE "Other players" END as Type,'
                               '"PlayersShot7DribbleRange_FGM" from "PlayersShot7DribbleRange" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersShot7DribbleRange_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersShot7DribbleRange_Season = "2020-21" AND '
                               'PlayersShot7DribbleRange_SeasonType = "Regular Season"', 'Number of "rolls" per game'],
     ['1 - 1', 'select CASE WHEN T.Type = "1 - 1" THEN "Traditional point guard" ELSE "Other players" END as Type,'
                               '"PlayersGeneralStats_AST" from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of assist per game'],
     ['1 - 2', 'select CASE WHEN T.Type = "1 - 2" THEN "Complete superstar" ELSE "Other players" END as Type,'
                               '"PlayersGeneralStats_PTS" from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of points per game'],
     ['2 - 0', 'select CASE WHEN T.Type = "2 - 0" THEN "Elite modern bigs" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_REB from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of points + number of rebounds per game'],
     ['2 - 1', 'select CASE WHEN T.Type = "2 - 1" THEN "Elite modern bigs" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_REB from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of points + number of rebounds per game'],
     ['2 - 2', 'select CASE WHEN T.Type = "2 - 2" THEN "Elite traditional center" ELSE "Other players" END as Type,'
                               '"PlayersShot0DribbleRange_FGM" from "PlayersShot0DribbleRange" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersShot0DribbleRange_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersShot0DribbleRange_Season = "2020-21" AND '
                               'PlayersShot0DribbleRange_SeasonType = "Regular Season"', 'Number of shot taken without dribbles'],
     ['3 - 0', 'select CASE WHEN T.Type = "3 - 0" THEN "Elite shooter" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_FG3M from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of 3 points made per game'],
     ['3 - 1', 'select CASE WHEN T.Type = "3 - 1" THEN "2-way forward" ELSE "Other players" END as Type,'
                               '"Players2ptsDefense_FG2A" from "Players2ptsDefense" P LEFT JOIN '
                               '"Players_with_type" T on P."Players2ptsDefense_CLOSE_DEF_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE Players2ptsDefense_Season = "2020-21" AND '
                               'Players2ptsDefense_SeasonType = "Regular Season"', 'Number of 2 pointer defended per game'],
     ['3 - 2', 'select CASE WHEN T.Type = "3 - 2" THEN "Combo guard" ELSE "Other players" END as Type,'
                               '"PlayersPlaytypes_PRBallHandler_POSS" from "PlayersPlaytypes_PRBallHandler" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersPlaytypes_PRBallHandler_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersPlaytypes_PRBallHandler_SeasonYear = "2020-21" AND '
                               'PlayersPlaytypes_PRBallHandler_SeasonType = "Regular Season"', 'Number of pick and roll player per game'],
     ['4 - 1', 'select CASE WHEN T.Type = "4 - 1" THEN "Low playing time forward" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_Min from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of minutes played per game'],
     ['4 - 2', 'select CASE WHEN T.Type = "4 - 2" THEN "Low playing time center" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_Min from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of minutes played per game'],
     ['5 - 0', 'select CASE WHEN T.Type = "5 - 0" THEN "Back up space creator" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_Min from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of minutes played per game'],
     ['5 - 1', 'select CASE WHEN T.Type = "5 - 1" THEN "Back up center" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_Min from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of minutes played per game'],
     ['5 - 2', 'select CASE WHEN T.Type = "5 - 2" THEN "Back up point guard" ELSE "Other players" END as Type,'
                               'PlayersTrackingPassing_PASSES_MADE/PlayersTrackingPassing_Min from "PlayersTrackingPassing" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersTrackingPassing_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersTrackingPassing_Season = "2020-21" AND '
                               'PlayersTrackingPassing_SeasonType = "Regular Season"', 'Number of minutes played per game'],
     ['6 - 0', 'select CASE WHEN T.Type = "6 - 0" THEN "3&D" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_FG3A from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of 3 points attempted per game'],
     ['6 - 1', 'select CASE WHEN T.Type = "6 - 1" THEN "Decent point guard" ELSE "Other players" END as Type,'
                               '"PlayersGeneralStats_AST" from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of assists per game'],
     ['6 - 2', 'select CASE WHEN T.Type = "6 - 2" THEN "Back up 3&D" ELSE "Other players" END as Type,'
                               'PlayersGeneralStats_FG3A from "PlayersGeneralStats" P LEFT JOIN '
                               '"Players_with_type" T on P."PlayersGeneralStats_PLAYER_ID" = '
                               'T.PlayersBios_PLAYER_ID WHERE PlayersGeneralStats_Season = "2020-21" AND '
                               'PlayersGeneralStats_SeasonType = "Regular Season"', 'Number of 3 points attempted per game']]

columns = ['Type', 'Query', 'Title']
df_table_query = pd.DataFrame(data=data, columns=columns)
df_table_query.to_sql('Query', Database.conn, if_exists='replace', index=False)