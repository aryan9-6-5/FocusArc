import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_focus_heatmap(sessions, title="🧠 Focus Intensity Heatmap"):
    """
    Creates a heatmap showing focus level per hour of day vs day of week.
    """
    # Create a DataFrame from session list
    data = []
    for s in sessions:
        data.append({
            "day": s.day_of_week,
            "hour": s.hour_of_day,
            "focus": s.focus
        })

    df = pd.DataFrame(data)

    # Pivot: days as rows, hours as columns
    heatmap_data = df.pivot_table(index="day", columns="hour", values="focus", aggfunc="mean")

    # Reorder days for better layout
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = heatmap_data.reindex(day_order)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.3, linecolor='gray', ax=ax, annot=False)

    ax.set_title(title, fontsize=17, weight='bold')
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week")

    plt.tight_layout()
    return fig
