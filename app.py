import streamlit as st
from datetime import datetime, timedelta

from app.data_loader import load_csv, filter_by_user, convert_to_sessions
from app.utils import calculate_daily_metrics
from visuals.report_text import generate_daily_summary
from visuals.category_pie import plot_category_pie
from visuals.timeline_chart import plot_timeline_chart
from visuals.heatmap import plot_focus_heatmap
from visuals.trends import plot_daily_trends

st.set_page_config(page_title="Focus Arc", layout="wide")

with st.sidebar:
    st.title("🧠 Focus Arc")
    st.markdown("Visualize your time, focus, and distractions with insight.")

    uploaded_file = st.file_uploader("📂 Upload Time Log CSV", type=["csv"])

    if uploaded_file:
        user_id = st.selectbox("👤 Select User", options=list(range(1, 11)))
        report_range = st.radio("📆 Report Range", ["Yesterday", "Last 7 Days", "Full Month"])

st.title("📊 Focus Arc – Cognitive Productivity Insights")

if uploaded_file:
    try:
        df = load_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Could not read uploaded file: {e}")
        st.stop()
    user_df = filter_by_user(df, user_id)

    if not user_df.empty:
        user_df['date'] = user_df['start_time'].dt.date
        data_min_date = user_df['date'].min()
        data_max_date = user_df['date'].max()
    else:
        st.warning(" No data found for this user.")
        st.stop()

    today = datetime.today().date()

    # Determine date range based on report selection
    if report_range == "Yesterday":
        requested_start = today - timedelta(days=1)
        requested_end = requested_start
    elif report_range == "Last 7 Days":
        requested_end = today
        requested_start = today - timedelta(days=6)
    else:
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        requested_start = first_day_last_month
        requested_end = last_day_last_month

    date_mask = (user_df['date'] >= requested_start) & (user_df['date'] <= requested_end)
    range_df = user_df[date_mask]

    if range_df.empty:
        if report_range == "Yesterday":
            fallback_date = data_max_date
            st.warning(f" No data for Yesterday ({requested_start}).\n Showing the last recorded day: {fallback_date}.")
            fallback_mask = (user_df['date'] == fallback_date)
            range_df = user_df[fallback_mask]
        elif report_range == "Last 7 Days":
            fallback_end = data_max_date
            fallback_start = fallback_end - timedelta(days=6)
            st.warning(f" No data for Last 7 Days ({requested_start}–{requested_end}).\n Showing last recorded week: {fallback_start}–{fallback_end}.")
            range_df = user_df[(user_df['date'] >= fallback_start) & (user_df['date'] <= fallback_end)]
        else:
            fallback_end = data_max_date
            fallback_start = fallback_end - timedelta(days=29)
            st.warning(f" No data for the last 30 days ({requested_start}–{requested_end}).\n Showing last recorded month: {fallback_start}–{fallback_end}.")
            range_df = user_df[(user_df['date'] >= fallback_start) & (user_df['date'] <= fallback_end)]

    sessions = convert_to_sessions(range_df)
    score_dict = calculate_daily_metrics(sessions)
    unique_dates = sorted({s.start.date() for s in sessions})

    if unique_dates:
        selected_day = st.selectbox("📅 Pick a Day for Timeline View", options=unique_dates)
        day_sessions = [s for s in sessions if s.start.date() == selected_day]
        summary = generate_daily_summary(score_dict, target_day=selected_day)

        st.subheader("🧠 Daily Insight Summary")
        st.text_area("Summary", summary, height=180)

        with st.expander("ℹ️ What does this summary mean?"):
            st.markdown("""
            This summary is generated using your productivity score, number of task switches,
            mood, and distractions. It compares the selected day's data with the previous recorded day to give personalized feedback.
            """)

        st.subheader("🍰 Time Distribution by Activity Type")
        st.pyplot(plot_category_pie(day_sessions))

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

        st.subheader("🔥 Focus Heatmap")
        st.pyplot(plot_focus_heatmap(sessions))

        with st.expander("📘 About This Heatmap"):
            st.markdown("""
            Shows average focus level across different hours of the day and days of the week.
            Use it to find when you’re most focused.
            """)

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
