import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score
import subprocess
import requests
import requests
import urllib3
import pickle
import csv

# Suppress only the specific InsecureRequestWarning (fuckin shit wasn't working dogshit API)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def predict_fight_outcome(fight_data, model):
    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([fight_data])

    # Align prediction input with the training data columns
    # input_df = pd.get_dummies(pd.DataFrame([data_fight]))
    # input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)

    # Make a prediction
    prediction = model.predict(input_df)
    # Define a manual label mapping
    label_map = {0: "Blue", 1: "Red"}

    # Assuming `prediction` is the model's numeric prediction (e.g., 0 or 1)
    decoded_prediction = label_map[prediction[0]]

    # If the model has probability predictions, get prediction probabilities
    if hasattr(model, "predict_proba"):
        prediction_prob = model.predict_proba(input_df)

    # Return the decoded prediction
    return prediction_prob[0], decoded_prediction


# API call with fighter name passed in
def get_fighter_data(firstName, lastName):
    url = "https://ufc_fighter_stats.p.rapidapi.com/fighter"
    querystring = {"firstName": firstName, "middleName": "&", "lastName": lastName}

    headers = {
        "x-rapidapi-key": "key",  # Replace with your actual API key
        "x-rapidapi-host": "ufc_fighter_stats.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring, verify=False)
    temp = response.json()
    result = [temp['stats']['Stikes']['accuracy'],
              temp['stats']['Takedowns']['accuracy'],
              temp['stats']['offense']['submission avg'],
              temp['stats']['offense']['sig. str. landed. per min'],
              temp['stats']['offense']['takedown avg'],
              temp['stats']['record']['wins'],
              temp['stats']['record']['losses'],
              temp['stats']['record']['draws'],
              temp['stats']['physique']['height'],
              temp['stats']['physique']['reach'],
              temp['stats']['age']]
    return result


def data_builder(data_r, data_b):
    # Replace "None" or None in data_r with 0
    for i in range(len(data_r)):
        if data_r[i] == "None" or data_r[i] is None or data_r[i] == "Not Fighting":
            data_r[i] = 0

    # Do the same for data_b if necessary
    for i in range(len(data_b)):
        if data_b[i] == "None" or data_b[i] is None or data_r[i] == "Not Fighting":
            data_b[i] = 0

    # Build the sample_data dictionary
    sample_data = {
        'B_avg_SIG_STR_pct': float(data_b[0]),
        'B_avg_TD_pct': float(data_b[1]),
        'B_avg_SUB_ATT': float(data_b[2]),
        'B_avg_SIG_STR_landed': float(data_b[3]),
        'B_avg_TD_landed': float(data_b[4]),
        'B_wins': float(data_b[5]),
        'B_losses': float(data_b[6]),
        'B_draw': float(data_b[7]),
        'B_Height_cms': float(data_b[8]),
        'B_Reach_cms': float(data_b[9]),
        'R_avg_SIG_STR_pct': float(data_r[0]),
        'R_avg_TD_pct': float(data_r[1]),
        'R_avg_SUB_ATT': float(data_r[2]),
        'R_avg_SIG_STR_landed': float(data_r[3]),
        'R_avg_TD_landed': float(data_r[4]),
        'R_wins': float(data_r[5]),
        'R_losses': float(data_r[6]),
        'R_draw': float(data_r[7]),
        'R_Height_cms': float(data_r[8]),
        'R_Reach_cms': float(data_r[9]),
        'B_age': float(data_b[10]),
        'R_age': float(data_r[10]),
    }
    return sample_data


def preprocess_fight_data(fight_data):
    # Convert numeric-like strings to floats
    for key, value in fight_data.items():
        try:
            fight_data[key] = float(value) if '.' in str(value) else int(value)
        except ValueError:
            # Leave non-numeric strings as they are (e.g., stance or weight class)
            pass
    return fight_data

# Load the model from the file
with open("model.sav", "rb") as model_file:
    lr = pickle.load(model_file)

fighter_data = pd.read_csv("ufc_master_data.csv")

weight_class = fighter_data["weight"]
fighter_name = fighter_data["name"]

print("Model loaded successfully!")
