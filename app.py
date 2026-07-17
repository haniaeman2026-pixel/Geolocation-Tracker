import streamlit as st
import requests
import folium
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
import base64

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Geolocation Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD CSS
# ==========================================

try:
    with open("style.css", "r", encoding="utf-8") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/854/854878.png",
        width=90
    )

    st.title("🌍 Geolocation Tracker")

    st.markdown("---")

    st.success("Application Status")
    st.write("🟢 Online")

    st.markdown("---")

    st.subheader("✨ Features")

    st.write("📍 Live IP Detection")
    st.write("🌎 Country Information")
    st.write("🏙️ City & Region")
    st.write("🗺️ Interactive Map")
    st.write("🌤️ Weather")
    st.write("🌐 ISP Details")
    st.write("🕒 Time Zone")
    st.write("📄 CSV Report")
    st.write("📄 PDF Report")

    st.markdown("---")

    st.info(
        "Developed for HexSoftwares Internship"
    )

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
"""
<div class="hero">

<h1>
🌍 Geolocation Tracker
</h1>

<p>
Track your live location using your Public IP Address.
Professional Dashboard built with Python & Streamlit.
</p>

</div>
""",
unsafe_allow_html=True
)

# ==========================================
# DATE & TIME
# ==========================================

current_time = datetime.now().strftime(
    "%d %B %Y | %I:%M:%S %p"
)

st.info(f"🕒 Current Time : {current_time}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# SECTION TITLE
# ==========================================

st.markdown(
"""
<h2 style='text-align:center;'>

📍 Current Location Information

</h2>
""",
unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# FETCH DATA FROM API
# ==========================================

try:

    response = requests.get(
        "https://ipinfo.io/json",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    ip = data.get("ip", "N/A")
    city = data.get("city", "N/A")
    region = data.get("region", "N/A")
    country = data.get("country", "N/A")
    timezone = data.get("timezone", "N/A")
    organization = data.get("org", "N/A")

    location = data.get("loc", "0,0")

    latitude, longitude = location.split(",")
    # ==========================================
    # COUNTRY FLAG
    # ==========================================

    flag_url = f"https://flagsapi.com/{country}/flat/64.png"

    st.image(flag_url, width=80)

    # ==========================================
    # DASHBOARD CARDS
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📡 Network Information")

        st.write(f"🌐 **IP Address:** {ip}")
        st.write(f"🌍 **Country:** {country}")
        st.write(f"🏙️ **City:** {city}")
        st.write(f"📍 **Region:** {region}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📍 Coordinates")

        st.write(f"📌 **Latitude:** {latitude}")
        st.write(f"📌 **Longitude:** {longitude}")

        st.write(f"🕒 **Time Zone:** {timezone}")

        st.write(f"🌐 **ISP:** {organization}")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ==========================================
    # METRICS
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🌍 Country",
            country
        )

    with c2:
        st.metric(
            "🏙️ City",
            city
        )

    with c3:
        st.metric(
            "📍 Region",
            region
        )

    with c4:
        st.metric(
            "🕒 Time Zone",
            timezone
        )

    st.markdown("---")

    # ==========================================
    # GOOGLE MAP BUTTON
    # ==========================================

    google_map = f"https://www.google.com/maps?q={latitude},{longitude}"

    st.link_button(
        "🌍 Open Location in Google Maps",
        google_map,
        use_container_width=True
    )

    st.markdown("---")
        # ==========================================
    # INTERACTIVE MAP
    # ==========================================

    st.subheader("🗺️ Interactive Location Map")

    location_map = folium.Map(
        location=[float(latitude), float(longitude)],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    folium.Marker(
        [float(latitude), float(longitude)],
        popup=f"{city}, {country}",
        tooltip="Your Current Location",
        icon=folium.Icon(color="red", icon="globe")
    ).add_to(location_map)

    st_folium(
        location_map,
        width=None,
        height=500
    )

    st.markdown("---")

    # ==========================================
    # WEATHER INFORMATION
    # ==========================================

    st.subheader("🌤️ Current Weather")

    weather_url = f"https://wttr.in/{city}?format=j1"

    try:

        weather = requests.get(weather_url, timeout=10).json()

        current = weather["current_condition"][0]

        temp = current["temp_C"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]
        description = current["weatherDesc"][0]["value"]

        w1, w2, w3, w4 = st.columns(4)

        w1.metric("🌡️ Temperature", f"{temp} °C")
        w2.metric("💧 Humidity", f"{humidity}%")
        w3.metric("🌬️ Wind", f"{wind} km/h")
        w4.metric("☁️ Condition", description)

    except:
        st.warning("Weather information is currently unavailable.")

    st.markdown("---")

    # ==========================================
    # DOWNLOAD CSV
    # ==========================================

    report = pd.DataFrame({

        "Field":[
            "IP Address",
            "Country",
            "City",
            "Region",
            "Latitude",
            "Longitude",
            "Time Zone",
            "ISP"
        ],

        "Value":[
            ip,
            country,
            city,
            region,
            latitude,
            longitude,
            timezone,
            organization
        ]

    })

    csv = report.to_csv(index=False)

    st.download_button(
        label="⬇️ Download CSV Report",
        data=csv,
        file_name="geolocation_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # DEVELOPER CARD
    # ==========================================

    st.markdown("""

<div class="card">

<h2 align="center">👩‍💻 Developer</h2>

<h3 align="center">Hania Eman</h3>

<p align="center">

HexSoftwares Internship Project

<br>

Python • Streamlit • Folium

</p>

</div>

""", unsafe_allow_html=True)

    st.markdown("---")

    # ==========================================
    # FOOTER
    # ==========================================

    st.markdown("""

<div class="footer">

<h3>🌍 Geolocation Tracker</h3>

<p>

Made with ❤️ using Python & Streamlit

</p>

<p>

© 2026 Hania Eman

</p>

</div>

""", unsafe_allow_html=True)

# ==========================================
# ERROR HANDLING
# ==========================================

except Exception as e:

    st.error("❌ Unable to fetch your location.")

    st.code(str(e))