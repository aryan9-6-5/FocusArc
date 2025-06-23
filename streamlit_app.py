from app.session import Session
import pandas as pd
import streamlit as st
from app.data_loader import load_csv, filter_by_user, filter_by_date, convert_to_sessions
import datetime
df = pd.read_csv("data/large_rich_time_log.csv", parse_dates=["start_time", "end_time"])
sample_row = df.iloc[0]
s = Session(sample_row)
print(s)
st.title("Focus Arc")

user_df = filter_by_user(df, user_id=1)
day_df = filter_by_date(user_df, datetime.date(2025, 4, 3))

sessions = convert_to_sessions(day_df)

# for s in sessions:
#     print(s)
# print(sessions[0].get_summary())

from visuals.category_pie import plot_category_pie
import streamlit as st

# After converting to sessions
fig = plot_category_pie(sessions)
st.pyplot(fig)
