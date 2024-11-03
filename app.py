import streamlit as st
import pandas as pd
from model import *

#fix the html/css

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

# Custom CSS styling for the app, including box spacing
st.markdown('''
    <style>
        .main-title {
            font-size: 2.5em;
            color: #ff4c4c;
            text-align: center;
            font-weight: bold;
        }
        .subheader {
            text-align: center;
            font-size: 1.2em;
            color: #333;
            margin-bottom: 20px;
        }
        .selectbox-label {
            font-weight: bold;
            color: #333;
            margin-bottom: -5px;  /* Adjust gap between label and dropdown */
        }
        /* Reduce margins around selectboxes */
        div[data-testid="stSelectbox"] > div {
            margin-top: -10px;
            margin-bottom: -10px;
        }
        .stButton > button {
            background-color: #ff4c4c;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            margin-top: 20px; /* Adjust margin if needed */
        }
        .result {
            font-size: 1.2em;
            font-weight: bold;
            color: #0073e6;
            text-align: center;
        }
    </style>
''', unsafe_allow_html=True)

# Streamlit UI
st.markdown('<div class="main-title">🥊 UFC Fight Outcome Predictor 🥊</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Select weight class and fighters to predict the winner!</div>', unsafe_allow_html=True)

# Weight class options
weight_class_options = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight", "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"]
fighter_names = []  # Initialize as an empty list

# Add weight class picker
st.markdown('<span class="selectbox-label">Weight Class</span>', unsafe_allow_html=True)
weight_class = st.selectbox(" ", weight_class_options)

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

# Input fields for fighters
col1, col2 = st.columns(2)
with col1:
    st.markdown('<span class="selectbox-label">Select Red Fighter</span>', unsafe_allow_html=True)
    r_fighter = st.selectbox(" ", options=fighter_names, key="red_fighter")
with col2:
    st.markdown('<span class="selectbox-label">Select Blue Fighter</span>', unsafe_allow_html=True)
    b_fighter = st.selectbox(" ", options=fighter_names, key="blue_fighter")

# Single prediction button
if st.button("Predict"):
    # Fetch data for both fighters using selected names
    fighter_data_r = get_fighter_data(*r_fighter.split())
    fighter_data_b = get_fighter_data(*b_fighter.split())

    if fighter_data_r and fighter_data_b:
        # Prepare data and predict
        fight_data = data_builder(fighter_data_r, fighter_data_b)
        probabilities, predicted_winner = predict_fight_outcome(fight_data, lr)

        # Display results
        st.markdown('<div class="result">Results:</div>', unsafe_allow_html=True)
        st.write(f"Blue Fighter Win Probability: **{probabilities[0] * 100:.2f}%**")
        st.write(f"Red Fighter Win Probability: **{probabilities[1] * 100:.2f}%**")
        st.success(f"🏆 Predicted Winner: **{predicted_winner}**")
    else:
        st.error("Unable to retrieve data for one or both fighters.")
