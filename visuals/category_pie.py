import matplotlib.pyplot as plt

def plot_category_pie(sessions):
    """
    Generates a pie chart of time spent per activity category.
    """

    # Aggregate durations by category
    category_durations = {}
    for s in sessions:
        cat = s.category
        category_durations[cat] = category_durations.get(cat, 0) + s.duration

    # Prepare data
    labels = list(category_durations.keys())
    sizes = list(category_durations.values())

    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        wedgeprops={'edgecolor': 'white'},
        textprops={'fontsize': 10}
    )
    ax.set_title("Time Breakdown by Activity Type", fontsize=14)
    plt.legend(loc="upper left", bbox_to_anchor=(0, 1),fontsize='5')
    return fig  # Return the figure for Streamlit
