import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_daily_trends(score_dict, metrics=["score", "avg mood", "avg focus"]):
    """
    Plots selected daily metrics over time from the score dictionary.
    """
    # Convert to DataFrame
    df = pd.DataFrame(score_dict).T  # Transpose
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))

    for metric in metrics:
        sns.lineplot(data=df, x=df.index, y=metric, label=metric, ax=ax, linewidth=2)

    ax.set_title("📈 Daily Productivity Trends", fontsize=14, weight='bold')
    ax.set_ylabel("Score / Level")
    ax.set_xlabel("Date")
    ax.legend(title="Metric")
    ax.grid(True)
    fig.autofmt_xdate()

    return fig
