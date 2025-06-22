import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

sns.set(context="talk", style="dark", font_scale=1.2, rc={
    "axes.facecolor": "#0d0d0d",
    "figure.facecolor": "#0d0d0d",
    "axes.edgecolor": "#CCCCCC",
    "axes.labelcolor": "white",
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#444444",
    "axes.grid": True,
    "grid.linestyle": "--",
})


df = pd.read_csv("../Files/dailyActivity_SummaryByDayOfWeek.csv")

palette = {"Weekday": "#47C5FF", "Weekend": "#FF40B6"}


plt.figure(figsize=(8,5))
sns.barplot(data=df, x="DayType", y="AvgActiveMinutes", hue="DayType", palette=palette, legend=False)
plt.title("Average Active Minutes: Weekday vs Weekend", fontsize=20, weight='bold')
plt.xlabel("Day Type", fontsize=14)
plt.ylabel("Avg Active Minutes", fontsize=14)
sns.despine(trim=True)
plt.tight_layout()

plt.savefig("average_active_minutes_weekday_vs_weekend.png", dpi=300, bbox_inches='tight', facecolor='#0d0d0d')

plt.show()

