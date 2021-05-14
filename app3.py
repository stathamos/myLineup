import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import sqlite3
import random


def app():

    def sort_list(li):
        if li[1] == 'Other players':
            li[1] = li[0]
            li[0] = 'Other players'
        return li


    conn = sqlite3.connect('../DB 100h Proj/DB_NBA_v6.db')  # Connection / Creation of the DataBase
    c = conn.cursor()
    conn.commit()

    st.image('../Logo.png')

    st.text("The next step in my analysis is to look for specifics on each type of player. By doing this I will be \n"
            "able to identify what field each type of player is good at / bad at. Whether for the player's coach or \n"
            "for the opposing coach, this information is very interesting because it allows: either to put his player \n"
            "in the best possible attack / defense position, or to prevent an opponent from getting into a comfort\n "
            "zone.\n\n"
            "For each type of player I summerized briefly what are his strength, and put it into this little tool :\n")

    characteristic_selection = st.selectbox('Do you want to search a player or a type of player ?'
                                            , ['Player', 'Type of player'])

    if characteristic_selection == 'Player':
        df_characteristic = pd.read_sql_query('SELECT PlayersBios_PLAYER_NAME as Name, PlayersBios_PLAYER_ID as Player_ID,'
                                              'P.Type, "Type name" as Type_name, Characteristics, Query, Title '
                                              'FROM Players_with_type P '
                                              'JOIN Type_description T on T.Type = P.Type '
                                              'LEFT JOIN Query Q on Q.Type = T."Type name"', conn)
        list_player_current_season = df_characteristic['Name'].to_list()
        characteristic_player_selection = st.selectbox('Select the player you and see his characteristics : '
                                                       , list_player_current_season)
        player_id = df_characteristic.loc[df_characteristic['Name'] ==
                                          characteristic_player_selection].Player_ID.values[0]
        type_name = df_characteristic.loc[df_characteristic['Name'] ==
                                          characteristic_player_selection].Type_name.values[0]
        characteristic = df_characteristic.loc[df_characteristic['Name'] ==
                                               characteristic_player_selection].Characteristics.values[0]
        query = df_characteristic.loc[df_characteristic['Name'] == characteristic_player_selection].Query.values[0]
        title = df_characteristic.loc[df_characteristic['Name'] == characteristic_player_selection].Title.values[0]

        img, graph = st.beta_columns(2)

        with img:
            st.subheader(characteristic_player_selection)
            st.image('../Players Pictures/' + player_id + '.png', caption=characteristic_player_selection
                                                                          + ' : ' + type_name)
            st.write(characteristic)
        with graph:
            df_graph = pd.read_sql_query(query, conn)
            li = df_graph.Type.unique().tolist()
            sort_list(li)
            dft = df_graph.iloc[:, 1].loc[df_graph['Type'] == li[0]]
            dfo = df_graph.iloc[:, 1].loc[df_graph['Type'] == li[1]]
            a = [dft.to_numpy(), dfo.to_numpy()]
            fig = ff.create_distplot(a, group_labels=li, curve_type='normal')
            fig.update_xaxes(title_text=title)
            fig.update_yaxes(title_text='Density')
            st.write(fig)

    elif characteristic_selection == 'Type of player':
        df_type = pd.read_sql_query('select "Type name" as Type_name, Type from Type_description', conn)
        df_characteristic = pd.read_sql_query('SELECT PlayersBios_PLAYER_NAME as Name, PlayersBios_PLAYER_ID as Player_ID,'
                                              'P.Type, "Type name" as Type_name, Characteristics, Query, Title '
                                              'FROM Players_with_type P '
                                              'JOIN Type_description T on T.Type = P.Type '
                                              'LEFT JOIN Query Q on Q.Type = T."Type name"', conn)
        list_type = df_type['Type_name'].to_list()
        type_selection = st.selectbox('Select the type of player you want to see and \n'
                                      'his characteristics : ', list_type)
        df_characteristic = df_characteristic.loc[df_characteristic['Type_name'] == type_selection]
        list_player_current_season = df_characteristic['Name'].to_list()
        characteristic_player_selection = random.choice(list_player_current_season)
        player_id = df_characteristic.loc[df_characteristic['Name'] ==
                                          characteristic_player_selection].Player_ID.values[0]
        type_name = df_characteristic.loc[df_characteristic['Name'] ==
                                          characteristic_player_selection].Type_name.values[0]
        characteristic = df_characteristic.loc[df_characteristic['Name'] ==
                                               characteristic_player_selection].Characteristics.values[0]
        query = df_characteristic.loc[df_characteristic['Name'] == characteristic_player_selection].Query.values[0]
        title = df_characteristic.loc[df_characteristic['Name'] == characteristic_player_selection].Title.values[0]

        img, graph = st.beta_columns(2)

        with img:
            st.subheader(characteristic_player_selection)
            st.image('../Players Pictures/' + player_id + '.png', caption=characteristic_player_selection
                                                                          + ' : ' + type_name)
            st.write(characteristic)
        with graph:
            df_graph = pd.read_sql_query(query, conn)
            li = df_graph.Type.unique().tolist()
            sort_list(li)
            dft = df_graph.iloc[:, 1].loc[df_graph['Type'] == li[0]]
            dfo = df_graph.iloc[:, 1].loc[df_graph['Type'] == li[1]]
            a = [dft.to_numpy(), dfo.to_numpy()]
            fig = ff.create_distplot(a, group_labels=li, curve_type='normal')
            fig.update_xaxes(title_text=title)
            fig.update_yaxes(title_text='Density')
            st.write(fig)
