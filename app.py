import streamlit as st
import pandas as pd

st.set_page_config(page_title="Baccarat Predictor", layout="centered", initial_sidebar_state="collapsed")

st.title("🎮 Manual Input")

# Session state for game history
if "history" not in st.session_state:
    st.session_state.history = []

# Input Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 Banker", use_container_width=True):
        st.session_state.history.append("B")
with col2:
    if st.button("🔵 Player", use_container_width=True):
        st.session_state.history.append("P")
with col3:
    if st.button("🟢 Tie", use_container_width=True):
        st.session_state.history.append("T")

# Export to CSV
csv_data = pd.DataFrame(st.session_state.history, columns=["Result"])
csv = csv_data.to_csv(index=False).encode('utf-8')
st.download_button("💾 Export to CSV", csv, "baccarat_history.csv", "text/csv")

# Upload CSV
st.subheader("📂 Import Result History (CSV)")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])
if uploaded_file:
    df_uploaded = pd.read_csv(uploaded_file)
    if "Result" in df_uploaded.columns:
        st.session_state.history = df_uploaded["Result"].tolist()

# Game History Grid
st.subheader("📜 Game History Grid")
grid_size = 20
grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]

row, col = 0, 0
for result in st.session_state.history:
    if row >= grid_size:
        col += 1
        row = 0
    if col >= grid_size:
        break
    grid[row][col] = result
    row += 1

def colored_cell(result):
    if result == "B":
        return f"<div style='background-color:#e74c3c;color:white;text-align:center;border-radius:5px;'>B</div>"
    elif result == "P":
        return f"<div style='background-color:#3498db;color:white;text-align:center;border-radius:5px;'>P</div>"
    elif result == "T":
        return f"<div style='background-color:#2ecc71;color:white;text-align:center;border-radius:5px;'>T</div>"
    else:
        return "&nbsp;"

st.markdown("<style>table, td {border: 1px solid #333; padding: 5px;} td {width: 20px; height: 20px;}</style>", unsafe_allow_html=True)
html_grid = "<table>"
for r in range(grid_size):
    html_grid += "<tr>"
    for c in range(grid_size):
        html_grid += f"<td>{colored_cell(grid[r][c])}</td>"
    html_grid += "</tr>"
html_grid += "</table>"
st.markdown(html_grid, unsafe_allow_html=True)