import pandas as pd
from app.session import Session

def load_csv(file_path):
    """
    Loads the CSV file into a pandas DataFrame.
    """
    df = pd.read_csv(file_path, parse_dates=["start_time", "end_time"])
    return df

def get_users(df):
    """
    Returns a sorted list of unique user IDs.
    """
    return sorted(df['user_id'].unique())

def filter_by_user(df, user_id):
    """
    Filters the DataFrame for a specific user.
    """
    return df[df['user_id'] == user_id]

def filter_by_date(df, date):
    """
    Filters the DataFrame for a specific date (datetime.date).
    """
    return df[df['start_time'].dt.date == date]

def convert_to_sessions(df):
    """
    Converts each row into a Session object.
    """
    return [Session(row) for _, row in df.iterrows()]
