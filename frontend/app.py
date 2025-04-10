import streamlit as st
from api import upload_pet, search_pet, register_volunteer, notify_rescue_center
from PIL import Image
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="Pet Rescue Finder", layout="wide")

# ---------- Custom CSS for enhanced UI ----------
st.markdown("""
    <style>
    /* Main app background */
    

    /* Expand to cover full width and remove white margins */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        
    }

    /* Optional: make sidebar also orange-ish */
    section[data-testid="stSidebar"] {
        background-color: #ffd480;  /* Light orange for contrast */
    }

    /* Text and button styles */
    h2, h3, h4 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #00CED1;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #219150;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)


# ---------- Session State Routing ----------
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

if st.sidebar.button("🏠 Home"):
    st.session_state.page = "🏠 Home"

if st.sidebar.button("🙋 Register as Volunteer"):
    st.session_state.page = "🙋 Register as Volunteer"

page = st.session_state.page

# ---------- App Title ----------
if page == "🏠 Home":
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="font-family:Comic Sans MS;">
            🐾 <span style="color:#ffd480;">Welcome</span> 
                <span style="color:#ffd480;">to</span>
            <span style="color:#ffd480;">Pet</span>
            <span style="color:#ffd480;">Rescue</span>
            <span style="color:#ffd480;">Finder</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <h1 style='font-weight: 800;'>Help Lost Pets<br><span style='color: #1abc9c;'>Find Their Way Home</span></h1>
        <p>Join our community of compassionate individuals helping to reunite lost pets with their worried families.</p>
        """, unsafe_allow_html=True)

        if st.button("🐾 I Found a Pet"):
            st.session_state.page = "upload"
            st.rerun()

        if st.button("🔍 I Lost My Pet"):
            st.session_state.page = "search"
            st.rerun()

    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <img src="https://images.unsplash.com/photo-1568572933382-74d440642117"
                    alt="Dog Image"
                    style="max-width: 375px; height: 375px; border-radius: 1000px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" />
            </div>
        """, unsafe_allow_html=True)


# ---------- Upload Pet ----------
elif page == "upload":
    st.markdown("""<div class='main'>""", unsafe_allow_html=True)
    st.header("📤 Upload Lost or Abandoned Pet")

    uploaded_image = st.file_uploader("Upload an image of the pet", type=["jpg", "png", "jpeg"])
    location = get_geolocation()
    if location and "coords" in location:
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]
        loc_dict = {"lat": lat, "lon": lon}
        st.success(f"📍 Your Location: Latitude {lat:.5f}, Longitude {lon:.5f}")
    else:
        st.warning("📡 Waiting for location access... Please allow it in your browser settings.")
        loc_dict = None

    rescue_option = st.radio(
        "What would you like to do with the pet?",
        [
            "1. I can take the pet to a nearby rescue center",
            "2. I just want to report this pet (notify rescue centers)"
        ]
    )

    if uploaded_image and loc_dict:
        if st.button("Upload & Analyze"):
            with st.spinner("🚀 Uploading and analyzing..."):
                result = upload_pet(image=uploaded_image, location=loc_dict)

                if result["status"] == "success":
                    data = result["data"]
                    st.success("✅ Pet uploaded successfully!")
                    st.markdown("### 🔍 Extracted Features")
                    st.markdown(f"**Breed:** {data['breed']}")
                    st.markdown(f"**Color:** {data['color']}")
                    st.markdown(f"**Size:** {data['size']}")
                    st.image(data["image_path"], caption="📷 Stored Image", use_container_width=True)
                    st.markdown(f"**Nearest Rescue Center:** {data['nearest_rescue_center']['name']} ({data['distance_to_rescue_center_km']} km)")

                    if rescue_option.startswith("2"):
                        notify_result = notify_rescue_center(data["nearest_rescue_center"], loc_dict)
                        if notify_result["status"] == "success":
                            st.info(f"📢 Alert sent to {data['nearest_rescue_center']['name']} at {data['nearest_rescue_center']['email']}")
                        else:
                            st.error("❌ Failed to notify the rescue center.")
                else:
                    st.error(f"❌ Upload failed: {result['message']}")
    st.markdown("""</div>""", unsafe_allow_html=True)

# ---------- Search Pet ----------
elif page == "search":
    st.markdown("""<div class='main'>""", unsafe_allow_html=True)
    st.header("🔍 Search for a Lost Pet")
    uploaded_image = st.file_uploader("Upload the image of your lost pet", type=["jpg", "png", "jpeg"])
    color = st.text_input("Color (e.g., brown, black, white)")
    size = st.selectbox("Size", ["small", "medium", "large"])
    breed = st.text_input("Breed (e.g., labrador, beagle)")

    if uploaded_image and color and size and breed:
        if st.button("Search"):
            with st.spinner("🔍 Searching..."):
                result = search_pet(breed, color, size, uploaded_image)
                if result["status"] == "success":
                    matches = result["matches"]
                    st.success(f"Top {len(matches)} matching pets found:")
                    for match in matches:
                        st.image(match["image_path"], caption=f"Score: {match['score']} | Breed: {match['breed']} | Color: {match['color']} | Size: {match['size']}", use_container_width=True)
                else:
                    st.error(f"❌ Search failed: {result['message']}")
    st.markdown("""</div>""", unsafe_allow_html=True)

# ---------- Register as Volunteer ----------
elif page == "🙋 Register as Volunteer":
    st.markdown("""<div class='main'>""", unsafe_allow_html=True)
    st.header("🙋 Register as Volunteer")

    name = st.text_input("Your Name")
    phone = st.text_input("Phone Number")

    location = get_geolocation()
    if location and "coords" in location:
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]
        st.success(f"📍 Location: Latitude {lat:.5f}, Longitude {lon:.5f}")
    else:
        st.warning("📡 Waiting for location access... Please allow it in your browser settings.")

    if st.button("Register as Volunteer"):
        if not name or not phone:
            st.error("❌ Please provide both name and phone number.")
        elif not phone.isdigit() or len(phone) != 10:
            st.error("❌ Please enter a valid 10-digit phone number.")
        elif not location or "coords" not in location:
            st.error("❌ Location is required for registration.")
        else:
            with st.spinner("📝 Registering..."):
                result = register_volunteer(name, phone, lat, lon)
                if result["status"] == "success":
                    st.success("✅ Registered successfully! Thank you for volunteering! ❤️")
                else:
                    st.error(f"❌ Registration failed: {result['message']}")
    st.markdown("""</div>""", unsafe_allow_html=True)
