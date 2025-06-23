from app.session import Session
import pandas as pd
import streamlit as st
from app.data_loader import load_csv, filter_by_user, filter_by_date, convert_to_sessions
import datetime
df = pd.read_csv("data/large_rich_time_log.csv", parse_dates=["start_time", "end_time"])
st.title("FocusArc")