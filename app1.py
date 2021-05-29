import streamlit as st
import pandas as pd
import sqlite3


def app():
    """Introduction of the app and showing the different tables we get."""
    def get_table(table_name):
        df = pd.read_sql_query('SELECT * FROM ' + table_name, conn)
        return df

    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v6.db')  # Connection / Creation of the DataBase
    conn.commit()

    st.image('../Logo.png')
    st.subheader('Optimizing NBA Lineups using unsupervised machine learning')
    st.markdown('After getting all stats possible on the NBA.com website, the main idea was to create\n'
                'clusters of players based on their statistics using unsupervised machine learning. \n'
                'Then after that, the goal was to\nsee what are the types of players that compose the \n'
                'bests lineups.')

    st.subheader('Introduction')
    st.markdown('Using request python library, we managed to get data from the last **7 years**. \n'
                'In total, we got **123** tables on statistics of : \n'
                '- Players\n'
                '- Teams\n'
                '- Lineups\n\n'
                'Here is a first tool that allow you to go through all the different tables we have\n'
                'in the database. \n')

    df_tables = pd.read_sql_query('SELECT name as "Tables" FROM sqlite_master WHERE type ="table" AND name NOT LIKE '
                                  '"sqlite_%" AND (name like "Players%"	OR name like "Teams%" OR name like "Lineups%")'
                                  ' AND name <> "Players_with_type"', conn)

    list_tables = df_tables['Tables'].to_list()
    table_selection = st.selectbox('Select the table you want to go through : ', list_tables)
    df_tables_selected = get_table(table_selection)
    st.dataframe(data=df_tables_selected)
