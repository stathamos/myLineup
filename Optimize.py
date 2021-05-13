import pandas as pd
import Database
import Toolbox as tool


def get_players_with_type():
    df = pd.read_sql_query('SELECT P.PlayersBios_PLAYER_NAME, P.PlayersBios_PLAYER_ID, P.PlayersBios_Season, P.Type, '
                           'CAST(NP.PlayersBios_TEAM_ID as INT) as Team_ID FROM PCA_Dataset_Players P JOIN '
                           'NonNumeric_Dataset_Players NP on P.PlayersBios_PLAYER_ID = NP.PlayersBios_PLAYER_ID WHERE '
                           'P.PlayersBios_Season = "2020-21" and NP.PlayersBios_Season = "2020-21"', Database.conn)
    df.to_sql('Players_with_type', Database.conn, if_exists='replace', index=False)


def get_type_description():
    df = pd.read_sql_query('SELECT P.PlayersBios_PLAYER_NAME, P.PlayersBios_PLAYER_ID, P.PlayersBios_Season, P.Type, '
                           'CAST(NP.PlayersBios_TEAM_ID as INT) as Team_ID FROM PCA_Dataset_Players P JOIN '
                           'NonNumeric_Dataset_Players NP on P.PlayersBios_PLAYER_ID = NP.PlayersBios_PLAYER_ID WHERE '
                           'P.PlayersBios_Season = NP.PlayersBios_Season', Database.conn)
    df_description = pd.read_csv('../DB 100h Proj/PlayersType2.csv', sep=";")
    df_description.sort_values('Types', inplace=True)
    df_description = df.merge(df_description, how='inner', on=['PlayersBios_PLAYER_NAME', 'PlayersBios_Season'])
    df_description.sort_values('Type', inplace=True)
    df_description.drop(['PlayersBios_PLAYER_NAME', 'PlayersBios_PLAYER_ID', 'Types', 'Team_ID', 'PlayersBios_Season']
                        , axis=1, inplace=True)
    df_description.to_sql('Type_description', Database.conn, if_exists='replace', index=False)


def get_teams_lineups():
    team_list = tool.sql_query_to_list('SELECT TeamsTraditionalStats_TEAM_ID FROM NonNumeric_Dataset_Teams where '
                                       'TeamsTraditionalStats_Season = "2020-21" and TeamsTraditionalStats_SeasonType = '
                                       '"Regular Season"')
    for i in team_list:
        df = pd.read_sql_query('SELECT * FROM Players_with_type WHERE Team_ID = "' + str(i) + '"', Database.conn)
        players_id = df['PlayersBios_PLAYER_ID'].to_list()
        players_name = df['PlayersBios_PLAYER_NAME'].to_list()
        lineups_id = tool.combinliste(players_id, 5)
        lineups_name = tool.combinliste(players_name, 5)
        lineups_name = [[x.replace("'", "") for x in l] for l in lineups_name]
        lineuptype = list()
        for p in lineups_id:
            l = list()
            for pid in p:
                p_type = df['Type'].astype(str).str[0].loc[(df['PlayersBios_PLAYER_ID'] == pid)].to_list()
                l.append(p_type[0])
            lineuptype.append(l)
        for j in range(0, len(lineuptype)):
            lineuptype[j].sort()
        team_lineups = pd.DataFrame()
        team_lineups['LineupName'] = lineups_name
        team_lineups['LineupName'] = team_lineups['LineupName'].str.join(', ')
        team_lineups['LineupID'] = lineups_id
        team_lineups['LineupID'] = team_lineups['LineupID'].str.join(', ')
        team_lineups['LineupType'] = lineuptype
        team_lineups['LineupType'] = team_lineups['LineupType'].str.join(', ')
        team_lineups['Team'] = i
        team_lineups.to_sql('Team_Lineups', Database.conn, if_exists='append', index=False)
    print('All the teams lineups have been inserted')


def get_players_boxscore(boxscore):
    boxscore.fillna(value=pd.np.nan, inplace=True)
    col = list(boxscore.columns.values)
    sum_col = col[1:6] + col[7:9] + col[10:12] + col[13:23] + col[34:43] + col[57:59] + col[60:62] + col[63:65] \
              + col[66:]
    mean_col = col[1:3] + col[23:34] + col[43:57]
    pct_col = [col[1]] + [col[6]] + [col[9]] + [col[12]] + [col[59]] + [col[62]] + [col[65]]
    summed_col = boxscore[sum_col].groupby('PlayerName').sum()
    weight_av = pd.DataFrame()
    for a in mean_col[2:]:
        wa = tool.weighted_average(boxscore[mean_col], a, 'Min', 'PlayerName')
        weight_av[a] = wa[a]
    for a in pct_col[1:]:
        if a == 'FG_PCT':
            summed_col[a] = summed_col['FGM'] / summed_col['FGA']
        if a == 'FG3_PCT':
            summed_col[a] = summed_col['FG3M'] / summed_col['FG3A']
        if a == 'FT_PCT':
            summed_col[a] = summed_col['FTM'] / summed_col['FTA']
        if a == 'OPP_FG_PCT':
            summed_col[a] = summed_col['OPP_FGM'] / summed_col['OPP_FGA']
        if a == 'OPP_FG3_PCT':
            summed_col[a] = summed_col['OPP_FG3M'] / summed_col['OPP_FG3A']
        if a == 'OPP_FT_PCT':
            summed_col[a] = summed_col['OPP_FTM'] / summed_col['OPP_FTA']
    boxscore_players = pd.DataFrame(columns=col)
    summed_col[mean_col[2:]] = weight_av
    summed_col.insert(0, 'PlayersBios_TEAM_ABBREVIATION', boxscore.iloc[0][0])
    summed_col.insert(1, 'PlayerName', summed_col.index)
    boxscore_players = boxscore_players.append(summed_col, ignore_index=True)
    return boxscore_players


def optimized_stats_team(data_to_insert):
    col = list(data_to_insert.columns.values)
    serie_to_pivot = pd.Series([data_to_insert.iloc[0][0], 'Lineup'], index=col[:2])
    sum_col = col[3:7] + col[8:10] + col[11:13] + col[14:24] + col[35:44] + col[58:60] + col[61:63] + col[64:66] + col[67:]
    mean_col = col[24:35] + col[44:58]
    pct_col = [col[7]] + [col[10]] + [col[13]] + [col[60]] + [col[63]] + [col[66]]
    wa_serie = pd.Series([])
    pct_serie = pd.Series([])
    summed_col = data_to_insert[sum_col].sum()
    for a in mean_col:
        i = 0
        t = 0
        d = dict()
        while i < len(data_to_insert['Min']):
            t = t + data_to_insert['Min'].iloc[i] * data_to_insert[a].iloc[i]
            i += 1
        d[a] = t / 48
        to_append = pd.Series(d)
        wa_serie = wa_serie.append(to_append)
    for a in pct_col:
        d = dict()
        if a == 'FG_PCT':
            d[a] = summed_col['FGM'] / summed_col['FGA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'FG3_PCT':
            d[a] = summed_col['FG3M'] / summed_col['FG3A']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'FT_PCT':
            d[a] = summed_col['FTM'] / summed_col['FTA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'OPP_FG_PCT':
            d[a] = summed_col['OPP_FGM'] / summed_col['OPP_FGA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'OPP_FG3_PCT':
            d[a] = summed_col['OPP_FG3M'] / summed_col['OPP_FG3A']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
        if a == 'OPP_FT_PCT':
            d[a] = summed_col['OPP_FTM'] / summed_col['OPP_FTA']
            to_append = pd.Series(d)
            pct_serie = pct_serie.append(to_append)
    serie_to_pivot = serie_to_pivot.append(pct_serie)
    serie_to_pivot = serie_to_pivot.append(summed_col)
    serie_to_pivot = serie_to_pivot.append(wa_serie)
    teams_compare = pd.DataFrame(columns=col)
    teams_compare = teams_compare.append(serie_to_pivot, ignore_index=True)
    return teams_compare


def optimization_lineup():
    team_list = tool.sql_query_to_list('SELECT TeamsTraditionalStats_TEAM_ID FROM NonNumeric_Dataset_Teams where '
                                  'TeamsTraditionalStats_Season = "2020-21" and TeamsTraditionalStats_SeasonType = '
                                  '"Regular Season"')
    for t in team_list:
        optimization_lineup_by_team(t)
    print('Teams lineups have been optimized')


def optimization_lineup_by_team(team_id):
    minutes = [12, 11, 10, 9, 6]
    bests_lineups = tool.sql_query_to_list('select "Lineup Type" from Bests_Lineups_count')
    for k in range(len(bests_lineups)):
        bests_lineups[k] = bests_lineups[k].split(', ')
    df = pd.read_sql_query('SELECT * FROM Team_Lineups WHERE Team = "' + str(team_id) + '"', Database.conn)
    combi = df['LineupType'].to_list()
    for k in range(len(combi)):
        combi[k] = combi[k].split(', ')
    for j in range(0, len(combi)):
        combi[j].sort()
    data_to_insert = pd.DataFrame()
    boxscore = pd.DataFrame()
    for m in minutes:
        done = False
        for b in bests_lineups:
            for c in combi:
                if b == c:
                    lineup_df = pd.DataFrame()
                    l_id = df['LineupID'].loc[(df['LineupType'] ==
                                               str(c).replace('[', '').replace(']', '').replace("'", ''))]
                    l_id = l_id.to_list()
                    if len(l_id) < 1:
                        break
                    for o in l_id:
                        lineup_df = pd.concat([lineup_df, pd.read_sql_query(Database.optimize(o, m), Database.conn)])
                    lineup_df['+/-'] = lineup_df['PTS'] - lineup_df['OPP_PTS']
                    z = 0
                    while z < len(lineup_df):
                        lineup_df.sort_values(['+/-'], ascending=False, inplace=True)
                        id_to_name = lineup_df['Lineup'].iloc[0]
                        names = df['LineupName'].loc[(df['LineupID'] == id_to_name)].to_string(index=False,
                                                                                               length=False)
                        if z == 0:
                            lineup_df.insert(2, 'LineupName', names)
                        else:
                            lineup_df['LineupName'] = names
                        data_to_insert = pd.concat([data_to_insert, lineup_df.nlargest(1, '+/-')])
                        data_to_insert.sort_values(['Min'], inplace=True)
                        bs = [i.split(', ') for i in data_to_insert['Lineup'].to_list()]
                        for p in bs[0]:
                            boxscore = pd.concat(
                                [boxscore, pd.read_sql_query(Database.optimize_players_stats(p, m), Database.conn)])
                        df = df.loc[(df['LineupID'] != data_to_insert['Lineup'].to_list()[0])]
                        check = boxscore.groupby(['PlayerName'])[["Min", "PF"]].sum()
                        check['Count'] = boxscore.groupby(['PlayerName'])[["PlayerName"]].count()
                        if data_to_insert.iloc[0][0] == 'CHA':
                            if not check.loc[(check.Min > 37) | (check.PF > 4) | (check.Count > 4)].empty:
                                data_to_insert = data_to_insert.iloc[1:]
                                lineup_df = lineup_df.iloc[1:]
                                boxscore = boxscore.loc[(boxscore['Min'] != m)]
                                z += 1
                                continue
                            done = True
                            break
                        elif not check.loc[(check.Min > 37) | (check.PF > 4) | (check.Count > 3)].empty:
                            data_to_insert = data_to_insert.iloc[1:]
                            lineup_df = lineup_df.iloc[1:]
                            boxscore = boxscore.loc[(boxscore['Min'] != m)]
                            z += 1
                            continue
                        done = True
                        break
                    break
            if done: break
    teams_compare = optimized_stats_team(data_to_insert)
    boxscore_players = get_players_boxscore(boxscore)
    teams_compare.to_sql('Optimized_teams', Database.conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized stats have been inserted')
    data_to_insert.to_sql('Optimized_lineups', Database.conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized lineups have been inserted')
    boxscore_players.to_sql('Optimized_boxscores_lineups', Database.conn, if_exists='append', index=False)
    print(str(data_to_insert.iloc[0][0]) + ' - Optimized boxscores have been inserted')
