import streamlit as st
import pandas as pd
import torch
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
    model.conf = 0.80  # Set a confidence threshold
    return model

model = load_model()

def get_image_coordinates(image):
    exif_data = image._getexif()
    if not exif_data:
        return None

    gps_info = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_info[sub_decoded] = value[t]

    if not gps_info:
        return None

    def convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    lat = convert_to_degrees(gps_info['GPSLatitude'])
    if gps_info['GPSLatitudeRef'] != "N":
        lat = -lat

    lon = convert_to_degrees(gps_info['GPSLongitude'])
    if gps_info['GPSLongitudeRef'] != "E":
        lon = -lon

    return lat, lon

def save_pothole_location(suburb, latitude, longitude):
    data = {"Suburb": suburb, "Latitude": latitude, "Longitude": longitude}
    df = pd.DataFrame([data])
    df.to_csv("pothole_locations.csv", mode='a', header=not os.path.isfile("pothole_locations.csv"), index=False)

def initialize_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w') as file:
            file.write("Suburb,Latitude,Longitude\n")

initialize_csv("pothole_locations.csv")

def report_page():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Open Sans', sans-serif;
        }

        .title {
            font-size: 48px;
            font-weight: 800;
            color: #285430;
            text-align: center;
            margin-bottom: 20px;
        }

        .form-container {
            background-color: #F0FFF0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .stFileUploader > div {
            background-color: #F0FFF0;
            border: 2px dashed #4C7850;
            border-radius: 10px;
        }

        .stButton > button {
            background-color: #285430;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px 0;
            border-top: 1px solid #A2D9CE;
            color: #4C7850;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="title">Report a Pothole 🌿</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload an image of the pothole...", type=["jpg", "png", "jpeg"])
    suburb = st.text_input("Enter the suburb name:")
    report_button = st.button("Report Pothole")

    if uploaded_file is not None and report_button:
        image = Image.open(uploaded_file)
        results = model(image)

        # Get the detections from the results
        detections = results.pandas().xyxy[0]

        # Check if a pothole is detected
        detected_pothole = False
        for index, detection in detections.iterrows():
            if detection['name'] == 'Pothole' and detection['confidence'] > model.conf:
                detected_pothole = True
                break

        if detected_pothole:
            coords = get_image_coordinates(image)
            if coords:
                latitude, longitude = coords
                st.success(f"Pothole detected and reported at coordinates: Latitude {latitude}, Longitude {longitude}")
                save_pothole_location(suburb, latitude, longitude)
            else:
                st.error("No GPS coordinates found in the image.")
        else:
            st.error("No pothole detected in the image.")

        st.image(results.render()[0], channels="BGR", caption="Uploaded Image with Detections")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer">
            <p>Developed by Xavier Ensor</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Ensure this script runs when the app is started
if __name__ == "__main__":
    report_page()
