import requests
import sqlite3
import time
import pandas as pd

conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.0.db')  # Connection / Creation of the DataBase
c = conn.cursor()
conn.commit()


def create_index(PlayerOrTeam, Type, TableName):
    if PlayerOrTeam == 'Player' and Type == 'Offense':
        c.execute(
            'CREATE INDEX "Index_' + TableName + '" ON "' + TableName + '" ("PLAYER_ID"	ASC, "Season" ASC, '
                                                                        '"SeasonType"	ASC);')
    elif PlayerOrTeam == 'Player' and Type == 'Defense':
        c.execute(
            'CREATE INDEX "Index_' + TableName + '" ON "' + TableName + '" ("CLOSE_DEF_PERSON_ID"	ASC, "Season" ASC, '
                                                                        '"SeasonType"	ASC);')
    elif PlayerOrTeam == 'Team' and Type == '':
        c.execute(
            'CREATE INDEX "Index_' + TableName + '" ON "' + TableName + '" ("TEAM_ID"	ASC, "Season" ASC, '
                                                                        '"SeasonType"	ASC);')
    elif PlayerOrTeam == 'Lineups' and Type == '':
        c.execute(
            'CREATE INDEX "Index_' + TableName + '" ON "' + TableName + '" ("GROUP_ID"	ASC, "Season" ASC, '
                                                                        '"SeasonType"	ASC);')


def sql_column_to_list(type):
    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v2.8.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    list = c.execute('select tbl_name from sqlite_master where type = "table" and name like "' + type + '%"').fetchall()
    return list


def get_players_data(url, typestat):
    i = 1  # Initiating the iterator to know how many lines left to import

    # Lists parameters needed for each request

    Seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21']
    Playtypes = ['Misc', 'OffRebound', 'OffScreen', 'Cut', 'Handoff', 'Spotup', 'Postup', 'PRBallHandler', 'PRRollman',
                 'Isolation', 'Transition']
    GeneralType = ['Base', 'Usage', 'Scoring', 'Advanced', 'Misc']
    GeneralTypeDetails = ['Opponent']
    SeasonType = ['Regular Season', 'Playoffs']
    PtMeasureType = ['Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding',
                     'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch']
    DefenseCategory = ['3 Pointers', '2 Pointers', 'Less Than 6Ft', 'Less Than 10Ft', 'Greater Than 15Ft']
    GeneralRange = ['Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft']
    DribbleRange = ['0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles']
    TouchTimeRange = ['Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds']
    CloseDefDistRange = ['0-2 Feet - Very Tight', '2-4 Feet - Tight', '4-6 Feet - Open', '6+ Feet - Wide Open']
    MeasureType = ['Base']

    # Parameters needed in the request made

    request_parameters = {
        'params': [
            # 1
            {'LastNGames': '0', 'LeagueID': '00', 'Month': '0', 'OpponentTeamID': '0', 'PORound': '0',
             'PerMode': 'PerGame', 'Period': '0', 'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 2
            , {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
               'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
               'LeagueID': '00', 'Location': '', 'MeasureType': GeneralType, 'Month': '0', 'OpponentTeamID': '0',
               'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
               'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons,
               'SeasonSegment': '', 'SeasonType': SeasonType, 'ShotClockRange': '', 'StarterBench': '', 'TeamID': '0',
               'TwoWay': '0', 'VsConference': '', 'VsDivision': ''}
            # 3
            , {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
               'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0',
               'LeagueID': '00', 'Location': '', 'MeasureType': 'Opponent', 'Month': '0', 'OpponentTeamID': '0',
               'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
               'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons,
               'SeasonSegment': '', 'SeasonType': SeasonType, 'ShotClockRange': '', 'StarterBench': '', 'TeamID': '0',
               'VsConference': '', 'VsDivision': '', 'Weight': ''}
            # 4
            , {'LeagueID': '00', 'Season': Seasons, 'SeasonType': SeasonType}
            # 5
            , {'AheadBehind': 'Ahead or Behind', 'ClutchTime': 'Last 5 Minutes', 'College': '', 'Conference': '',
               'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'DraftPick': '', 'DraftYear': '',
               'GameScope': '', 'GameSegment': '', 'Height': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
               'MeasureType': GeneralType, 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0',
               'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '',
               'PlusMinus': 'N', 'PointDiff': '5', 'Rank': 'N', 'Season': Seasons, 'SeasonSegment': '',
               'SeasonType': SeasonType, 'ShotClockRange': '', 'StarterBench': '', 'TeamID': '0', 'VsConference': '',
               'VsDivision': ''}
            # 6
            , {'LeagueID': '00', 'PerMode': 'PerGame', 'PlayType': Playtypes, 'PlayerOrTeam': 'P',
               'SeasonType': SeasonType, 'SeasonYear': Seasons, 'TypeGrouping': 'offensive'}
            # 7
            , {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
               'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'Height': '', 'LastNGames': '0', 'LeagueID': '00',
               'Location': '', 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PerMode': 'PerGame',
               'PlayerExperience': '', 'PlayerOrTeam': 'Player', 'PlayerPosition': '', 'PtMeasureType': PtMeasureType,
               'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType, 'StarterBench': '', 'TeamID': '0',
               'VsConference': '', 'VsDivision': '', 'Weight': ''}
            # 8
            , {'DefenseCategory': DefenseCategory, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0',
               'OpponentTeamID': '0', 'PORound': '0', 'PerMode': 'PerGame', 'Period': '0', 'Season': Seasons,
               'SeasonType': SeasonType, 'TeamID': '0'}
            # 9
            , {'GeneralRange': GeneralRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0', 'OpponentTeamID': '0',
               'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N',
               'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 10
            , {'DribbleRange': DribbleRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0', 'OpponentTeamID': '0',
               'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N',
               'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 11
            , {'TouchTimeRange:': TouchTimeRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0',
               'OpponentTeamID': '0', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
               'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 12
            , {'CloseDefDistRange': CloseDefDistRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0',
               'OpponentTeamID': '0', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
               'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 13
            , {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '',
               'DistanceRange': '5ft Range', 'Division': '', 'DraftPick': '', 'DraftYear': '', 'GameScope': '',
               'GameSegment': '', 'Height': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
               'MeasureType': MeasureType, 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0',
               'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '',
               'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType,
               'ShotClockRange': '', 'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
            # 14
            , {'LastNGames': '0', 'LeagueID': '00', 'Month': '0', 'OpponentTeamID': '0', 'PORound': '0',
               'PaceAdjust': 'N', 'PerMode': 'PerGame', 'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons,
               'SeasonType': SeasonType, 'TeamID': '0'}
        ]
    }

    # Fixed header for each parameters

    header = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
        'origin': 'https://www.nba.com',
        'referer': 'https://www.nba.com/',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }

    # 1 - Players Bios
    if url == 'https://stats.nba.com/stats/leaguedashplayerbiostats' and typestat == '':
        for Sea in Seasons:  # Allow the code to run through every year at each iteration
            for Typ in SeasonType:  # Run through the season type (Playoffs or regular at each iteration
                request_parameters['params'][0]['Season'] = Sea  # Replace value for each season at each iteration
                request_parameters['params'][0]['SeasonType'] = Typ  # Replace value for season types at each iteration
                param = request_parameters['params'][0]  # Set the good parameter based on the url given
                data = requests.get(url=url, headers=header, params=param).json()  # Get data from request
                dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])  # Convert datas to DataFrame
                dataframe['Season'] = Sea  # Adding a new column 'Season' to DataFrame
                dataframe['SeasonType'] = Typ  # Adding a new column 'SeasonType' to DataFrame
                if dataframe.empty:  # If dataframe is empty, it means that there aren't data left to get
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))  # Shows the number of iteration made/left
                    i += 1
                else:
                    col = data['resultSets'][0]['headers']  # Get columns from the request made
                    col.append('Season')  # Adding a new column 'Season' to DataFrame
                    col.append('SeasonType')  # Adding a new column 'SeasonType' to DataFrame
                    table = 'PlayersBios_'
                    table_col = [table + x for x in col]
                    dataframe.columns = table_col  # Set the columns name for the DataFrame
                    dataframe.to_sql('PlayersBios', conn, if_exists='append', index=False)  # Insert data in SQLiteDB
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))  # Shows the number of iteration made/left
                    i += 1
                    time.sleep(1)  # Forced to put this, or the NBA.com website would block my requests
        create_index('Player', 'Offense', 'PlayersBios')
        print('All the indexes have been created')
        print('PlayersBios inserted')

    # 2 - Player General Base, Usage, Scoring, Advanced, Misc
    elif url == 'https://stats.nba.com/stats/leaguedashplayerstats' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for GenTyp in GeneralType:
                    request_parameters['params'][1]['Season'] = Sea
                    request_parameters['params'][1]['SeasonType'] = Typ
                    request_parameters['params'][1]['MeasureType'] = GenTyp
                    param = request_parameters['params'][1]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['MeasureType'] = GenTyp
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralType)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('MeasureType')
                        if GenTyp == 'Base':
                            table = 'PlayersGeneralStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralStats', conn, if_exists='append', index=False)
                        elif GenTyp == 'Usage':
                            table = 'PlayersGeneralUsageStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralUsageStats', conn, if_exists='append', index=False)
                        elif GenTyp == 'Scoring':
                            table = 'PlayersGeneralScoringStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralScoringStats', conn, if_exists='append', index=False)
                        elif GenTyp == 'Advanced':
                            table = 'PlayersGeneralAdvancedStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralAdvancedStats', conn, if_exists='append', index=False)
                        elif GenTyp == 'Misc':
                            table = 'PlayersGeneralMiscStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralMiscStats', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralType)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersGeneralStats')
        create_index('Player', 'Offense', 'PlayersGeneralUsageStats')
        create_index('Player', 'Offense', 'PlayersGeneralScoringStats')
        create_index('Player', 'Offense', 'PlayersGeneralAdvancedStats')
        create_index('Player', 'Offense', 'PlayersGeneralMiscStats')
        print('All the indexes have been created')
        print('PlayersGeneralStats inserted')

    # 3 - Player General Opponent
    elif url == 'https://stats.nba.com/stats/leagueplayerondetails' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for GenTypDet in GeneralTypeDetails:
                    request_parameters['params'][2]['Season'] = Sea
                    request_parameters['params'][2]['SeasonType'] = Typ
                    request_parameters['params'][2]['GeneralTypeDetails'] = GenTypDet
                    param = request_parameters['params'][2]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['GeneralTypeDetails'] = GenTypDet
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralTypeDetails)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('GeneralTypeDetails')
                        table = 'PlayersGeneralStatsDetailed_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('PlayersGeneralStatsDetailed', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralTypeDetails)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersGeneralStatsDetailed')
        print('All the indexes have been created')
        print('PlayersGeneralStatsDetailed inserted')

    # 4 - Player Estimated Metrics
    elif url == 'https://stats.nba.com/stats/playerestimatedmetrics' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                request_parameters['params'][3]['Season'] = Sea
                request_parameters['params'][3]['SeasonType'] = Typ
                param = request_parameters['params'][3]
                data = requests.get(url=url, headers=header, params=param).json()
                dataframe = pd.DataFrame(data['resultSet']['rowSet'])
                dataframe['Season'] = Sea
                dataframe['SeasonType'] = Typ
                if dataframe.empty:
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                else:
                    col = data['resultSet']['headers']
                    col.append('Season')
                    col.append('SeasonType')
                    table = 'PlayersEstimMetrics_'
                    table_col = [table + x for x in col]
                    dataframe.columns = table_col
                    dataframe.to_sql('PlayersEstimMetrics', conn, if_exists='append', index=False)
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                    time.sleep(1)
        create_index('Player', 'Offense', 'PlayersEstimMetrics')
        print('All the indexes have been created')
        print('PlayersEstimMetrics inserted')

    # 5 - Player Stats in the clutch
    elif url == 'https://stats.nba.com/stats/leaguedashplayerclutch' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for GenTyp in GeneralType:
                    request_parameters['params'][4]['Season'] = Sea
                    request_parameters['params'][4]['SeasonType'] = Typ
                    request_parameters['params'][4]['MeasureType'] = GenTyp
                    param = request_parameters['params'][4]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['MeasureType'] = GenTyp
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralType)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('MeasureType')
                        if GenTyp == 'Base':
                            table = 'PlayersGeneralStatsClutch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralStatsClutch', conn, if_exists='append', index=False)
                        elif GenTyp == 'Usage':
                            table = 'PlayersGeneralUsageStatsClutch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralUsageStatsClutch', conn, if_exists='append', index=False)
                        elif GenTyp == 'Scoring':
                            table = 'PlayersGeneralScoringStatsClutch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralScoringStatsClutch', conn, if_exists='append', index=False)
                        elif GenTyp == 'Advanced':
                            table = 'PlayersGeneralAdvancedStatsClutch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralAdvancedStatsClutch', conn, if_exists='append', index=False)
                        elif GenTyp == 'Misc':
                            table = 'PlayersGeneralMiscStatsClutch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersGeneralMiscStatsClutch', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralType)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersGeneralStatsClutch')
        create_index('Player', 'Offense', 'PlayersGeneralUsageStatsClutch')
        create_index('Player', 'Offense', 'PlayersGeneralScoringStatsClutch')
        create_index('Player', 'Offense', 'PlayersGeneralAdvancedStatsClutch')
        create_index('Player', 'Offense', 'PlayersGeneralMiscStatsClutch')
        print('All the indexes have been created')
        print('PlayersClutchStats inserted')

    # 6 - Players Playtypes
    elif url == 'https://stats.nba.com/stats/synergyplaytypes' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for PlayTy in Playtypes:
                    request_parameters['params'][5]['SeasonYear'] = Sea
                    request_parameters['params'][5]['SeasonType'] = Typ
                    request_parameters['params'][5]['PlayType'] = PlayTy
                    param = request_parameters['params'][5]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['SeasonYear'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['Playtype'] = PlayTy
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(Playtypes)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('SeasonYear')
                        col.append('SeasonType')
                        col.append('Playtype')
                        if PlayTy == 'Misc':
                            table = 'PlayersPlaytypes_Misc_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Misc', conn, if_exists='append', index=False)
                        elif PlayTy == 'OffRebound':
                            table = 'PlayersPlaytypes_OffRebound_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_OffRebound', conn, if_exists='append', index=False)
                        elif PlayTy == 'OffScreen':
                            table = 'PlayersPlaytypes_OffScreenc_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_OffScreen', conn, if_exists='append', index=False)
                        elif PlayTy == 'Cut':
                            table = 'PlayersPlaytypes_Cut_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Cut', conn, if_exists='append', index=False)
                        elif PlayTy == 'Handoff':
                            table = 'PlayersPlaytypes_Handoff_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Handoff', conn, if_exists='append', index=False)
                        elif PlayTy == 'Spotup':
                            table = 'PlayersPlaytypes_Spotup_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Spotup', conn, if_exists='append', index=False)
                        elif PlayTy == 'Postup':
                            table = 'PlayersPlaytypes_Postup_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Postup', conn, if_exists='append', index=False)
                        elif PlayTy == 'PRBallHandler':
                            table = 'PlayersPlaytypes_PRBallHandler_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_PRBallHandler', conn, if_exists='append', index=False)
                        elif PlayTy == 'PRRollman':
                            table = 'PlayersPlaytypes_PRRollman_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_PRRollman', conn, if_exists='append', index=False)
                        elif PlayTy == 'Isolation':
                            table = 'PlayersPlaytypes_Isolation_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Isolation', conn, if_exists='append', index=False)
                        elif PlayTy == 'Transition':
                            table = 'PlayersPlaytypes_Transition_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPlaytypes_Transition', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(Playtypes)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersPlaytypes_Misc')
        create_index('Player', 'Offense', 'PlayersPlaytypes_Transition')
        create_index('Player', 'Offense', 'PlayersPlaytypes_Isolation')
        create_index('Player', 'Offense', 'PlayersPlaytypes_PRRollman')
        create_index('Player', 'Offense', 'PlayersPlaytypes_PRBallHandler')
        create_index('Player', 'Offense', 'PlayersPlaytypes_Postup')
        create_index('Player', 'Offense', 'PlayersPlaytypes_Spotup')
        create_index('Player', 'Offense', 'PlayersPlaytypes_OffRebound')
        create_index('Player', 'Offense', 'PlayersPlaytypes_OffScreen')
        create_index('Player', 'Offense', 'PlayersPlaytypes_Cut')
        create_index('Player', 'Offense', 'PlayersPlaytypes_Handoff')
        print('All the indexes have been created')
        print('PlayersPlaytypes inserted')

    # 7 - Player Tracking data
    elif url == 'https://stats.nba.com/stats/leaguedashptstats' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for PtMeaTy in PtMeasureType:
                    request_parameters['params'][6]['Season'] = Sea
                    request_parameters['params'][6]['SeasonType'] = Typ
                    request_parameters['params'][6]['PtMeasureType'] = PtMeaTy
                    param = request_parameters['params'][6]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['PtMeasureType'] = PtMeaTy
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(PtMeasureType)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('PtMeasureType')
                        if PtMeaTy == 'Drives':
                            table = 'PlayersTrackingDrives_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingDrives', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Defense':
                            table = 'PlayersTrackingDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingDefense', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'CatchShoot':
                            table = 'PlayersTrackingCatchShoot_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingCatchShoot', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Passing':
                            table = 'PlayersTrackingPassing_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingPassing', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Possessions':
                            table = 'PlayersTrackingPossessions_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingPossessions', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'PullUpShot':
                            table = 'PlayersTrackingPullUpShot_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingPullUpShot', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Rebounding':
                            table = 'PlayersTrackingRebounding_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingRebounding', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Efficiency':
                            table = 'PlayersTrackingEfficiency_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingEfficiency', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'SpeedDistance':
                            table = 'PlayersTrackingSpeedDistance_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingSpeedDistance', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'ElbowTouch':
                            table = 'PlayersTrackingElbowTouch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingElbowTouch', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'PostTouch':
                            table = 'PlayersTrackingPostTouch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingPostTouch', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'PaintTouch':
                            table = 'PlayersTrackingPaintTouch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersTrackingPaintTouch', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(PtMeasureType)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersTrackingDrives')
        create_index('Player', 'Offense', 'PlayersTrackingDefense')
        create_index('Player', 'Offense', 'PlayersTrackingCatchShoot')
        create_index('Player', 'Offense', 'PlayersTrackingPassing')
        create_index('Player', 'Offense', 'PlayersTrackingPossessions')
        create_index('Player', 'Offense', 'PlayersTrackingPullUpShot')
        create_index('Player', 'Offense', 'PlayersTrackingRebounding')
        create_index('Player', 'Offense', 'PlayersTrackingEfficiency')
        create_index('Player', 'Offense', 'PlayersTrackingSpeedDistance')
        create_index('Player', 'Offense', 'PlayersTrackingElbowTouch')
        create_index('Player', 'Offense', 'PlayersTrackingPostTouch')
        create_index('Player', 'Offense', 'PlayersTrackingPaintTouch')
        print('All the indexes have been created')
        print('PlayersTrackingData inserted')

    # 8 - Players Defensive Dashboard DefenseCategory
    elif url == 'https://stats.nba.com/stats/leaguedashptdefend' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for DefCat in DefenseCategory:
                    request_parameters['params'][7]['Season'] = Sea
                    request_parameters['params'][7]['SeasonType'] = Typ
                    request_parameters['params'][7]['DefenseCategory'] = DefCat
                    param = request_parameters['params'][7]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['DefenseCategory'] = DefCat
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DefenseCategory)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('DefenseCategory')
                        if DefCat == '3 Pointers':
                            table = 'Players3ptsDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('Players3ptsDefense', conn, if_exists='append', index=False)
                        elif DefCat == '2 Pointers':
                            table = 'Players2ptsDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('Players2ptsDefense', conn, if_exists='append', index=False)
                        elif DefCat == 'Less Than 6Ft':
                            table = 'PlayersPaintDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersPaintDefense', conn, if_exists='append', index=False)
                        elif DefCat == 'Less Than 10Ft':
                            table = 'PlayersOutsidePaintDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersOutsidePaintDefense', conn, if_exists='append', index=False)
                        elif DefCat == 'Greater Than 15Ft':
                            table = 'PlayersFarFromBasketDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersFarFromBasketDefense', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DefenseCategory)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Defense', 'Players3ptsDefense')
        create_index('Player', 'Defense', 'Players2ptsDefense')
        create_index('Player', 'Defense', 'PlayersPaintDefense')
        create_index('Player', 'Defense', 'PlayersOutsidePaintDefense')
        create_index('Player', 'Defense', 'PlayersFarFromBasketDefense')
        print('All the indexes have been created')
        print('PlayersDefenseDashboard inserted')

    # 9 - Players Shots Dashboard - General Range
    elif url == 'https://stats.nba.com/stats/leaguedashplayerptshot' and typestat == 'GeneralRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for GenRan in GeneralRange:
                    request_parameters['params'][8]['Season'] = Sea
                    request_parameters['params'][8]['SeasonType'] = Typ
                    request_parameters['params'][8]['GeneralRange'] = GenRan
                    param = request_parameters['params'][8]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['GeneralRange'] = GenRan
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('GeneralRange')
                        if GenRan == 'Overall':
                            table = 'PlayersShotOverallRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShotOverallRange', conn, if_exists='append', index=False)
                        elif GenRan == 'Catch and Shoot':
                            table = 'PlayersShotCandS_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShotCandS', conn, if_exists='append', index=False)
                        elif GenRan == 'Pullups':
                            table = 'PlayersShotPullups_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShotPullups', conn, if_exists='append', index=False)
                        elif GenRan == 'Less Than 10 ft':
                            table = 'PlayersShot10FeetRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShot10FeetRange', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralRange)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersShotOverallRange')
        create_index('Player', 'Offense', 'PlayersShotCandS')
        create_index('Player', 'Offense', 'PlayersShotPullups')
        create_index('Player', 'Offense', 'PlayersShot10FeetRange')
        print('All the indexes have been created')
        print('PlayersShotGeneralRange inserted')

    # 10 - Players Shots Dashboard - Dribble Range
    elif url == 'https://stats.nba.com/stats/leaguedashplayerptshot' and typestat == 'DribbleRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for DriRan in DribbleRange:
                    request_parameters['params'][9]['Season'] = Sea
                    request_parameters['params'][9]['SeasonType'] = Typ
                    request_parameters['params'][9]['DribbleRange'] = DriRan
                    param = request_parameters['params'][9]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['DribbleRange'] = DriRan
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DribbleRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('DribbleRange')
                        if DriRan == '0 Dribbles':
                            table = 'PlayersShot0DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShot0DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '1 Dribble':
                            table = 'PlayersShot1DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShot1DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '2 Dribbles':
                            table = 'PlayersShot2DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShot2DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '3-6 Dribbles':
                            table = 'PlayersShot3_6DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShot3_6DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '7+ Dribbles':
                            table = 'PlayersShot7DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShot7DribbleRange', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DribbleRange)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersShot0DribbleRange')
        create_index('Player', 'Offense', 'PlayersShot1DribbleRange')
        create_index('Player', 'Offense', 'PlayersShot2DribbleRange')
        create_index('Player', 'Offense', 'PlayersShot3_6DribbleRange')
        create_index('Player', 'Offense', 'PlayersShot7DribbleRange')
        print('All the indexes have been created')
        print('PlayersShotDribbleRange inserted')

    # 11 - Players Shots Dashboard - Touch Time Range
    elif url == 'https://stats.nba.com/stats/leaguedashplayerptshot' and typestat == 'TouchTimeRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for TouRan in TouchTimeRange:
                    request_parameters['params'][10]['Season'] = Sea
                    request_parameters['params'][10]['SeasonType'] = Typ
                    request_parameters['params'][10]['TouchTimeRange'] = TouRan
                    param = request_parameters['params'][10]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['TouchTimeRange'] = TouRan
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(TouchTimeRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('TouchTimeRange')
                        if TouRan == 'Touch < 2 Seconds':
                            table = 'PlayersShotTouchTimeLT2Sec_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShotTouchTimeLT2Sec', conn, if_exists='append', index=False)
                        elif TouRan == 'Touch 2-6 Seconds':
                            table = 'PlayersShotTouchTime2_6Sec_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShotTouchTime2_6Sec', conn, if_exists='append', index=False)
                        elif TouRan == 'Touch 6+ Seconds':
                            table = 'PlayersShotTouchTime6Sec_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersShotTouchTime6Sec', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(TouchTimeRange)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersShotTouchTimeLT2Sec')
        create_index('Player', 'Offense', 'PlayersShotTouchTime2_6Sec')
        create_index('Player', 'Offense', 'PlayersShotTouchTime6Sec')
        print('All the indexes have been created')
        print('PlayersShotDribbleRange inserted')

    # 12 - Players Shots Dashboard - Defense
    elif url == 'https://stats.nba.com/stats/leaguedashplayerptshot' and typestat == 'CloseDefDistRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for ClosDef in CloseDefDistRange:
                    request_parameters['params'][11]['Season'] = Sea
                    request_parameters['params'][11]['SeasonType'] = Typ
                    request_parameters['params'][11]['CloseDefDistRange'] = ClosDef
                    param = request_parameters['params'][11]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['CloseDefDistRange'] = ClosDef
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(CloseDefDistRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('CloseDefDistRange')
                        if ClosDef == '0-2 Feet - Very Tight':
                            table = 'PlayersCloseDefDist_0_2_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersCloseDefDist_0_2', conn, if_exists='append', index=False)
                        elif ClosDef == '2-4 Feet - Tight':
                            table = 'PlayersCloseDefDist_2_4_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersCloseDefDist_2_4', conn, if_exists='append', index=False)
                        elif ClosDef == '4-6 Feet - Open':
                            table = 'PlayersCloseDefDist_4_6_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersCloseDefDist_4_6', conn, if_exists='append', index=False)
                        elif ClosDef == '6+ Feet - Wide Open':
                            table = 'PlayersCloseDefDist_6_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('PlayersCloseDefDist_6', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(CloseDefDistRange)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersCloseDefDist_0_2')
        create_index('Player', 'Offense', 'PlayersCloseDefDist_2_4')
        create_index('Player', 'Offense', 'PlayersCloseDefDist_4_6')
        create_index('Player', 'Offense', 'PlayersCloseDefDist_6')
        print('All the indexes have been created')
        print('PlayersCloseDefDistRange inserted')

    # 13 - Players Shot Location
    elif url == 'https://stats.nba.com/stats/leaguedashplayershotlocations' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for MeaTyp in MeasureType:
                    request_parameters['params'][12]['Season'] = Sea
                    request_parameters['params'][12]['SeasonType'] = Typ
                    request_parameters['params'][12]['MeasureType'] = MeaTyp
                    param = request_parameters['params'][12]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets']['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['MeasureType'] = MeaTyp
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                        i += 1
                    else:
                        col = ['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'AGE',
                               'FGM _ Less Than 5 ft.', 'FGA _ Less Than 5 ft.', 'FG_PCT _ Less Than 5 ft.',
                               'FGM _ 5_9 ft.', 'FGA _ 5_9 ft.', 'FG_PCT _ 5_9 ft.', 'FGM _ 10_14 ft.',
                               'FGA _ 10_14 ft.', 'FG_PCT _ 10_14 ft.', 'FGM _ 15_19 ft.', 'FGA _ 15_19 ft.',
                               'FG_PCT _ 15_19 ft.', 'FGM _ 20_24 ft.', 'FGA _ 20_24 ft.', 'FG_PCT _ 20_24 ft.',
                               'FGM _ 25_29 ft.', 'FGA _ 25_29 ft.', 'FG_PCT _ 25_29 ft.', 'FGM _ 30_34 ft.',
                               'FGA _ 30_34 ft.', 'FG_PCT _ 30_34 ft.', 'FGM _ 35_39 ft.', 'FGA _ 35_39 ft.',
                               'FG_PCT _ 35_39 ft.', 'FGM _ 40+ ft.', 'FGA _ 40+ ft.', 'FG_PCT _ 40+ ft.', 'Season',
                               'SeasonType', 'MeasureType']
                        table = 'PlayersShotLocation_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('PlayersShotLocation', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                        i += 1
                        time.sleep(1)
        create_index('Player', 'Offense', 'PlayersShotLocation')
        print('All the indexes have been created')
        print('PlayersShotLocation inserted')

    # 14 - Players Hustles Stats
    elif url == 'https://stats.nba.com/stats/leaguehustlestatsplayer' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                request_parameters['params'][13]['Season'] = Sea
                request_parameters['params'][13]['SeasonType'] = Typ
                param = request_parameters['params'][13]
                data = requests.get(url=url, headers=header, params=param).json()
                dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                dataframe['Season'] = Sea
                dataframe['SeasonType'] = Typ
                if dataframe.empty:
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                else:
                    col = data['resultSets'][0]['headers']
                    col.append('Season')
                    col.append('SeasonType')
                    table = 'PlayersHustleStats_'
                    table_col = [table + x for x in col]
                    dataframe.columns = table_col
                    dataframe.to_sql('PlayersHustleStats', conn, if_exists='append', index=False)
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                    time.sleep(1)
        create_index('Player', 'Offense', 'PlayersHustleStats')
        print('All the indexes have been created')
        print('PlayersHustleStats inserted')


def get_teams_data(url, typestat):

    i = 1  # Initiating the iterator to know how many lines left to import

    # Lists parameters needed for each request

    Seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21']
    SeasonType = ['Regular Season', 'Playoffs']
    MeasureType = ['Base', 'Advanced', 'Four Factors', 'Scoring', 'Misc', 'Opponent']
    Playtypes = ['Misc', 'OffRebound', 'OffScreen', 'Cut', 'Handoff', 'Spotup', 'Postup', 'PRBallHandler', 'PRRollman',
                 'Isolation', 'Transition']
    PtMeasureType = ['Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding',
                     'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch']
    DefenseCategory = ['3 Pointers', '2 Pointers', 'Less Than 6Ft', 'Less Than 10Ft', 'Greater Than 15Ft']
    GeneralRange = ['Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft']
    DribbleRange = ['0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles']
    TouchTimeRange = ['Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds']
    CloseDefDistRange = ['0-2 Feet - Very Tight', '2-4 Feet - Tight', '4-6 Feet - Open', '6+ Feet - Wide Open']

    # Parameters needed in the request made

    request_parameters = {
        'params': [
            # 1
            {'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '',
             'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': MeasureType, 'Month': '0',
             'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame',
             'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N', 'Rank': 'N',
             'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType, 'ShotClockRange': '', 'StarterBench': '',
             'TeamID': '0', 'TwoWay': '0', 'VsConference': '', 'VsDivision': ''}
            # 2
            , {'LeagueID': '00', 'Season': Seasons, 'SeasonType': SeasonType}
            # 3
            , {'AheadBehind': 'Ahead or Behind', 'ClutchTime': 'Last 5 Minutes', 'Conference': '', 'DateFrom': '',
               'DateTo': '', 'Division': '', 'GameScope': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00',
               'Location': '', 'MeasureType': MeasureType, 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '',
               'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlayerExperience': '',
               'PlayerPosition': '', 'PlusMinus': 'N', 'PointDiff': '5', 'Rank': 'N', 'Season': Seasons,
               'SeasonSegment': '', 'SeasonType': SeasonType, 'ShotClockRange': '', 'StarterBench': '', 'TeamID': '0',
               'VsConference': '', 'VsDivision': ''}
            # 4
            , {'LeagueID': '00', 'PerMode': 'PerGame', 'PlayType': Playtypes, 'PlayerOrTeam': 'T',
               'SeasonType': SeasonType, 'SeasonYear': Seasons, 'TypeGrouping': 'offensive'}
            # 5
            , {'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '', 'Division': '',
               'DraftPick': '', 'DraftYear': '', 'GameScope': '', 'Height': '', 'LastNGames': '0', 'LeagueID': '00',
               'Location': '', 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PerMode': 'PerGame',
               'PlayerExperience': '', 'PlayerOrTeam': 'Team', 'PlayerPosition': '', 'PtMeasureType': PtMeasureType,
               'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType, 'StarterBench': '', 'TeamID': '0',
               'VsConference': '', 'VsDivision': '', 'Weight': ''}
            # 6
            , {'Conference': '', 'DateFrom': '', 'DateTo': '', 'DefenseCategory': DefenseCategory, 'Division': '',
               'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'Month': '0',
               'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PerMode': 'PerGame', 'Period': '0',
               'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType, 'TeamID': '0', 'VsConference': '',
               'VsDivision': ''}
            # 7
            , {'CloseDefDistRange': '', 'College': '', 'Conference': '', 'Country': '', 'DateFrom': '', 'DateTo': '',
               'Division': '', 'DraftPick': '', 'DraftYear': '', 'DribbleRange': '', 'GameScope': '', 'GameSegment': '',
               'GeneralRange': GeneralRange, 'Height': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
               'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N',
               'PerMode': 'PerGame', 'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '', 'PlusMinus': 'N',
               'Rank': 'N', 'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType, 'ShotClockRange': '',
               'ShotDistRange': '', 'StarterBench': '', 'TeamID': '0', 'TouchTimeRange': '', 'VsConference': '',
               'VsDivision': '', 'Weight': ''}
            # 8
            , {'DribbleRange': DribbleRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0', 'OpponentTeamID': '0',
               'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N',
               'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 9
            , {'TouchTimeRange:': TouchTimeRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0',
               'OpponentTeamID': '0', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
               'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 10
            , {'CloseDefDistRange': CloseDefDistRange, 'LastNGames': '0', 'LeagueID': '00', 'Month': '0',
               'OpponentTeamID': '0', 'PORound': '0', 'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0',
               'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonType': SeasonType, 'TeamID': '0'}
            # 11
            , {'Conference': '', 'DateFrom': '', 'DateTo': '', 'DistanceRange': '5ft Range', 'Division': '',
               'GameScope': '', 'GameSegment': '', 'LastNGames': '0', 'LeagueID': '00', 'Location': '',
               'MeasureType': 'Base', 'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0',
               'PaceAdjust': 'N', 'PerMode': 'PerGame', 'Period': '0', 'PlayerExperience': '', 'PlayerPosition': '',
               'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonSegment': '', 'SeasonType': SeasonType,
               'ShotClockRange': '', 'StarterBench': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}
            # 12
            , {'LastNGames': '0', 'LeagueID': '00', 'Month': '0', 'OpponentTeamID': '0', 'PORound': '0',
               'PaceAdjust': 'N', 'PerMode': 'PerGame', 'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons,
               'SeasonType': SeasonType, 'TeamID': '0'}

        ]
    }

    # Fixed header for each parameters

    header = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
        'origin': 'https://www.nba.com',
        'referer': 'https://www.nba.com/',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }

    # 1 - Teams General Traditional Stats
    if url == 'https://stats.nba.com/stats/leaguedashteamstats' and typestat == '':
        for Sea in Seasons:  # Allow the code to run through every year at each iteration
            for Typ in SeasonType:  # Run through the season type (Playoffs or regular at each iteration
                for MeaTyp in MeasureType:
                    request_parameters['params'][0]['Season'] = Sea  # Replace value for each season at each iteration
                    request_parameters['params'][0][
                        'SeasonType'] = Typ  # Replace value for season types at each iteration
                    request_parameters['params'][0]['MeasureType'] = MeaTyp
                    param = request_parameters['params'][0]  # Set the good parameter based on the url given
                    data = requests.get(url=url, headers=header, params=param).json()  # Get data from request
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])  # Convert datas to DataFrame
                    dataframe['Season'] = Sea  # Adding a new column 'Season' to DataFrame
                    dataframe['SeasonType'] = Typ  # Adding a new column 'SeasonType' to DataFrame
                    dataframe['MeasureType'] = MeaTyp  # Adding a new column 'MeasureType' to DataFrame
                    if dataframe.empty:  # If dataframe is empty, it means that there aren't data left to get
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(
                            MeasureType)))  # Shows the number of iteration made/left
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']  # Get columns from the request made
                        col.append('Season')  # Adding a new column 'Season' to DataFrame
                        col.append('SeasonType')  # Adding a new column 'SeasonType' to DataFrame
                        col.append('MeasureType')  # Adding a new column 'MeasureType' to DataFrame
                        if MeaTyp == 'Base':
                            table = 'TeamsTraditionalStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTraditionalStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Advanced':
                            table = 'TeamsAdvancedStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsAdvancedStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Four Factors':
                            table = 'TeamsFourFactorsStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsFourFactorsStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Scoring':
                            table = 'TeamsScoringStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsScoringStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Misc':
                            table = 'TeamsMiscStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsMiscStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Opponent':
                            table = 'TeamsOpponentStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsOpponentStats', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                        i += 1
                        time.sleep(1)  # Forced to put this, or the NBA.com website would block my requests
        create_index('Team', '', 'TeamsTraditionalStats')
        create_index('Team', '', 'TeamsAdvancedStats')
        create_index('Team', '', 'TeamsFourFactorsStats')
        create_index('Team', '', 'TeamsScoringStats')
        create_index('Team', '', 'TeamsMiscStats')
        create_index('Team', '', 'TeamsOpponentStats')
        print('All the indexes have been created')
        print('TeamsTraditionalStats inserted')

    # 2 - Teams Estimated Metrics
    elif url == 'https://stats.nba.com/stats/teamestimatedmetrics' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                request_parameters['params'][1]['Season'] = Sea
                request_parameters['params'][1]['SeasonType'] = Typ
                param = request_parameters['params'][1]
                data = requests.get(url=url, headers=header, params=param).json()
                dataframe = pd.DataFrame(data['resultSet']['rowSet'])
                dataframe['Season'] = Sea
                dataframe['SeasonType'] = Typ
                if dataframe.empty:
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                else:
                    col = data['resultSet']['headers']
                    col.append('Season')
                    col.append('SeasonType')
                    table = 'TeamsEstimatedMetrics_'
                    table_col = [table + x for x in col]
                    dataframe.columns = table_col
                    dataframe.to_sql('TeamsEstimatedMetrics', conn, if_exists='append', index=False)
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                    time.sleep(1)
        create_index('Team', '', 'TeamsEstimatedMetrics')
        print('All the indexes have been created')
        print('TeamsEstimatedMetrics inserted')

    # 3 - Teams Clutch Stats
    elif url == 'https://stats.nba.com/stats/leaguedashteamclutch' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for MeaTyp in MeasureType:
                    request_parameters['params'][2]['Season'] = Sea
                    request_parameters['params'][2][
                        'SeasonType'] = Typ
                    request_parameters['params'][2]['MeasureType'] = MeaTyp
                    param = request_parameters['params'][2]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['MeasureType'] = MeaTyp
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('MeasureType')
                        dataframe.columns = col
                        if MeaTyp == 'Base':
                            table = 'TeamsTraditionalClutchStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTraditionalClutchStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Advanced':
                            table = 'TeamsAdvancedClutchStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsAdvancedClutchStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Four Factors':
                            table = 'TeamsFourFactorsClutchStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsFourFactorsClutchStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Scoring':
                            table = 'TeamsScoringClutchStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsScoringClutchStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Misc':
                            table = 'TeamsMiscClutchStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsMiscClutchStats', conn, if_exists='append', index=False)
                        elif MeaTyp == 'Opponent':
                            table = 'TeamsOpponentClutchStats_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsOpponentClutchStats', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsTraditionalClutchStats')
        create_index('Team', '', 'TeamsAdvancedClutchStats')
        create_index('Team', '', 'TeamsFourFactorsClutchStats')
        create_index('Team', '', 'TeamsScoringClutchStats')
        create_index('Team', '', 'TeamsMiscClutchStats')
        create_index('Team', '', 'TeamsOpponentClutchStats')
        print('All the indexes have been created')
        print('TeamsTraditionalClutchStats inserted')

    # 4 - Teams Playtypes Stats
    elif url == 'https://stats.nba.com/stats/synergyplaytypes' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for PlayTy in Playtypes:
                    request_parameters['params'][3]['SeasonYear'] = Sea
                    request_parameters['params'][3]['SeasonType'] = Typ
                    request_parameters['params'][3]['PlayType'] = PlayTy
                    param = request_parameters['params'][3]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['SeasonYear'] = Sea
                    dataframe['SeasonType'] = Typ
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(Playtypes)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('SeasonYear')
                        col.append('SeasonType')
                        if PlayTy == 'Misc':
                            table = 'TeamsPlaytypes_Misc_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Misc', conn, if_exists='append', index=False)
                        elif PlayTy == 'OffRebound':
                            table = 'TeamsPlaytypes_OffRebound_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_OffRebound', conn, if_exists='append', index=False)
                        elif PlayTy == 'OffScreen':
                            table = 'TeamsPlaytypes_OffScreenc_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_OffScreen', conn, if_exists='append', index=False)
                        elif PlayTy == 'Cut':
                            table = 'TeamsPlaytypes_Cut_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Cut', conn, if_exists='append', index=False)
                        elif PlayTy == 'Handoff':
                            table = 'TeamsPlaytypes_Handoff_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Handoff', conn, if_exists='append', index=False)
                        elif PlayTy == 'Spotup':
                            table = 'TeamsPlaytypes_Spotup_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Spotup', conn, if_exists='append', index=False)
                        elif PlayTy == 'Postup':
                            table = 'TeamsPlaytypes_Postup_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Postup', conn, if_exists='append', index=False)
                        elif PlayTy == 'PRBallHandler':
                            table = 'TeamsPlaytypes_PRBallHandler_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_PRBallHandler', conn, if_exists='append', index=False)
                        elif PlayTy == 'PRRollman':
                            table = 'TeamsPlaytypes_PRRollman_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_PRRollman', conn, if_exists='append', index=False)
                        elif PlayTy == 'Isolation':
                            table = 'TeamsPlaytypes_Isolation_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Isolation', conn, if_exists='append', index=False)
                        elif PlayTy == 'Transition':
                            table = 'TeamsPlaytypes_Transition_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPlaytypes_Transition', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(Playtypes)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsPlaytypes_Misc')
        create_index('Team', '', 'TeamsPlaytypes_Transition')
        create_index('Team', '', 'TeamsPlaytypes_Isolation')
        create_index('Team', '', 'TeamsPlaytypes_PRRollman')
        create_index('Team', '', 'TeamsPlaytypes_PRBallHandler')
        create_index('Team', '', 'TeamsPlaytypes_Postup')
        create_index('Team', '', 'TeamsPlaytypes_Spotup')
        create_index('Team', '', 'TeamsPlaytypes_OffRebound')
        create_index('Team', '', 'TeamsPlaytypes_OffScreen')
        create_index('Team', '', 'TeamsPlaytypes_Cut')
        create_index('Team', '', 'TeamsPlaytypes_Handoff')
        print('All the indexes have been created')
        print('TeamsPlaytypes inserted')

    # 5 - Teams Tracking Data
    elif url == 'https://stats.nba.com/stats/leaguedashptstats' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for PtMeaTy in PtMeasureType:
                    request_parameters['params'][4]['Season'] = Sea
                    request_parameters['params'][4]['SeasonType'] = Typ
                    request_parameters['params'][4]['PtMeasureType'] = PtMeaTy
                    param = request_parameters['params'][4]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['PtMeasureType'] = PtMeaTy
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(PtMeasureType)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('PtMeasureType')
                        if PtMeaTy == 'Drives':
                            table = 'TeamsTrackingDrives_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingDrives', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Defense':
                            table = 'TeamsTrackingDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingDefense', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'CatchShoot':
                            table = 'TeamsTrackingCatchShoot_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingCatchShoot', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Passing':
                            table = 'TeamsTrackingPassing_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingPassing', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Possessions':
                            table = 'TeamsTrackingPossessions_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingPossessions', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'PullUpShot':
                            table = 'TeamsTrackingPullUpShot_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingPullUpShot', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Rebounding':
                            table = 'TeamsTrackingRebounding_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingRebounding', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'Efficiency':
                            table = 'TeamsTrackingEfficiency_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingEfficiency', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'SpeedDistance':
                            table = 'TeamsTrackingSpeedDistance_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingSpeedDistance', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'ElbowTouch':
                            table = 'TeamsTrackingElbowTouch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingElbowTouch', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'PostTouch':
                            table = 'TeamsTrackingPostTouch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingPostTouch', conn, if_exists='append', index=False)
                        elif PtMeaTy == 'PaintTouch':
                            table = 'TeamsTrackingPaintTouch_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsTrackingPaintTouch', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(PtMeasureType)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsTrackingDrives')
        create_index('Team', '', 'TeamsTrackingDefense')
        create_index('Team', '', 'TeamsTrackingCatchShoot')
        create_index('Team', '', 'TeamsTrackingPassing')
        create_index('Team', '', 'TeamsTrackingPossessions')
        create_index('Team', '', 'TeamsTrackingPullUpShot')
        create_index('Team', '', 'TeamsTrackingRebounding')
        create_index('Team', '', 'TeamsTrackingEfficiency')
        create_index('Team', '', 'TeamsTrackingSpeedDistance')
        create_index('Team', '', 'TeamsTrackingElbowTouch')
        create_index('Team', '', 'TeamsTrackingPostTouch')
        create_index('Team', '', 'TeamsTrackingPaintTouch')
        print('All the indexes have been created')
        print('TeamsTrackingData inserted')

    # 6 - Teams Defense Dashboard
    elif url == 'https://stats.nba.com/stats/leaguedashptteamdefend' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                for DefCat in DefenseCategory:
                    request_parameters['params'][5]['Season'] = Sea
                    request_parameters['params'][5]['SeasonType'] = Typ
                    request_parameters['params'][5]['DefenseCategory'] = DefCat
                    param = request_parameters['params'][5]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['DefenseCategory'] = DefCat
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DefenseCategory)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('DefenseCategory')
                        if DefCat == '3 Pointers':
                            table = 'Teams3ptsDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('Teams3ptsDefense', conn, if_exists='append', index=False)
                        elif DefCat == '2 Pointers':
                            table = 'Teams2ptsDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('Teams2ptsDefense', conn, if_exists='append', index=False)
                        elif DefCat == 'Less Than 6Ft':
                            table = 'TeamsPaintDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsPaintDefense', conn, if_exists='append', index=False)
                        elif DefCat == 'Less Than 10Ft':
                            table = 'TeamsOutsidePaintDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsOutsidePaintDefense', conn, if_exists='append', index=False)
                        elif DefCat == 'Greater Than 15Ft':
                            table = 'TeamsFarFromBasketDefense_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsFarFromBasketDefense', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DefenseCategory)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'Teams3ptsDefense')
        create_index('Team', '', 'Teams2ptsDefense')
        create_index('Team', '', 'TeamsPaintDefense')
        create_index('Team', '', 'TeamsOutsidePaintDefense')
        create_index('Team', '', 'TeamsFarFromBasketDefense')
        print('All the indexes have been created')
        print('TeamsDefenseDashboard inserted')

    # 7 - Teams Shot Dashboard
    elif url == 'https://stats.nba.com/stats/leaguedashteamptshot' and typestat == 'GeneralRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for GenRan in GeneralRange:
                    request_parameters['params'][6]['Season'] = Sea
                    request_parameters['params'][6]['SeasonType'] = Typ
                    request_parameters['params'][6]['GeneralRange'] = GenRan
                    param = request_parameters['params'][6]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['GeneralRange'] = GenRan
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('GeneralRange')
                        if GenRan == 'Overall':
                            table = 'TeamsShotOverallRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShotOverallRange', conn, if_exists='append', index=False)
                        elif GenRan == 'Catch and Shoot':
                            table = 'TeamsShotCandS_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShotCandS', conn, if_exists='append', index=False)
                        elif GenRan == 'Pullups':
                            table = 'TeamsShotPullups_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShotPullups', conn, if_exists='append', index=False)
                        elif GenRan == 'Less Than 10 ft':
                            table = 'TeamsShot10FeetRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShot10FeetRange', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(GeneralRange)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsShotOverallRange')
        create_index('Team', '', 'TeamsShotCandS')
        create_index('Team', '', 'TeamsShotPullups')
        create_index('Team', '', 'TeamsShot10FeetRange')
        print('All the indexes have been created')
        print('TeamsShotGeneralRange inserted')

    # 8 - Teams Shots Dashboard - Dribble Range
    elif url == 'https://stats.nba.com/stats/leaguedashteamptshot' and typestat == 'DribbleRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for DriRan in DribbleRange:
                    request_parameters['params'][7]['Season'] = Sea
                    request_parameters['params'][7]['SeasonType'] = Typ
                    request_parameters['params'][7]['DribbleRange'] = DriRan
                    param = request_parameters['params'][7]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['DribbleRange'] = DriRan
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DribbleRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('DribbleRange')
                        if DriRan == '0 Dribbles':
                            table = 'TeamsShot0DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShot0DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '1 Dribble':
                            table = 'TeamsShot1DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShot1DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '2 Dribbles':
                            table = 'TeamsShot2DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShot2DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '3-6 Dribbles':
                            table = 'TeamsShot3_6DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShot3_6DribbleRange', conn, if_exists='append', index=False)
                        elif DriRan == '7+ Dribbles':
                            table = 'TeamsShot7DribbleRange_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShot7DribbleRange', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(DribbleRange)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsShot0DribbleRange')
        create_index('Team', '', 'TeamsShot1DribbleRange')
        create_index('Team', '', 'TeamsShot2DribbleRange')
        create_index('Team', '', 'TeamsShot3_6DribbleRange')
        create_index('Team', '', 'TeamsShot7DribbleRange')
        print('All the indexes have been created')
        print('TeamsShotDribbleRange inserted')

    # 9 - Teams Shots Dashboard - Touch Time Range
    elif url == 'https://stats.nba.com/stats/leaguedashteamptshot' and typestat == 'TouchTimeRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for TouRan in TouchTimeRange:
                    request_parameters['params'][8]['Season'] = Sea
                    request_parameters['params'][8]['SeasonType'] = Typ
                    request_parameters['params'][8]['TouchTimeRange'] = TouRan
                    param = request_parameters['params'][8]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['TouchTimeRange'] = TouRan
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(TouchTimeRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('TouchTimeRange')
                        if TouRan == 'Touch < 2 Seconds':
                            table = 'TeamsShotTouchTimeLT2Sec_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShotTouchTimeLT2Sec', conn, if_exists='append', index=False)
                        elif TouRan == 'Touch 2-6 Seconds':
                            table = 'TeamsShotTouchTime2_6Sec_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShotTouchTime2_6Sec', conn, if_exists='append', index=False)
                        elif TouRan == 'Touch 6+ Seconds':
                            table = 'TeamsShotTouchTime6Sec_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsShotTouchTime6Sec', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(TouchTimeRange)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsShotTouchTimeLT2Sec')
        create_index('Team', '', 'TeamsShotTouchTime2_6Sec')
        create_index('Team', '', 'TeamsShotTouchTime6Sec')
        print('All the indexes have been created')
        print('TeamsShotTouchTimeRange inserted')

    # 10 - Teams Shots Dashboard - Defense
    elif url == 'https://stats.nba.com/stats/leaguedashteamptshot' and typestat == 'CloseDefDistRange':
        for Sea in Seasons:
            for Typ in SeasonType:
                for ClosDef in CloseDefDistRange:
                    request_parameters['params'][9]['Season'] = Sea
                    request_parameters['params'][9]['SeasonType'] = Typ
                    request_parameters['params'][9]['CloseDefDistRange'] = ClosDef
                    param = request_parameters['params'][9]
                    data = requests.get(url=url, headers=header, params=param).json()
                    dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                    dataframe['Season'] = Sea
                    dataframe['SeasonType'] = Typ
                    dataframe['CloseDefDistRange'] = ClosDef
                    if dataframe.empty:
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(CloseDefDistRange)))
                        i += 1
                    else:
                        col = data['resultSets'][0]['headers']
                        col.append('Season')
                        col.append('SeasonType')
                        col.append('CloseDefDistRange')
                        if ClosDef == '0-2 Feet - Very Tight':
                            table = 'TeamsCloseDefDist_0_2_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsCloseDefDist_0_2', conn, if_exists='append', index=False)
                        elif ClosDef == '2-4 Feet - Tight':
                            table = 'TeamsCloseDefDist_2_4_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsCloseDefDist_2_4', conn, if_exists='append', index=False)
                        elif ClosDef == '4-6 Feet - Open':
                            table = 'TeamsCloseDefDist_4_6_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsCloseDefDist_4_6', conn, if_exists='append', index=False)
                        elif ClosDef == '6+ Feet - Wide Open':
                            table = 'TeamsCloseDefDist_6_'
                            table_col = [table + x for x in col]
                            dataframe.columns = table_col
                            dataframe.to_sql('TeamsCloseDefDist_6', conn, if_exists='append', index=False)
                        print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(CloseDefDistRange)))
                        i += 1
                        time.sleep(1)
        create_index('Team', '', 'TeamsCloseDefDist_0_2')
        create_index('Team', '', 'TeamsCloseDefDist_2_4')
        create_index('Team', '', 'TeamsCloseDefDist_4_6')
        create_index('Team', '', 'TeamsCloseDefDist_6')
        print('All the indexes have been created')
        print('TeamsCloseDefDistRange inserted')

    # 11 - Shot Teams Location
    elif url == 'https://stats.nba.com/stats/leaguedashteamshotlocations' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                request_parameters['params'][10]['Season'] = Sea
                request_parameters['params'][10]['SeasonType'] = Typ
                param = request_parameters['params'][10]
                data = requests.get(url=url, headers=header, params=param).json()
                dataframe = pd.DataFrame(data['resultSets']['rowSet'])
                dataframe['Season'] = Sea
                dataframe['SeasonType'] = Typ
                if dataframe.empty:
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                else:
                    col = ['TEAM_ID', 'TEAM_NAME', 'FGM _ Less Than 5 ft.', 'FGA _ Less Than 5 ft.',
                           'FG_PCT _ Less Than 5 ft.', 'FGM _ 5_9 ft.', 'FGA _ 5_9 ft.', 'FG_PCT _ 5_9 ft.',
                           'FGM _ 10_14 ft.', 'FGA _ 10_14 ft.', 'FG_PCT _ 10_14 ft.', 'FGM _ 15_19 ft.',
                           'FGA _ 15_19 ft.', 'FG_PCT _ 15_19 ft.', 'FGM _ 20_24 ft.', 'FGA _ 20_24 ft.',
                           'FG_PCT _ 20_24 ft.', 'FGM _ 25_29 ft.', 'FGA _ 25_29 ft.', 'FG_PCT _ 25_29 ft.',
                           'FGM _ 30_34 ft.', 'FGA _ 30_34 ft.', 'FG_PCT _ 30_34 ft.', 'FGM _ 35_39 ft.',
                           'FGA _ 35_39 ft.', 'FG_PCT _ 35_39 ft.', 'FGM _ 40+ ft.', 'FGA _ 40+ ft.',
                           'FG_PCT _ 40+ ft.', 'Season', 'SeasonType']
                    table = 'TeamsShotLocation_'
                    table_col = [table + x for x in col]
                    dataframe.columns = table_col
                    dataframe.to_sql('TeamsShotLocation', conn, if_exists='append', index=False)
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                    time.sleep(1)
        create_index('Team', '', 'TeamsShotLocation')
        print('All the indexes have been created')
        print('TeamsShotLocation inserted')

    # 12 - Hustle Teams Stats
    elif url == 'https://stats.nba.com/stats/leaguehustlestatsteam' and typestat == '':
        for Sea in Seasons:
            for Typ in SeasonType:
                request_parameters['params'][11]['Season'] = Sea
                request_parameters['params'][11]['SeasonType'] = Typ
                param = request_parameters['params'][11]
                data = requests.get(url=url, headers=header, params=param).json()
                dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                dataframe['Season'] = Sea
                dataframe['SeasonType'] = Typ
                if dataframe.empty:
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                else:
                    col = data['resultSets'][0]['headers']
                    col.append('Season')
                    col.append('SeasonType')
                    table = 'TeamsHustleStats_'
                    table_col = [table + x for x in col]
                    dataframe.columns = table_col
                    dataframe.to_sql('TeamsHustleStats', conn, if_exists='append', index=False)
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType)))
                    i += 1
                    time.sleep(1)
        create_index('Team', '', 'TeamsHustleStats')
        print('All the indexes have been created')
        print('TeamsHustleStats inserted')


def get_lineups_data(url):
    i = 1

    MeasureType = ['Base', 'Four Factors', 'Scoring', 'Advanced', 'Misc', 'Opponent']
    Seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21']
    SeasonType = ['Regular Season', 'Playoffs']

    header = {'Accept': 'application/json, text/plain, */*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
              'Connection': 'keep-alive',
              'Host': 'stats.nba.com',
              'Origin': 'https://www.nba.com',
              'Referer': 'https://www.nba.com/',
              'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
              'sec-ch-ua-mobile': '?0',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-site',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
              'x-nba-stats-origin': 'stats',
              'x-nba-stats-token': 'true'}


    request_parameters = {'param' : [{'Conference': '', 'DateFrom': '', 'DateTo': '', 'Division': '', 'GameID': '', 'GameSegment': '',
              'GroupQuantity': '5', 'LastNGames': '0', 'LeagueID': '00', 'Location': '', 'MeasureType': MeasureType,
              'Month': '0', 'OpponentTeamID': '0', 'Outcome': '', 'PORound': '0', 'PaceAdjust': 'N',
              'PerMode': 'PerGame', 'Period': '0', 'PlusMinus': 'N', 'Rank': 'N', 'Season': Seasons, 'SeasonSegment': '',
              'SeasonType': SeasonType, 'ShotClockRange': '', 'TeamID': '0', 'VsConference': '', 'VsDivision': ''}]}

    for Sea in Seasons:
        for Typ in SeasonType:
            for MeaTyp in MeasureType:
                request_parameters['param'][0]['Season'] = Sea
                request_parameters['param'][0]['SeasonType'] = Typ
                request_parameters['param'][0]['MeasureType'] = MeaTyp
                param = request_parameters['param'][0]
                data = requests.get(url=url, headers=header, params=param).json()
                dataframe = pd.DataFrame(data['resultSets'][0]['rowSet'])
                dataframe['Season'] = Sea
                dataframe['SeasonType'] = Typ
                dataframe['MeasureType'] = MeaTyp
                if dataframe.empty:
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                    i += 1
                else:
                    col = data['resultSets'][0]['headers']  # Get columns from the request made
                    col.append('Season')  # Adding a new column 'Season' to DataFrame
                    col.append('SeasonType')  # Adding a new column 'SeasonType' to DataFrame
                    col.append('MeasureType')  # Adding a new column 'MeasureType' to DataFrame
                    if MeaTyp == 'Base':
                        table = 'LineupsTraditionalStats_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('LineupsTraditionalStats', conn, if_exists='append', index=False)
                    elif MeaTyp == 'Advanced':
                        table = 'LineupsAdvancedStats_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('LineupsAdvancedStats', conn, if_exists='append', index=False)
                    elif MeaTyp == 'Four Factors':
                        table = 'LineupsFourFactorsStats_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('LineupsFourFactorsStats', conn, if_exists='append', index=False)
                    elif MeaTyp == 'Scoring':
                        table = 'LineupsScoringStats_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('LineupsScoringStats', conn, if_exists='append', index=False)
                    elif MeaTyp == 'Misc':
                        table = 'LineupsMiscStats_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('LineupsMiscStats', conn, if_exists='append', index=False)
                    elif MeaTyp == 'Opponent':
                        table = 'LineupsOpponentStats_'
                        table_col = [table + x for x in col]
                        dataframe.columns = table_col
                        dataframe.to_sql('LineupsOpponentStats', conn, if_exists='append', index=False)
                    print(str(i) + '/' + str(len(Seasons) * len(SeasonType) * len(MeasureType)))
                    i += 1
                    time.sleep(1)  # Forced to put this, or the NBA.com website would block my requests
    create_index('Lineups', '', 'LineupsTraditionalStats')
    create_index('Lineups', '', 'LineupsAdvancedStats')
    create_index('Lineups', '', 'LineupsFourFactorsStats')
    create_index('Lineups', '', 'LineupsScoringStats')
    create_index('Lineups', '', 'LineupsMiscStats')
    create_index('Lineups', '', 'LineupsOpponentStats')
    print('All the indexes have been created')
    print('LineupsTraditionalStats inserted')


def clean_dataset(dataset):

    if dataset == 'Players':

        column_not_to_drop = ["PlayersGeneralStats_GP", "PlayersGeneralStats_W", "PlayersGeneralStats_L",
                              "PlayersGeneralStats_W_PCT"]
        column_to_drop = ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "TEAM_ABBREVIATION", "_AGE", "_GP", "_W", "_L", "_W_PCT",
                          "_CFID", "_CFPARAMS", "_Season", "_MeasureType", "_GeneralTypeDetails", "_GROUP_SET",
                          "_TEAM_NAME", "_COURT_STATUS", "_CloseDefDistRange", "_TouchTimeRange", "_DribbleRange",
                          "10FeetRange_FG3_PCT", "_GeneralRange", "_PtMeasureType", "_Playtype", "_SEASON_ID", "_PLAY_TYPE",
                          "_TYPE_GROUPING", "_PLAYER_POSITION", "_DEFENSE_CATEGORY", "_RANK", "_Defense_Category",
                          "_DefenseCategory", "Hustle"]

        query_players = pd.read_sql_query('SELECT * FROM Dataset_Players', conn)
        df = pd.DataFrame(query_players)
        df_columns_players = df.columns.to_list()
        to_add = []
        column_playersbios = [s for s in df_columns_players if "PlayersBios" in s]
        for k in column_playersbios:
            to_add.append(k)
        for j in column_not_to_drop:
            to_add.append(j)
        for z in column_to_drop:
            for y in [s for s in df_columns_players if z in s]:
                df_columns_players.remove(y)
        df_columns_players = to_add + df_columns_players
        main_list = list(set(df.columns.to_list()) - set(df_columns_players))
        df.drop(main_list, axis=1, inplace=True)
        df.to_sql('Dataset_Players_2', conn, if_exists='replace', index=False)

    elif dataset == 'Teams':

        column_to_drop = ["TEAMS_ID", "TEAM_NAME", "TEAM_ID", "TEAM_ABBREVIATION", "_AGE", "_GP", "_W", "_L",
                          "_W_PCT",
                          "_CFID", "_CFPARAMS", "_Season", "_MeasureType", "_GeneralTypeDetails", "_GROUP_SET",
                          "_TEAM_NAME", "_COURT_STATUS", "_CloseDefDistRange", "_TouchTimeRange", "_DribbleRange",
                          "10FeetRange_FG3_PCT", "_GeneralRange", "_PtMeasureType", "_Playtype", "_SEASON_ID",
                          "_PLAY_TYPE",
                          "_TYPE_GROUPING", "_PLAYER_POSITION", "_DEFENSE_CATEGORY", "_RANK", "_Defense_Category",
                          "_DefenseCategory", "Hustle"]

        query_Teams = pd.read_sql_query('SELECT * FROM Dataset_Teams', conn)
        df = pd.DataFrame(query_Teams)
        df_columns_Teams = df.columns.to_list()
        column_not_to_drop = df_columns_Teams[0:26]+df_columns_Teams[56:58]
        to_add = []
        for j in column_not_to_drop:
            to_add.append(j)
        for z in column_to_drop:
            for y in [s for s in df_columns_Teams if z in s]:
                df_columns_Teams.remove(y)
        df_columns_Teams = to_add + df_columns_Teams
        main_list = list(set(df.columns.to_list()) - set(df_columns_Teams))
        df.drop(main_list, axis=1, inplace=True)
        df.to_sql('Dataset_Teams_2', conn, if_exists='replace', index=False)

    elif dataset == 'Lineups':

        column_to_drop = ["TEAMS_ID", "TEAM_NAME", "TEAM_ID", "TEAM_ABBREVIATION", "_AGE", "_GP", "_W", "_L",
                          "_W_PCT",
                          "_CFID", "_CFPARAMS", "_Season", "_MeasureType", "_GeneralTypeDetails", "_GROUP_SET",
                          "_TEAM_NAME", "_COURT_STATUS", "_CloseDefDistRange", "_TouchTimeRange", "_DribbleRange",
                          "10FeetRange_FG3_PCT", "_GeneralRange", "_PtMeasureType", "_Playtype", "_SEASON_ID",
                          "_PLAY_TYPE",
                          "_TYPE_GROUPING", "_PLAYER_POSITION", "_DEFENSE_CATEGORY", "_RANK", "_Defense_Category",
                          "_DefenseCategory", "Hustle", "_GROUP_ID", "_GROUP_NAME"]

        query_Teams = pd.read_sql_query('SELECT * FROM Dataset_Lineups', conn)
        df = pd.DataFrame(query_Teams)
        df_columns_Teams = df.columns.to_list()
        column_not_to_drop = df_columns_Teams[1:30]+df_columns_Teams[57:59]
        to_add = []
        for j in column_not_to_drop:
            to_add.append(j)
        for z in column_to_drop:
            for y in [s for s in df_columns_Teams if z in s]:
                df_columns_Teams.remove(y)
        df_columns_Teams = to_add + df_columns_Teams
        main_list = list(set(df.columns.to_list()) - set(df_columns_Teams))
        df.drop(main_list, axis=1, inplace=True)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        lst = c.execute('select LineupsTraditionalStats_GROUP_ID from Dataset_Lineups').fetchall()
        lst = [e[1:len(e) - 1] for e in lst]
        lst = [w.replace('-', ', ') for w in lst]
        df['LineupsTraditionalStats_GROUP_ID'] = lst
        df.to_sql('Dataset_Lineups_2', conn, if_exists='replace', index=False)
