import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# App modules
from app.data_loader import load_csv, filter_by_user, convert_to_sessions
from app.utils import calculate_daily_metrics
from visuals.report_text import generate_daily_summary
from visuals.category_pie import plot_category_pie
from visuals.timeline_chart import plot_timeline_chart
from visuals.heatmap import plot_focus_heatmap
from visuals.trends import plot_daily_trends

# ---------------------- SIDEBAR ----------------------
st.set_page_config(page_title="Focus Arc", layout="wide")

with st.sidebar:
    st.title("🧠 Focus Arc")
    st.markdown("Visualize your time, focus, and distractions with insight.")

    uploaded_file = st.file_uploader("📂 Upload Time Log CSV", type=["csv"])

    if uploaded_file:
        user_id = st.selectbox("👤 Select User", options=list(range(1, 11)))
        report_range = st.radio("📆 Report Range", ["Yesterday", "Last 7 Days", "Full Month"])

# ---------------------- MAIN PAGE ----------------------
st.title("📊 Focus Arc – Cognitive Productivity Insights")

if uploaded_file:
    df = load_csv(uploaded_file)
    user_df = filter_by_user(df, user_id)

    # Filter by date range
    today = datetime.today().date()
    if report_range == "Yesterday":
        start_date = today - timedelta(days=1)
        end_date = start_date
    elif report_range == "Last 7 Days":
        start_date = today - timedelta(days=7)
        end_date = today
    else:
        start_date = today - timedelta(days=30)
        end_date = today

    date_mask = (user_df['start_time'].dt.date >= start_date) & (user_df['start_time'].dt.date <= end_date)
    range_df = user_df[date_mask]

    sessions = convert_to_sessions(range_df)

    unique_dates = sorted({s.start.date() for s in sessions})
    if unique_dates:
        selected_day = st.selectbox("📅 Pick a Day for Timeline View", options=unique_dates)
        day_sessions = [s for s in sessions if s.start.date() == selected_day]

        score_dict = calculate_daily_metrics(sessions)

        # ------------------ Summary ------------------
        st.subheader("🧠 Daily Insight Summary")
        summary = generate_daily_summary(score_dict)
        st.text_area("Summary", summary, height=180)

        with st.expander("ℹ️ What does this summary mean?"):
            st.markdown("""
            This summary is generated using your productivity score, number of task switches,
            mood, and distractions. It compares today's data with the previous day to give personalized feedback.
            """)

        # ------------------ Pie Chart ------------------
        st.subheader("🍰 Time Distribution by Activity Type")
        st.pyplot(plot_category_pie(sessions))

        with st.expander("📘 About This Chart"):
            st.markdown("""
            <span style='color:#4CAF50'>🟩 Productive</span>: Deep/shallow work sessions  
            <span style='color:#F44336'>🟥 Leisure</span>: Social media, YouTube, etc.  
            <span style='color:#FF9800'>🟧 Break</span>: Short rest, lunch, walks  
            <span style='color:#2196F3'>🟦 Learning</span>: Courses, reading  
            <span style='color:#9C27B0'>🟪 Health</span>: Stretching, exercise, meditation  
            <span style='color:#607D8B'>⬜ Reflective</span>: Journaling, organizing  
            <span style='color:#9E9E9E'>⬛ Neutral</span>: Admin tasks, email
            """, unsafe_allow_html=True)

        # ------------------ Timeline ------------------
        st.subheader(f"🕒 Timeline – {selected_day.strftime('%A, %B %d')}")
        if day_sessions:
            st.pyplot(plot_timeline_chart(day_sessions))
        else:
            st.warning("No sessions available to display timeline for this day.")

        with st.expander("📘 About This Timeline"):
            st.markdown("""
            Visualizes your activity blocks for the **selected day**.
            Use this to reflect on how you structured your most recent days.
            """)

        # ------------------ Heatmap ------------------
        st.subheader("🔥 Focus Heatmap")
        st.pyplot(plot_focus_heatmap(sessions))

        with st.expander("📘 About This Heatmap"):
            st.markdown("""
            Shows average focus level across different hours of the day and days of the week.
            Use it to find when you’re most focused.
            """)

        # ------------------ Trends ------------------
        if len(score_dict) > 1:
            st.subheader("📈 Daily Focus & Mood Trends")
            st.pyplot(plot_daily_trends(score_dict))

            with st.expander("📘 About This Trends Chart"):
                st.markdown("""
                Line plot showing how your productivity score, mood, and focus levels change over days.
                Useful for identifying burnout or positive momentum.
                """)
        else:
            st.info("📈 Not enough data for trends — try selecting 'Last 7 Days' or 'Full Month'.")

    else:
        st.info("Please select a day with available session data to view charts.")
else:
    st.info("👈 Please upload your time log CSV from the sidebar to begin.")
    st.info("💡 You can find a sample CSV in the app folder.")
