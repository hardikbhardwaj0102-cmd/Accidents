import streamlit as st
import numpy as np
import joblib
import folium
from streamlit_folium import st_folium

# Load model
model = joblib.load("accident_model.pkl")

st.set_page_config(page_title="Accident Risk Predictor", layout="wide")

# ----------- SESSION STATE ----------- #
if "page" not in st.session_state:
    st.session_state.page = "input"

if "markers" not in st.session_state:
    st.session_state.markers = []

# ---------------- PAGE 1 (INPUT) ---------------- #
if st.session_state.page == "input":

    st.title("🚗 Smart Accident Risk Prediction System")
    st.write("Enter road and environmental conditions to predict accident risk.")

    col1, col2 = st.columns(2)

    with col1:
        road_type = st.selectbox("Road Type", ["Urban", "Highway", "Rural"])
        road_type = {"Urban":1, "Highway":2, "Rural":3}[road_type]

        num_lanes = st.selectbox("Number of Lanes", [1, 2, 3])
        curvature = st.slider("Curvature", 0.0, 1.0)
        speed_limit = st.selectbox("Speed Limit", [25, 45, 60, 70])

        lighting = st.selectbox("Lighting", ["Dim", "Night", "Daylight"])
        lighting = {"Dim":1, "Night":2, "Daylight":3}[lighting]

        weather = st.selectbox("Weather", ["Clear", "Foggy", "Rainy"])
        weather = {"Clear":1, "Foggy":2, "Rainy":3}[weather]

    with col2:
        road_signs_present = st.selectbox("Road Signs Present", [0, 1])
        public_road = st.selectbox("Public Road", [0, 1])

        time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening"])
        time_of_day = {"Morning":1, "Afternoon":2, "Evening":3}[time_of_day]

        holiday = st.selectbox("Holiday", [0, 1])
        school_season = st.selectbox("School Season", [0, 1])

        num_reported_accidents = st.slider("Reported Accidents", 0.0, 10.0, 0.0, 1.0)

        lat = st.number_input("Latitude", value=28.61)
        lon = st.number_input("Longitude", value=77.20)

    if st.button("🔍 Predict Risk"):

        st.session_state.input_data = [
            road_type, num_lanes, curvature, speed_limit,
            lighting, weather, road_signs_present,
            public_road, time_of_day, holiday,
            school_season, num_reported_accidents
        ]

        st.session_state.lat = lat
        st.session_state.lon = lon

        st.session_state.page = "result"
        st.rerun()

# ---------------- PAGE 2 (RESULT + MAP) ---------------- #
elif st.session_state.page == "result":

    st.title("📍 Accident Risk Map")

    data = np.array(st.session_state.input_data).reshape(1, -1)
    pred = model.predict(data)[0]

    # Risk mapping
    if pred == 0:
        risk = "Low Risk"
        color = "green"
        st.success("🟢 Low Risk - Safe conditions")
    elif pred == 1:
        risk = "Medium Risk"
        color = "orange"
        st.warning("🟡 Medium Risk - Stay alert")
    else:
        risk = "High Risk"
        color = "red"
        st.error("🔴 High Risk - Dangerous conditions!")

    st.subheader(f"Predicted Risk Level: {risk}")

    # -------- MAP -------- #
    st.subheader("📍 Click anywhere on map to check risk")

    lat = st.session_state.lat
    lon = st.session_state.lon

    m = folium.Map(
        location=[lat, lon],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    # Show previous markers
    for marker in st.session_state.markers:
        folium.Marker(
            location=[marker["lat"], marker["lon"]],
            popup=f"Risk: {marker['risk']}",
            icon=folium.Icon(color=marker["color"])
        ).add_to(m)

    map_data = st_folium(m, width=800, height=500)

    # -------- CLICK PREDICTION -------- #
    if map_data and map_data["last_clicked"]:

        click_lat = map_data["last_clicked"]["lat"]
        click_lon = map_data["last_clicked"]["lng"]

        st.write(f"📌 Selected Location: {click_lat:.4f}, {click_lon:.4f}")

        data = np.array(st.session_state.input_data).reshape(1, -1)
        pred = model.predict(data)[0]

        if pred == 0:
            risk = "Low Risk"
            color = "green"
        elif pred == 1:
            risk = "Medium Risk"
            color = "orange"
        else:
            risk = "High Risk"
            color = "red"

        st.success(f"Predicted Risk at selected location: {risk}")

        st.session_state.markers.append({
            "lat": click_lat,
            "lon": click_lon,
            "risk": risk,
            "color": color
        })

        st.rerun()

    # 🔙 Back button
    if st.button("⬅ Back"):
        st.session_state.page = "input"
        st.rerun()