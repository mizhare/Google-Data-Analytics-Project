import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

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

neon_palette = ["#FF66B2", "#00FFFF"]

df_steps = pd.read_csv("../Files/dailySteps_Steps.csv")
df_activity = pd.read_csv("../Files/dailyActivity_Steps.csv")

min_len = min(len(df_steps), len(df_activity))
df_steps = df_steps.iloc[:min_len]
df_activity = df_activity.iloc[:min_len]

indices = np.arange(min_len)
bar_width = 0.4

plt.figure(figsize=(18, 8))

plt.bar(indices - bar_width/2, df_steps["StepTotal"], width=bar_width,
        label="dailySteps_Steps.csv", color=neon_palette[0])

plt.bar(indices + bar_width/2, df_activity["TotalSteps"], width=bar_width,
        label="dailyActivity_Steps.csv", color=neon_palette[1])

padding = 0.3

min_x = -bar_width - padding
max_x = (min_len - 1) + bar_width + padding

plt.xlim(min_x, max_x)

xmax_ceil = math.ceil(max_x / 5) * 5
tick_step = 5

plt.xticks(range(0, int(xmax_ceil) + 1, tick_step))

plt.title("Comparison of Total Steps", fontsize=22, weight='bold')
plt.xlabel("Index (Row Number)", fontsize=18)
plt.ylabel("Total Steps", fontsize=18)

legend = plt.legend(
    title="Source",
    loc='lower left',
    bbox_to_anchor=(0, 0.99),
    fontsize=13,
    title_fontsize=14
)
legend.get_frame().set_facecolor("#111111")
legend.get_frame().set_edgecolor("white")
legend.get_frame().set_alpha(0.9)

sns.despine(trim=True)
plt.tight_layout()

plt.savefig("comparison_total_steps.png", dpi=300, bbox_inches='tight')
plt.show()