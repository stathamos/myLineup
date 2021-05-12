import streamlit as st
import pandas as pd
import sqlite3


def app():

    def get_table(table_name):
        df = pd.read_sql_query('SELECT * FROM ' + table_name, conn)
        return df

    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v5.db')  # Connection / Creation of the DataBase
    c = conn.cursor()
    conn.commit()

    logo = open(file='../Logo.png')

    st.image('../Logo.png')
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
    st.dataframe(data=df_tables_selected)