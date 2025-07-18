def generate_daily_summary(score_dict, target_day=None):
    """
    Generates detailed text insights based on a target day from score_dict.
    If target_day is None or not in score_dict, uses the latest day available.

    Returns a string report.
    """
    if not score_dict:
        return "No data available to generate a report."

    sorted_dates = sorted(score_dict.keys())

    # Use target_day if provided and exists in data, else latest available
    if target_day and target_day in score_dict:
        latest_day = target_day
    else:
        latest_day = sorted_dates[-1]

    latest = score_dict[latest_day]

    report = f"🗓️ Report for {latest_day.strftime('%A, %B %d')}:\n"

    report += (
        f"\n🔢 Productivity Score: {latest['score']} | "
        f"Focus Time: {latest['focus %']}% | "
        f"Task Switches: {latest['switches']}"
    )
    report += (
        f"\n😊 Average Mood: {latest['avg mood']} | "
        f"🎯 Average Focus Level: {latest['avg focus']}"
    )
    if latest['waste_at_night'] > 0:
        report += (
            f"\n🌙 You spent {latest['waste_at_night']} minutes on distractions after 9 PM. "
            "Consider reducing late-night distractions for better rest and focus."
        )
    else:
        report += "\n🌙 Great job avoiding distractions after 9 PM!"

    # Attempt comparison with previous day that actually exists (handle date gaps)
    if len(sorted_dates) >= 2:
        # Find the closest previous day before latest_day
        prev_day = None
        for d in reversed(sorted_dates):
            if d < latest_day:
                prev_day = d
                break

        if prev_day is not None:
            prev = score_dict[prev_day]
            diff = round(latest['score'] - prev['score'], 1)

            report += f"\n\n📊 Comparison to previous recorded day ({prev_day.strftime('%A, %B %d')}):"
            if diff > 0:
                report += f"\n📈 Your productivity score improved by {diff} points. Keep up the momentum!"
            elif diff < 0:
                report += (
                    f"\n📉 Your productivity score dropped by {abs(diff)} points. "
                    "Try focusing on fewer task switches or minimizing night distractions."
                )
            else:
                report += "\n➖ Your productivity score remained steady."

            # Mood and focus comparison
            mood_diff = round(latest['avg mood'] - prev['avg mood'], 2)
            focus_diff = round(latest['avg focus'] - prev['avg focus'], 2)

            if mood_diff > 0:
                report += f"\n😊 Your mood improved by {mood_diff} points compared to the previous day."
            elif mood_diff < 0:
                report += f"\n😕 Your mood decreased by {abs(mood_diff)} points; consider self-care."

            if focus_diff > 0:
                report += f"\n🎯 Your average focus level increased by {focus_diff} points."
            elif focus_diff < 0:
                report += f"\n⚠️ Your average focus level dropped by {abs(focus_diff)} points."

        else:
            report += (
                "\n\nℹ️ No earlier day data available for comparison. "
                "Try gathering more data for trend insights."
            )
    else:
        report += (
            "\n\nℹ️ Not enough data for comparison. Keep logging your sessions for more insights!"
        )

    return report
