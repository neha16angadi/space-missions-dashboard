import pandas as pd

#Loads the data from the CSV file and parses the dates.
def load_data():
    return pd.read_csv("data/space_missions.csv", parse_dates=["Date"])