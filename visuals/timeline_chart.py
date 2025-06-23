# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from datetime import datetime

# CATEGORY_COLORS = {
#     "productive": "#4CAF50",
#     "leisure": "#F44336",
#     "break": "#FF9800",
#     "learning": "#2196F3",
#     "health": "#9C27B0",
#     "reflective": "#607D8B",
#     "neutral": "#9E9E9E"
# }

# def plot_timeline_chart(sessions, title="Focus Arc: Daily Timeline"):
#     """
#     Enhanced horizontal timeline of activities across the day.
#     """
#     fig, ax = plt.subplots(figsize=(12, len(sessions) * 0.6))

#     for i, s in enumerate(sessions[::-1]):  # Reverse so top is earliest
#         start = mdates.date2num(s.start)
#         end = mdates.date2num(s.end)
#         color = CATEGORY_COLORS.get(s.category, "#CCCCCC")

#         ax.barh(y=i, width=end - start, left=start, height=0.5,
#                 color=color, edgecolor='black')

#         # ax.text(start, i, f"  {s.activity}", va='center', ha='left', fontsize=9, color='white' if s.category in ['leisure', 'productive'] else 'black')

#     # Format x-axis as time of day
#     ax.xaxis_date()
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#     # ax.set_xlim([mdates.date2num(datetime(sessions[0].start.year, sessions[0].start.month, sessions[0].start.day, 6)),
#     #              mdates.date2num(datetime(sessions[0].start.year, sessions[0].start.month, sessions[0].start.day, 24))])
#     ax.set_xlim([
#     mdates.date2num(datetime(sessions[0].start.year, sessions[0].start.month, sessions[0].start.day, 6)),
#     mdates.date2num(datetime(sessions[0].start.year, sessions[0].start.month, sessions[0].start.day, 23, 59)) 
# ])

    
#     ax.set_yticks(range(len(sessions)))
#     ax.set_yticklabels([f"{s.start.strftime('%H:%M')}" for s in sessions[::-1]], fontsize=8)

#     ax.set_title(title, fontsize=14, weight='bold')
#     ax.set_xlabel("Time of Day")
#     ax.set_ylabel("Start Time")
#     plt.legend(loc="upper right", bbox_to_anchor=(0, 1))
#     plt.tight_layout()
#     return fig
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from datetime import datetime

CATEGORY_COLORS = {
    "productive": "#4CAF50",
    "leisure": "#F44336",
    "break": "#FF9800",
    "learning": "#2196F3",
    "health": "#9C27B0",
    "reflective": "#607D8B",
    "neutral": "#9E9E9E"
}

def plot_timeline_chart(sessions, title="Focus Arc: Daily Timeline"):
    """
    Enhanced horizontal timeline of activities across the day with legend.
    """
    fig, ax = plt.subplots(figsize=(12, len(sessions) * 0.6))

    for i, s in enumerate(sessions[::-1]):  # Reverse so top is earliest
        start = mdates.date2num(s.start)
        end = mdates.date2num(s.end)
        color = CATEGORY_COLORS.get(s.category, "#CCCCCC")

        ax.barh(
            y=i,
            width=end - start,
            left=start,
            height=0.5,
            color=color,
        )
        ax.text(
            start,
            i,
            f"                      <- {s.activity}", va='center', ha='left', fontsize=10, color='green' if s.category in ['leisure', 'productive'] else 'black')

    # Format x-axis as time of day
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim([
        mdates.date2num(datetime(sessions[0].start.year, sessions[0].start.month, sessions[0].start.day, 6)),
        mdates.date2num(datetime(sessions[0].start.year, sessions[0].start.month, sessions[0].start.day, 23, 59))
    ])

    ax.set_yticks(range(len(sessions)))
    ax.set_yticklabels([s.start.strftime('%H:%M') for s in sessions[::-1]], fontsize=8)

    ax.set_title(title, fontsize=14, weight='bold')
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Start Time")

    # Custom Legend
    legend_elements = [
        Patch(facecolor=color, edgecolor='black', label=category.capitalize())
        for category, color in CATEGORY_COLORS.items()
    ]
    ax.legend(handles=legend_elements, title="Categories", loc='upper right', bbox_to_anchor=(1.15, 1))

    plt.tight_layout()
    return fig
