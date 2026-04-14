import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ---------------- LOAD MODEL ---------------- #
model = joblib.load("accident_model.pkl")

st.set_page_config(page_title="Accident Risk Predictor", layout="wide")

# ---------------- SESSION STATE ---------------- #
if "page" not in st.session_state:
    st.session_state.page = "input"

if "input_data" not in st.session_state:
    st.session_state.input_data = None

# ---------------- PAGE 1 ---------------- #
if st.session_state.page == "input":

    st.title("🚗 Accident Risk Prediction System")

    tab1, tab2, tab3 = st.tabs(["Road Info", "Environment", "Human Factors"])

    # -------- TAB 1 -------- #
    with tab1:
        road_mapping = {"Urban": 1, "Highway": 2, "Rural": 3}
        road_type_label = st.selectbox("Road Type 🚦", list(road_mapping.keys()))
        road_type = road_mapping[road_type_label]

        num_lanes = st.selectbox("Number of Lanes", [1, 2, 3, 4])
        curvature = st.slider("Curvature", 0.0, 1.0)
        speed_limit = st.selectbox("Speed Limit", [25, 45, 60, 70])

    # -------- TAB 2 -------- #
    with tab2:
        lighting_mapping = {"Dim 🌆": 1, "Night 🌙": 2, "Daylight ☀️": 3}
        lighting_label = st.selectbox("Lighting Condition 💡", list(lighting_mapping.keys()))
        lighting = lighting_mapping[lighting_label]

        weather_mapping = {"Clear ☀️": 1, "Foggy 🌫️": 2, "Rainy 🌧️": 3}
        weather_label = st.selectbox("Weather Condition 🌦️", list(weather_mapping.keys()))
        weather = weather_mapping[weather_label]

        road_signs_present = st.selectbox("Road Signs Present", [0, 1])
        public_road = st.selectbox("Public Road", [0, 1])

    # -------- TAB 3 -------- #
    with tab3:
        time_mapping = {"Morning 🌅": 1, "Afternoon 🌞": 2, "Evening 🌇": 3}
        time_label = st.selectbox("Time of Day ⏰", list(time_mapping.keys()))
        time_of_day = time_mapping[time_label]

        holiday = st.selectbox("Holiday 🎉", [0, 1])
        school_season = st.selectbox("School Season 🏫", [0, 1])
        num_reported_accidents = st.slider("Reported Accidents", 0.0, 10.0, 0.0, 1.0)

        if st.button("🔍 Predict Risk"):
            st.session_state.input_data = [
                road_type, num_lanes, curvature, speed_limit,
                lighting, weather, road_signs_present,
                public_road, time_of_day, holiday,
                school_season, num_reported_accidents
            ]
            st.session_state.page = "result"
            st.rerun()

# ---------------- PAGE 2 ---------------- #
elif st.session_state.page == "result":

    if st.session_state.input_data is None:
        st.warning("⚠️ No input found. Please go back.")
        if st.button("Go Back"):
            st.session_state.page = "input"
            st.rerun()
        st.stop()

    st.title("📊 Accident Risk Prediction Result")

    data = np.array(st.session_state.input_data).reshape(1, -1)

    pred = model.predict(data)[0]
    proba = model.predict_proba(data)[0]
    confidence = round(max(proba) * 100, 2)

    # -------- GRAPH -------- #
    st.markdown("### 📊 Risk Probability Distribution")

    fig, ax = plt.subplots(figsize=(3.5, 2))
    ax.bar(["Low", "Medium", "High"], proba)
    ax.set_title("Risk", fontsize=10)
    ax.set_ylabel("Prob", fontsize=8)
    ax.tick_params(axis='both', labelsize=8)
    fig.tight_layout()

    st.pyplot(fig, use_container_width=False)

    # -------- RISK DISPLAY -------- #
    if pred == 0:
        risk = "Low Risk"
        st.success("🟢 Low Risk")
    elif pred == 1:
        risk = "Medium Risk"
        st.warning("🟡 Medium Risk")
    else:
        risk = "High Risk"
        st.error("🔴 High Risk")

    st.subheader(f"Prediction: {risk}")
    st.write(f"Confidence: {confidence}%")

    # -------- REASONS -------- #
    reasons = []

    if st.session_state.input_data[4] == 2:
        reasons.append("Driving at night increases risk 🌙")

    if st.session_state.input_data[5] == 3:
        reasons.append("Rainy weather reduces visibility 🌧️")

    if st.session_state.input_data[2] > 0.6:
        reasons.append("High road curvature is dangerous 🛣️")

    if st.session_state.input_data[11] > 4:
        reasons.append("Area has high accident history ⚠️")

    if st.session_state.input_data[3] >= 60:
        reasons.append("High speed limit increases accident severity 🚗💨")

    if pred == 0:
        st.info("✅ Conditions are relatively safe. No major risk factors detected.")
    elif reasons:
        st.markdown("### ⚠️ Why this risk?")
        for r in reasons:
            st.write("- " + r)

    # -------- SAFETY SUGGESTIONS -------- #
    st.markdown("### 🛡️ Safety Suggestions")

    suggestions = []

    if st.session_state.input_data[5] == 3:
        suggestions.append("Drive slowly and maintain distance in rainy conditions 🌧️")

    if st.session_state.input_data[4] == 2:
        suggestions.append("Use headlights and stay alert while driving at night 🌙")

    if st.session_state.input_data[3] >= 60:
        suggestions.append("Avoid overspeeding 🚗💨")

    if st.session_state.input_data[2] > 0.6:
        suggestions.append("Reduce speed on curved roads 🛣️")

    if st.session_state.input_data[11] > 4:
        suggestions.append("High accident area — drive cautiously ⚠️")

    if st.session_state.input_data[0] == 2:
        suggestions.append("Maintain safe distance on highways 🛣️")

    if suggestions:
        for s in suggestions:
            st.success(s)
    else:
        st.success("✅ No special precautions needed. Drive safely!")

    # -------- SUMMARY -------- #
    reverse_road_mapping = {1: "Urban", 2: "Highway", 3: "Rural"}

    lighting_mapping = {"Dim 🌆": 1, "Night 🌙": 2, "Daylight ☀️": 3}
    weather_mapping = {"Clear ☀️": 1, "Foggy 🌫️": 2, "Rainy 🌧️": 3}
    time_mapping = {"Morning 🌅": 1, "Afternoon 🌞": 2, "Evening 🌇": 3}

    reverse_lighting_mapping = {v: k for k, v in lighting_mapping.items()}
    reverse_weather_mapping = {v: k for k, v in weather_mapping.items()}
    reverse_time_mapping = {v: k for k, v in time_mapping.items()}

    st.markdown("### 📋 Input Summary")

    st.write({
        "Road Type": reverse_road_mapping[st.session_state.input_data[0]],
        "Number of Lanes": st.session_state.input_data[1],
        "Curvature": st.session_state.input_data[2],
        "Speed Limit": st.session_state.input_data[3],
        "Lighting": reverse_lighting_mapping[st.session_state.input_data[4]],
        "Weather": reverse_weather_mapping[st.session_state.input_data[5]],
        "Road Signs": "Yes" if st.session_state.input_data[6] else "No",
        "Public Road": "Yes" if st.session_state.input_data[7] else "No",
        "Time of Day": reverse_time_mapping[st.session_state.input_data[8]],
        "Holiday": "Yes" if st.session_state.input_data[9] else "No",
        "School Season": "Yes" if st.session_state.input_data[10] else "No",
        "Reported Accidents": st.session_state.input_data[11],
    })

    # -------- DOWNLOAD REPORT -------- #
    st.markdown("### 📥 Download Report")

    report = f"""
Accident Risk Report

Prediction: {risk}
Confidence: {confidence}%

Road Type: {reverse_road_mapping[st.session_state.input_data[0]]}
Weather: {reverse_weather_mapping[st.session_state.input_data[5]]}
Lighting: {reverse_lighting_mapping[st.session_state.input_data[4]]}
Speed Limit: {st.session_state.input_data[3]}
Curvature: {st.session_state.input_data[2]}

Safety Suggestions:
"""

    for s in suggestions:
        report += f"- {s}\n"

    st.download_button("📄 Download Report", report, file_name="Accident_Report.txt")

    # -------- BACK BUTTON -------- #
    if st.button("⬅ Back"):
        st.session_state.page = "input"
        st.rerun()