import streamlit as st
import pydeck as pdk
import pandas as pd
import os

def initialize_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w') as file:
            file.write("Suburb,Latitude,Longitude\n")

initialize_csv("pothole_locations.csv")

def load_pothole_data():
    try:
        return pd.read_csv("pothole_locations.csv", names=["Suburb", "Latitude", "Longitude"], skiprows=1)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Suburb", "Latitude", "Longitude"])

def map_page():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Open Sans', sans-serif;
        }

        .map-container {
            background: linear-gradient(to bottom, #A2D9CE, #F0FFF0);
            padding: 50px 0;
            text-align: center;
        }

        .map-title {
            font-size: 48px;
            font-weight: 800;
            color: #285430;
            margin-bottom: 20px;
        }
        
        .map-subtitle {
            font-size: 24px;
            color: #4C7850;
            margin-bottom: 40px;
        }

        .search-container {
            background-color: #F0FFF0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .sidebar .stTextInput > div > input {
            background-color: #E6F5E3;
            border: 1px solid #A2D9CE;
            border-radius: 8px;
        }

        .footer {
            text-align: center;
            padding: 20px 0;
            border-top: 1px solid #A2D9CE;
            color: #4C7850;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    df = pd.read_csv("sydney_suburbs.csv")
    pothole_df = load_pothole_data()

    with st.container():
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.markdown('<div class="map-title">Pothole Detection Map 🌿</div>', unsafe_allow_html=True)
        st.markdown('<div class="map-subtitle">Explore and report potholes in Sydney</div>', unsafe_allow_html=True)

        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_term = st.text_input("Enter a suburb name:", "")
        st.markdown('</div>', unsafe_allow_html=True)

        if search_term:
            selected_suburb = df[df['Suburb'].str.contains(search_term, case=False)]
            if not selected_suburb.empty:
                selected_lat = selected_suburb['Latitude'].values[0]
                selected_lon = selected_suburb['Longitude'].values[0]
                initial_view_state = pdk.ViewState(latitude=selected_lat, longitude=selected_lon, zoom=14)
            else:
                st.error("Suburb not found.")
                initial_view_state = pdk.ViewState(latitude=-33.8688, longitude=151.2093, zoom=9)
        else:
            initial_view_state = pdk.ViewState(latitude=-33.8688, longitude=151.2093, zoom=9)

        view_state = pdk.ViewState(latitude=-33.8688, longitude=151.2093, zoom=10, pitch=0)

        layer = pdk.Layer(
            'ScatterplotLayer',
            data=pothole_df,
            get_position=['Longitude', 'Latitude'],
            get_color=[200, 30, 0, 160],
            get_radius=2,
        )
        st.pydeck_chart(
            pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=initial_view_state,
                layers=[layer],
                tooltip={"text": "Suburb: {Suburb}\nLatitude: {Latitude}\nLongitude: {Longitude}"}
            )
        )

    st.markdown(
        """
        <div class="footer">
            <p>Developed by Xavier Ensor</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
