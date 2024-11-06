from model import *
import streamlit as st
import pandas as pd
from backend import save_prediction  # Only import necessary functions
import sqlite3

# CSS for custom styling
st.markdown("""
    <style>
    /* Page layout styling */
    .main {
        background: linear-gradient(135deg, #f0f4c3, #b2ebf2);
        color: #333;
        font-family: Arial, sans-serif;
    }

    /* Title styling */
    .title {
        font-size: 2.5em;
        color: #003049;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }

    /* Subtitle styling */
    .subtitle {
        font-size: 1.2em;
        color: #003049;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Dropdown styling */
    .stSelectbox label {
        font-weight: bold;
        color: #333;
    }

    /* Button styling */
    .stButton > button {
        background-color: #00796b;
        color: #fff;
        border-radius: 10px;
        font-size: 1.1em;
        padding: 10px;
        margin-top: 20px;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #004d40;
    }

    /* Result box styling */
    .result-box {
        border-radius: 10px;
        background-color: #00796b;
        padding: 15px;
        color: white;
        text-align: center;
        font-size: 1.2em;
        margin-top: 10px;
    }

    /* Fighter names and probability text */
    .fighter-text {
        font-size: 1.1em;
        color: #ffffff;
        font-weight: bold;
    }

    /* Column styling */
    .stColumn {
        margin-top: 15px;
    }

    /* Error message styling */
    .stError {
        background-color: #f8d7da;
        color: #842029;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .Headernew {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-top: 2%;
    margin-bottom: 2%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize SQLite database
con = sqlite3.connect("searches.db")
cur = con.cursor()

# Drop the table if it exists and recreate it with the correct columns
cur.execute("DROP TABLE IF EXISTS results")
cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight_class TEXT,
        red_fighter TEXT,
        blue_fighter TEXT,
        red_win_probability REAL,
        blue_win_probability REAL,
        winner TEXT,
        prediction_time TEXT
    )
""")
con.commit()

# Streamlit UI with Tabs
st.markdown('<h1 class="title">🏆 UFC Fight Outcome Predictor</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Predict the Outcome of a UFC Fight by Selecting Fighters from the Same Weight Class</p>',
    unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Fight Prediction", "Results"])

with tab1:
    # Load fighter data
    fighter_data = pd.read_csv("ufc_master_data.csv")

    # Extract weights and names
    weight = fighter_data["weight"].astype(str).str.strip()  # Ensure weight is a clean string
    fighter = fighter_data["name"]


    # Initialize lists for each weight class
    fighter_names_125 = []
    fighter_names_135 = []
    fighter_names_145 = []
    fighter_names_155 = []
    fighter_names_170 = []
    fighter_names_185 = []
    fighter_names_205 = []
    fighter_names_265 = []

    # Populate the fighter names lists based on weight class
    for i in range(len(fighter_data)):
        if weight[i] == '125':
            fighter_names_125.append(fighter[i])
        elif weight[i] == '135':
            fighter_names_135.append(fighter[i])
        elif weight[i] == '145':
            fighter_names_145.append(fighter[i])
        elif weight[i] == '155':
            fighter_names_155.append(fighter[i])
        elif weight[i] == '170':
            fighter_names_170.append(fighter[i])
        elif weight[i] == '185':
            fighter_names_185.append(fighter[i])
        elif weight[i] == '205':
            fighter_names_205.append(fighter[i])
        elif weight[i] == '265':
            fighter_names_265.append(fighter[i])

    # Streamlit UI
    st.title("UFC Fight Outcome Predictor")

    # Weight class options
    weight_class_options = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight", "Welterweight", "Middleweight",
                            "Light Heavyweight", "Heavyweight"]

    # Fix the weight class selector and fighter selection
    weight_class = st.selectbox("Select Weight Class", weight_class_options, key="weight_class_selectbox")

    fighter_names = []  # Initialize as an empty list

    # Populate fighter_names based on the selected weight class
    if weight_class == "Flyweight":
        fighter_names = fighter_names_125
    elif weight_class == "Bantamweight":
        fighter_names = fighter_names_135
    elif weight_class == "Featherweight":
        fighter_names = fighter_names_145
    elif weight_class == "Lightweight":
        fighter_names = fighter_names_155
    elif weight_class == "Welterweight":
        fighter_names = fighter_names_170
    elif weight_class == "Middleweight":
        fighter_names = fighter_names_185
    elif weight_class == "Light Heavyweight":
        fighter_names = fighter_names_205
    elif weight_class == "Heavyweight":
        fighter_names = fighter_names_265


    # Input fields for fighters with unique keys
    col1, col2 = st.columns(2)
    with col1:
        r_fighter = st.selectbox("Select Red Fighter", options=fighter_names, key="red_fighter_selectbox")
    with col2:
        b_fighter = st.selectbox("Select Blue Fighter", options=fighter_names, key="blue_fighter_selectbox")

    # Prediction button with enhanced UI
    if st.button("Predict Outcome"):
        # Fetch data for both fighters using selected names
        fighter_data_r = get_fighter_data(*r_fighter.split())
        fighter_data_b = get_fighter_data(*b_fighter.split())

        if fighter_data_r and fighter_data_b:
            # Prepare data and predict
            fight_data = data_builder(fighter_data_r, fighter_data_b)
            probabilities, predicted_winner = predict_fight_outcome(fight_data, lr)

            # Display results with rounded probabilities
            st.markdown('<div class="Headernew">Fight Prediction Results</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="fighter-text">{r_fighter} (Red Fighter) Win Probability: <b>{probabilities[1] * 100:.2f}%</b></div>',
                unsafe_allow_html=True)
            st.markdown(
                f'<div class="fighter-text">{b_fighter} (Blue Fighter) Win Probability: <b>{probabilities[0] * 100:.2f}%</b></div>',
                unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">🏅 <b>Predicted Winner:</b> {predicted_winner}</div>',
                        unsafe_allow_html=True)

            save_prediction(weight_class, r_fighter, b_fighter, probabilities[1] * 100, probabilities[0] * 100, predicted_winner)
        else:
            st.error("⚠️ Unable to retrieve data for one or both fighters. Please check your selection.")

with tab2:
    # Retrieve and display saved predictions
    st.markdown('<h2>Previous Prediction Results</h2>', unsafe_allow_html=True)
    cur.execute("SELECT * FROM results ORDER BY prediction_time DESC")
    results = cur.fetchall()

    # Display results
    if results:
        for result in results:
            st.markdown(f"""
                <div class="result-box">
                    <p><b>Weight Class:</b> {result[1]}</p>
                    <p><b>Red Fighter:</b> {result[2]} ({result[4]:.2f}% win probability)</p>
                    <p><b>Blue Fighter:</b> {result[3]} ({result[5]:.2f}% win probability)</p>
                    <p><b>Predicted Winner:</b> {result[6]}</p>
                    <p><b>Date:</b> {result[7]}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No previous predictions available.")
