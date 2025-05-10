import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load original CSV
INPUT_CSV = "stain_dual_volume_summary.csv"
OUTPUT_CSV = "daily_summary.csv"
PLOT_PATH = "daily_volume_plot.png"

# Load data
df = pd.read_csv(INPUT_CSV)

# Parse and clean date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

# Extract just the date (not time)
df['day'] = df['date'].dt.date

# Group by day and sum the volume columns
daily_df = df.groupby('day')[['absorbed_mL', 'standing_mL', 'total_mL']].sum().reset_index()

# Compute 3-day rolling average of total volume
daily_df['rolling_total_mL'] = daily_df['total_mL'].rolling(window=3, min_periods=1).mean()

# Save the daily summary to a new CSV
daily_df.to_csv(OUTPUT_CSV, index=False)

# Plot daily totals and rolling average
plt.figure(figsize=(12, 6))
plt.plot(daily_df['day'], daily_df['total_mL'], label='Daily Total Volume (ml)', marker='o')
plt.plot(daily_df['day'], daily_df['rolling_total_mL'], label='3-Day Rolling Avg', linestyle='--', color='orange')

plt.title("Daily Estimated Blood Volume with 3-Day Rolling Average")
plt.xlabel("Date")
plt.ylabel("Volume (ml)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(PLOT_PATH)
plt.close()

print(f"Saved daily summary to: {OUTPUT_CSV}")
print(f"Saved plot to: {PLOT_PATH}")
