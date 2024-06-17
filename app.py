import streamlit as st

st.set_page_config(page_title='Pothole Detection', page_icon="🚧", layout="wide")

# Import the different pages
from home import home_page
from map_page import map_page
from report_page import report_page

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

tabs = ["Home", "Map", "Report Pothole"]
selected_tab = st.sidebar.radio("Navigation", tabs)

if selected_tab == "Home":
    home_page()
elif selected_tab == "Map":
    map_page()
elif selected_tab == "Report Pothole":
    report_page()
