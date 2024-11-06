import sqlite3
from datetime import datetime

# Function to save prediction result to SQLite database
def save_prediction(weight_class, r_fighter, b_fighter, r_prob, b_prob, winner):
    # Open a new connection within the function
    con = sqlite3.connect("searches.db", check_same_thread=False)
    cur = con.cursor()

    prediction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO results (weight_class, red_fighter, blue_fighter, red_win_probability, blue_win_probability, winner, prediction_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (weight_class, r_fighter, b_fighter, r_prob, b_prob, winner, prediction_time))
    con.commit()
    con.close()  # Close the connection after the operation
