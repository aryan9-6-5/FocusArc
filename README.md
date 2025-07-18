# Focus Arc

**Focus Arc** is a Streamlit web application designed to help you visualize your time, focus, and distractions based on your personal time logs. It provides insightful cognitive productivity metrics and interactive charts to help you understand and improve your daily focus habits.

---

## Features

- Upload your personal **Time Log CSV** to analyze your activities.
- Filter by user ID (supports multiple users in one dataset).
- Select report ranges:
  - **Yesterday**
  - **Last 7 Days**
  - **Last Month** (full calendar month)
- Intelligent fallback:
  - If the selected date or range is **not present in your data**, the app automatically shows the **most recent available day/week/month** with a clear warning.
- Visualizations include:
  - **Daily Insight Summary** with productivity scores, distractions, mood analysis.
  - **Time Distribution Pie Chart** by activity type.
  - **Timeline Chart** visualizing daily sessions.
  - **Focus Heatmap** across hours and days.
  - **Daily Focus & Mood Trends** over time.
- Clear explanations and tooltips for all charts.
- Robust CSV file parsing with user-friendly error messages.

---

## How It Works

1. Upload your time log CSV file in the sidebar.  
2. Select a user ID from the available list.  
3. Choose a report range (Yesterday, Last 7 Days, or Last Month).  
4. The app filters the data accordingly and displays interactive visualizations.  
5. If your selected range is missing from the data, the app falls back to the latest available range, informing you via a warning message.  
6. Explore your daily or aggregated data with rich, easy-to-understand charts and summaries.

---

## CSV Data Format Requirements

Your CSV file should include the following columns:

- `user_id`: Numeric or string identifier for users.  
- `start_time`: Timestamp (datetime) indicating when a session started.  
- Other columns related to activity type, mood, focus levels, distractions, etc. as required by your data loader and visualization modules.

*Note*: Date and time columns should be parseable by Pandas datetime functions.

---

## Future Improvements

- Dynamic user list extraction from CSV instead of static user ID selection.  
- Support for multiple file formats (Excel, JSON).  
- Integration with calendar apps (Google Calendar, Outlook) for real-time task syncing.  
- Real-time live data tracking and notifications.  
- Enhanced analytics with machine learning models for personalized productivity recommendations.

---

## Installation & Running

1. Clone this repository.  
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
## Run the app:
   ```bash
   streamlit run app.py

