import streamlit as st
import torch
from PIL import Image

@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  
    model.conf = 0.80
    return model

model = load_model()

def detect_page():
    # --- Custom Styles (Forest Theme) ---
    st.markdown(
        """
        <style>
        body {
            font-family: 'Open Sans', sans-serif;
        }

        /* Title and Subtitle */
        .title {
            font-size: 48px;
            font-weight: 800; 
            color: #285430;   
            text-align: center;
            margin-bottom: 20px; 
        }

        /* File Uploader */
        .stFileUploader > div {
            background-color: #F0FFF0;
            border: 2px dashed #4C7850;
            border-radius: 10px;
        }

        /* Button */
        .stButton > button {
            background-color: #285430;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }

        /* Image Display */
        .image-container {
            text-align: center;
        }
        .image-container img {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        }

        /* Footer */
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

    # --- Content ---
    st.markdown('<div class="title">Pothole Detector 🌿</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    detect_button = st.button("Detect Potholes")

    if uploaded_file is not None and detect_button:
        image = Image.open(uploaded_file)
        results = model(image)

        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(results.render()[0], channels="BGR", caption="Uploaded Image with Detections")
        st.markdown('</div>', unsafe_allow_html=True)
