import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

df = pd.read_csv("../Files/relation_Sleep_Activity.csv")

bins = np.linspace(df["AvgSleepEfficiency"].min(), df["AvgSleepEfficiency"].max(), 7)  # 7 limites => 6 grupos
labels = [f"{round(bins[i],2)} - {round(bins[i+1],2)}" for i in range(len(bins)-1)]
df["SleepEfficiencyGroup"] = pd.cut(df["AvgSleepEfficiency"], bins=bins, labels=labels, include_lowest=True)

neon_palette_6 = [
    "#FF40B6",
    "#FF4040",
    "#F19B45",
    "#47C5FF",
    "#9BE574",
    "#E1FF00",
]

plt.figure(figsize=(13, 8))

sns.scatterplot(
    data=df,
    x="AvgActivityRatio",
    y="AvgSleep",
    hue="SleepEfficiencyGroup",
    palette=neon_palette_6,
    s=300,
    edgecolor="white",
    linewidth=1,
    alpha=1
)

sns.regplot(
    data=df,
    x="AvgActivityRatio",
    y="AvgSleep",
    scatter=False,
    color="#00FFFF",
    line_kws={"linewidth": 2.5, "alpha": 0.7},
    ci=None
)

plt.title("Activity vs Sleep", fontsize=22, weight='bold')
plt.xlabel("Activity Ratio (Active Hours / Sedentary Hours)", fontsize=16)
plt.ylabel("Average Sleep Duration (Hours)", fontsize=16)

legend = plt.legend(title="Sleep Efficiency", loc="lower right", fontsize=13, title_fontsize=14)
legend.get_frame().set_facecolor("#111111")
legend.get_frame().set_edgecolor("white")
legend.get_frame().set_alpha(0.9)

sns.despine(trim=True)
plt.tight_layout()

plt.savefig("activity_vs_sleep_neon.png", dpi=300, bbox_inches="tight", facecolor="#0d0d0d")
plt.show()