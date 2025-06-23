from collections import defaultdict

def calculate_daily_metrics(sessions):
    """
    Groups sessions by date and computes daily metrics.
    Returns a dict: {date: {metrics...}, ...}
    """
    daily = defaultdict(list)

    for s in sessions:
        day = s.start.date()
        daily[day].append(s)

    day_scores = {}

    for day, sess_list in daily.items():
        total_time = sum(s.duration for s in sess_list)
        focus_time = sum(s.duration for s in sess_list if s.category in ["productive", "learning"])
        waste_time = sum(s.duration for s in sess_list if s.category == "leisure" and s.hour_of_day >= 21)
        num_switches = len(sess_list)

        avg_mood = sum(s.mood for s in sess_list) / len(sess_list)
        avg_focus = sum(s.focus for s in sess_list) / len(sess_list)

        # Score Calculation (out of 100)
        focus_ratio = focus_time / total_time if total_time else 0
        base_score = focus_ratio * 100
        switch_penalty = num_switches * 0.7
        night_penalty = waste_time * 0.5
        mood_bonus = avg_mood * 2
        focus_bonus = avg_focus * 1.5

        final_score = base_score - switch_penalty - night_penalty + mood_bonus + focus_bonus
        final_score = max(0, min(100, round(final_score, 1)))  # Clamp between 0–100

        day_scores[day] = {
            "score": final_score,
            "focus %": round(focus_ratio * 100, 1),
            "total mins": int(total_time),
            "avg mood": round(avg_mood, 1),
            "avg focus": round(avg_focus, 1),
            "switches": num_switches,
            "waste_at_night": int(waste_time)
        }

    return day_scores
