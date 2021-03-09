import pandas as pd
import sqlite3


conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.0.db')  # Connect to the 1st database
c = conn.cursor()
conn.commit()

conn2 = sqlite3.connect('../DB 100h Proj/DB_NBA_v4.1.db')  # Creation of new database that will have only the 3 datasets
c2 = conn2.cursor()  # the db will be "lighter"
conn2.commit()

query_players = pd.read_sql_query('SELECT * FROM Dataset_Players_2', conn)  # Get players stats
query_teams = pd.read_sql_query('SELECT * FROM Dataset_Teams_2', conn)  # Get teams stats
query_lineups = pd.read_sql_query('SELECT * FROM Dataset_Lineups_2', conn)  # Get lineups stats

df_players = pd.DataFrame(query_players)  # convert the query into a dataframe
df_teams = pd.DataFrame(query_teams)  # convert the query into a dataframe
df_lineups = pd.DataFrame(query_lineups)  # convert the query into a dataframe

df_players.to_sql('Dataset_Players', conn2, if_exists='replace', index=False)  # insert dataframe into new db
df_teams.to_sql('Dataset_Teams', conn2, if_exists='replace', index=False)
df_lineups.to_sql('Dataset_Lineups', conn2, if_exists='replace', index=False)

c2.execute('CREATE INDEX "Index_Dataset_Players" ON "Dataset_Players" ("PlayersBios_PLAYER_ID"	ASC, '
           '"PlayersBios_Season" ASC, "PlayersBios_SeasonType"	ASC);')
c2.execute('CREATE INDEX "Index_Dataset_Teams" ON "Dataset_Teams" ("TeamsTraditionalStats_TEAM_ID"	ASC, '
           '"TeamsTraditionalStats_Season" ASC, "TeamsTraditionalStats_SeasonType"	ASC);')
c2.execute('CREATE INDEX "Index_Dataset_Lineups" ON "Dataset_Lineups" ("LineupsTraditionalStats_PLAYER_ID"	ASC, '
           '"LineupsTraditionalStats_Season" ASC, "LineupsTraditionalStats_SeasonType"	ASC);')