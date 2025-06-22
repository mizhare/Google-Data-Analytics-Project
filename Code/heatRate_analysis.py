import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")
plt.style.use('dark_background')

palette_activity = {
    'Sedentary': '#FF6EC7',
    'Low Active': '#00FFFF',
    'Active': '#FFD700',
    'Unclassified': '#888888'
}

palette_hr = {
    'Elevated Heart Rate': '#FF2975',
    'Normal Heart Rate': '#39FF14'
}

df = pd.read_csv('../Files/fitbit_user_classification_detailed.csv')
df = df[df['activity_level'].isin(['Sedentary', 'Low Active', 'Active'])]

order = ['Sedentary', 'Low Active', 'Active']

fig, axs = plt.subplots(1, 2, figsize=(16, 6), constrained_layout=True)

# Gráfico 1 — Contagem de usuários por atividade e HR status
sns.countplot(data=df, x='activity_level', hue='heart_rate_status', palette=palette_hr, ax=axs[0], order=order)
axs[0].set_title('User Count by Activity Level and Heart Rate Status', fontsize=16, weight='bold', color='white')
axs[0].set_xlabel('Activity Level', fontsize=12, color='white')
axs[0].set_ylabel('User Count', fontsize=12, color='white')
axs[0].tick_params(colors='white')
axs[0].legend(title='Heart Rate Status', title_fontsize=12, fontsize=10, facecolor='#222222', edgecolor='white')
axs[0].grid(axis='y', linestyle='--', alpha=0.6)

# Rótulos nas barras
for container in axs[0].containers:
    axs[0].bar_label(container, label_type='edge', padding=3, color='white', fontsize=10, fontweight='bold')

# Gráfico 2 — Percentual de usuários com HR elevado por nível de atividade
percent_df = (
    df.groupby(['activity_level', 'heart_rate_status'])
      .size()
      .reset_index(name='count')
)
total_per_activity = percent_df.groupby('activity_level')['count'].transform('sum')
percent_df['percent'] = percent_df['count'] / total_per_activity * 100
elevated_df = percent_df[percent_df['heart_rate_status'] == 'Elevated Heart Rate']

sns.barplot(
    data=elevated_df,
    x='activity_level',
    y='percent',
    hue='activity_level',
    palette=palette_activity,
    ax=axs[1],
    order=order,
    legend=False            # oculta legenda duplicada
)
axs[1].set_title('Percentage of Users with Elevated Heart Rate by Activity Level', fontsize=16, weight='bold', color='white')
axs[1].set_xlabel('Activity Level', fontsize=12, color='white')
axs[1].set_ylabel('Percent (%)', fontsize=12, color='white')
axs[1].set_ylim(0, 100)
axs[1].tick_params(colors='white')
axs[1].grid(axis='y', linestyle='--', alpha=0.6)

# Rótulos nas barras do gráfico de porcentagem
elevated_df_indexed = elevated_df.set_index('activity_level').reindex(order)

for i, v in enumerate(elevated_df_indexed['percent']):
    if pd.notnull(v):
        axs[1].text(i, v + 3, f"{v:.1f}%", color='white', ha='center', fontweight='bold')

plt.suptitle('Association Between Elevated Heart Rate and Activity Level', fontsize=20, weight='bold', color='white', y=1.05)
plt.savefig('elevated_heart_rate_analysis.png', dpi=300, bbox_inches='tight', facecolor='black')
plt.show()