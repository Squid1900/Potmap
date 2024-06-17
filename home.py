import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Open Sans', sans-serif;
            background-color: #F0FFF0;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(to bottom, #A2D9CE, #F0FFF0);
            padding: 100px 0;
            text-align: center;
        }
        .main-title {
            font-size: 60px;
            font-weight: 800;
            color: #285430;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 28px;
            color: #4C7850;
            margin-bottom: 40px;
        }

        /* Content Sections (Bubbles) */
        .section-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 40px 0;
        }
        .bubble {
            background-color: #FFFFFF;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
            flex: 1;
            margin: 0 10px;
            min-width: 250px;
            transition: transform 0.3s ease-in-out;
        }
        .bubble:hover {
            transform: scale(1.05);
        }
        .section-title {
            font-size: 24px;
            color: #285430;
            margin-bottom: 15px;
        }
        .section-text {
            font-size: 16px;
            color: #333;
        }

        /* Scrolling Content */
        .scrolling-content {
            padding: 50px 0;
            display: flex;
            align-items: center;
        }
        .pothole-info {
            width: 50%;
            padding-right: 40px;
        }
        .pothole-image {
            width: 50%;
            text-align: center;
        }
        .pothole-image img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 20px 0;
            border-top: 1px solid #A2D9CE;
            color: #4C7850;
            background-color: #EAF6F2;
            margin-top: 50px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_hero_section():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Welcome to Pothole Detection 🌿</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your partner in making roads safer</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_bubbled_content():
    bubbles = [
        {
            "title": "🗺️ Explore & Report",
            "text": "Discover and navigate the map to see all reported potholes. Found a new one? Easily report it through the app."
        },
        {
            "title": "🌳 Contribute & Improve",
            "text": "Your reports are valuable. They help us prioritize repairs and make informed decisions."
        },
        {
            "title": "📷 Be safe & Help out",
            "text": "Unsure if you have a pothole? Use our detection tool to identify potential potholes in your area."
        }
    ]

    cols = st.columns(3)
    for i, bubble in enumerate(bubbles):
        with cols[i]:
            st.markdown(
                f"""
                <div class="bubble">
                    <div class="section-title">{bubble['title']}</div>
                    <div class="section-text">{bubble['text']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_scrolling_content(image_path, title, content, reverse=False):
    st.markdown("<div class='scrolling-content'>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        if reverse:
            col1, col2 = col2, col1

        with col1:
            st.markdown("<div class='pothole-image'>", unsafe_allow_html=True)
            st.image(image_path)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='pothole-info'>", unsafe_allow_html=True)
            st.markdown(f"## {title}")
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_footer():
    st.markdown(
        """
        <div class='footer'>
            © 2024 Pothole Detection. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )

def home_page():
    apply_custom_styles()
    render_hero_section()
    render_bubbled_content()
    
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    pothole_info = """A pothole is a sunken depression or hole in a road surface, ranging from a few centimetres to several metres in size. 
    They form when water penetrates the road's weakened surface, weakening the underlying base material through repeated freeze-thaw cycles or vehicle traffic. 
    Traffic compression causes further damage by breaking apart surrounding pavement, allowing more water intrusion and accelerating the pothole's growth. 
    The formation of potholes begins with small cracks in the road caused by weathering and environmental factors like heavy rain or freeze-thaw cycles. 
    Water seeps into these cracks, weakening the base material, and repeated traffic only contributes the damage. 
    The combination of water intrusion and vehicular stress eventually results in a pothole. 
    Potholes pose safety hazards for drivers as they can cause tire blowouts, vehicle alignment issues, and even accidents.
    Preventative measures like regular road maintenance and patching small cracks before they become potholes are crucial to preserving the integrity of road infrastructure."""

    render_scrolling_content('./page.jpg', 'What is a Pothole?', pothole_info, reverse=True)
    
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    
    report_info = """Reporting a pothole using our app is simple and helps keep our roads safe:
    
    1. Take a Photo: Use your phone to capture a clear image of the pothole.
    2. Upload: Using our report page you can upload a photo from your library.
    2. Automatic Detection: Our software analyses the image to verify the presence of a pothole.
    3. Location Extraction: The app automatically extracts the location information from the photo.
    4. Submit Report: Complete the report with any additional details and submit it. Your report will be added to our database and prioritized for repair.
    
    By reporting potholes, you contribute to safer roads and help authorities address road damage more efficiently. Your participation makes a significant difference in road safety and maintenance."""

    render_scrolling_content('./break.jpg', 'How to Report a Pothole?', report_info)
    
    render_footer()

if __name__ == '__main__':
    home_page()
