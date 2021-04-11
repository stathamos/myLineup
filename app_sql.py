import Database
import pandas as pd


def get_table(table_name):
    df = pd.read_sql_query('SELECT * FROM ' + table_name, Database.conn)
    return df


df_tables = pd.read_sql_query('SELECT name as "Tables" FROM sqlite_master WHERE type ="table" AND name NOT LIKE '
                             '"sqlite_%" AND (name like "Players%"	OR name like "Teams%" OR name like "Lineups%") '
                             'AND name <> "Players_with_type"', Database.conn)

list_tables = df_tables['Tables'].to_list()