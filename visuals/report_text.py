def generate_daily_summary(score_dict):
    """
    Generates text insights based on latest 2 days in the score_dict.
    Returns a string report.
    """
    if len(score_dict) < 1:
        return "No data available to generate a report."

    sorted_dates = sorted(score_dict.keys())
    latest_day = sorted_dates[-1]
    latest = score_dict[latest_day]

    # Start report
    report = f"🗓️ Report for {latest_day.strftime('%A, %B %d')}:\n"

    report += f"\n🔢 Score: {latest['score']} | Focus: {latest['focus %']}% | Switches: {latest['switches']}"
    report += f"\n😊 Mood: {latest['avg mood']} | 🎯 Avg Focus Level: {latest['avg focus']}"
    if latest['waste_at_night'] > 0:
        report += f"\n🌙 You spent {latest['waste_at_night']} minutes on distractions after 9 PM."

    # Compare to yesterday
    if len(score_dict) >= 2:
        prev_day = sorted_dates[-2]
        prev = score_dict[prev_day]
        diff = round(latest['score'] - prev['score'], 1)

        if diff > 0:
            report += f"\n📈 Your score increased by {diff} from yesterday. Great job bouncing back!"
        elif diff < 0:
            report += f"\n📉 Your score dropped by {abs(diff)} from yesterday. Consider reducing task switches or night use."
        else:
            report += "\n➖ Your score remained the same as yesterday."

    return report
