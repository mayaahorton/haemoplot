import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("stain_dual_volume_summary.csv")

# Basic debug print to show the first few lines of dataframe.
# If there are problems, they'll probably be in the date column
print(df.head())

# Minimal plot: just plot the three volume columns as sequences
# If nothing at all gets plotted, then the main script probably hasn't worked.
plt.figure()
plt.plot(df['absorbed_mL'], label='Absorbed')
plt.plot(df['standing_mL'], label='Standing')
plt.plot(df['total_mL'], label='Total')
plt.legend()
plt.show()
