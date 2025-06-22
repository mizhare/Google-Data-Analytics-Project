import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

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

df = pd.read_csv("../Files/intensity_by_block.csv")

# Ordenar os dias da semana para eixo X
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df["DayOfWeek"] = pd.Categorical(df["DayOfWeek"], categories=days_order, ordered=True)

# Ordenar os blocos de horário para eixo Y (8 blocos)
hour_order = ['00-03','03-06','06-09','09-12','12-15','15-18','18-21','21-24']
df["HourBlock"] = pd.Categorical(df["HourBlock"], categories=hour_order, ordered=True)

# Pivot para matriz
pivot = df.pivot(index="HourBlock", columns="DayOfWeek", values="AvgIntensity")

base_colors = [
    "#2b0f54",
    "#47FF7F"
]
cmap = LinearSegmentedColormap.from_list("base_colors", base_colors, N=1000)

plt.figure(figsize=(14, 8))

ax = sns.heatmap(
    pivot,
    cmap=cmap,
    linewidths=0.5,
    linecolor="#0d0d0d",
    cbar_kws={"shrink": 0.75, "label": "Average Activity Intensity"},
    square=False,
    annot=False,
    xticklabels=True,
    yticklabels=True
)

# Colocar o eixo X (dias da semana) no topo, horizontal e centralizado
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
plt.xticks(rotation=0, ha='center', fontsize=14)

# Ajustar labels do eixo Y (faixas de hora)
plt.yticks(rotation=0, fontsize=14)

plt.title("Average Activity Intensity by Hour Block and Day", fontsize=24, weight="bold", pad=20)
plt.xlabel("Day of Week", fontsize=18, labelpad=16)
plt.ylabel("Hour Block", fontsize=18, labelpad=15)

plt.tight_layout()
plt.savefig("frequency_days_heatmap2.png", dpi=300, bbox_inches="tight", facecolor="#0d0d0d")
plt.show()