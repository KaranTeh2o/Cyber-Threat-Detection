import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("model/model.pkl", "rb"))

st.set_page_config(page_title="Cyber Threat Dashboard", layout="wide")

st.title("Cyber Threat Intelligence Dashboard")

# ---------------- SESSION STORAGE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUT SECTION ----------------
st.subheader("Enter Network Data")

col1, col2, col3 = st.columns(3)

with col1:
    duration = st.number_input("Duration", min_value=0)

with col2:
    src_bytes = st.number_input("Source Bytes", min_value=0)

with col3:
    dst_bytes = st.number_input("Destination Bytes", min_value=0)

col4, col5 = st.columns(2)

with col4:
    count = st.number_input("Count", min_value=0)

with col5:
    srv_count = st.number_input("Srv Count", min_value=0)

# ---------------- PREDICTION ----------------
if st.button("Detect Threat"):
    data = [[duration, src_bytes, dst_bytes, count, srv_count]]
    result = model.predict(data)

    status = "Normal"
    if result[0] == -1:
        st.error("⚠️ Threat Detected!")
        status = "Threat"
        st.warning("🚨 ALERT: Suspicious activity detected!")
    else:
        st.success("✅ Normal Traffic")

    # Save history
    st.session_state.history.append({
        "duration": duration,
        "src_bytes": src_bytes,
        "dst_bytes": dst_bytes,
        "count": count,
        "srv_count": srv_count,
        "status": status
    })

# ---------------- HISTORY ----------------
st.subheader("Detection History")

if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history)

    st.dataframe(df)

    # ---------------- STATS ----------------
    st.subheader("Analytics")

    colA, colB = st.columns(2)

    with colA:
        st.write("### Threat vs Normal Count")
        st.bar_chart(df["status"].value_counts())

    with colB:
        st.write("### Source Bytes Trend")
        st.line_chart(df["src_bytes"])

else:
    st.info("No data yet. Run some predictions!")

# ---------------- CLEAR BUTTON ----------------
if st.button("Clear History"):
    st.session_state.history = []
    st.success("History Cleared!")