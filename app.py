import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Title and theme toggle
st.set_page_config(page_title="Baccarat Predictor", layout="wide")
st.title("🔮 Baccarat Predictor Tool")

# Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if st.toggle("🌗 Toggle Dark Mode"):
    st.session_state.theme = "Dark"
else:
    st.session_state.theme = "Light"

st.markdown(f"**Current Theme:** {st.session_state.theme}")

# Initialize result history
if "results" not in st.session_state:
    st.session_state.results = []

# Input buttons
st.subheader("🎮 Manual Input")
cols = st.columns(3)
if cols[0].button("🟥 Banker"):
    st.session_state.results.append("B")
elif cols[1].button("🟦 Player"):
    st.session_state.results.append("P")
elif cols[2].button("🟩 Tie"):
    st.session_state.results.append("T")

# Save to CSV
if st.button("💾 Export to CSV"):
    df_export = pd.DataFrame({"Result": st.session_state.results})
    df_export.to_csv("baccarat_history.csv", index=False)
    st.success("Exported to baccarat_history.csv")

# Load from CSV
uploaded_file = st.file_uploader("📂 Import Result History (CSV)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.results = df["Result"].tolist()
    st.success("Result history loaded successfully")

# Show result history
st.subheader("📜 Game History")
st.write(st.session_state.results)

# Stats
st.subheader("📊 Statistics")
if st.session_state.results:
    df_stats = pd.Series(st.session_state.results)
    counts = df_stats.value_counts()
    st.write("**Win Distribution:**")
    st.bar_chart(counts)

    streak = 1
    max_streaks = []
    for i in range(1, len(df_stats)):
        if df_stats[i] == df_stats[i - 1]:
            streak += 1
        else:
            max_streaks.append(streak)
            streak = 1
    max_streaks.append(streak)

    st.write(f"Longest streak: {max(max_streaks)}")
    st.write(f"Total games: {len(df_stats)}")
    st.write(f"Tie %: {round((counts.get('T', 0) / len(df_stats)) * 100, 2)}%")

# Prediction (basic pattern-based)
def predict_next(results):
    if not results:
        return "Need more data"
    last = results[-1]
    if last == "B":
        return "Maybe P (Player)"
    elif last == "P":
        return "Maybe B (Banker)"
    return "Too random"

st.subheader("🔮 Prediction")
st.info(predict_next(st.session_state.results))
