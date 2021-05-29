import app1
import app2
import app3
import app4
import streamlit as st


# Main file of the streamlit application.

PAGES = {
    "Introduction": app1,
    "Clustering NBA Players": app2,
    "Identifying player's characteristics": app3,
    "Optimizing lineups": app4
}
st.sidebar.title('Tabs')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
