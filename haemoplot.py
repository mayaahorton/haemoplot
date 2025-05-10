import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file
df = pd.read_csv("stain_dual_volume_summary.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.sort_values('date')

# Plot absorbed, standing, and total volume
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['absorbed_mL'], label='Absorbed Volume (ml)', marker='o')
plt.plot(df['date'], df['standing_mL'], label='Standing Volume (ml)', marker='o')
plt.plot(df['date'], df['total_mL'], label='Total Volume (ml)', marker='x', linestyle='--', color='black')

plt.title("Estimated Blood Volume Over Time")
plt.xlabel("Date")
plt.ylabel("Volume (ml)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("blood_volume_over_time_plot.png")
plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt

# # Load CSV file
# df = pd.read_csv("stain_dual_volume_summary.csv")

# # Basic debug print to check what's in the DataFrame
# print(df.head())

# # Minimal plot: just plot the three volume columns as sequences
# plt.figure()
# plt.plot(df['absorbed_mL'], label='Absorbed')
# plt.plot(df['standing_mL'], label='Standing')
# plt.plot(df['total_mL'], label='Total')
# plt.legend()
# plt.show()
