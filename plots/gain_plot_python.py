import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Load data from LTspice-exported .txt file
file_path = "./data/NJ_Plot_Data.txt"  # change path if needed
with open(file_path, 'r', encoding='latin1') as file:
    lines = file.readlines()

# Extract frequency and gain (dB)
freqs = []
gains_db = []

for line in lines:
    match = re.match(r"([0-9\.e\+\-]+)\s+\(([\d\.e\+\-]+)dB,", line)
    if match:
        freq = float(match.group(1))
        gain_db = float(match.group(2))
        freqs.append(freq)
        gains_db.append(gain_db)

# Store in DataFrame
df = pd.DataFrame({
    "Frequency (Hz)": freqs,
    "Gain (dB)": gains_db
})

# Determine -3 dB cutoff
max_gain = df["Gain (dB)"].max()
cutoff_gain = max_gain - 3
df["Delta"] = abs(df["Gain (dB)"] - cutoff_gain)
cutoff_row = df.loc[df["Delta"].idxmin()]

cutoff_freq = cutoff_row["Frequency (Hz)"]
cutoff_db = cutoff_row["Gain (dB)"]

# Plot
plt.figure(figsize=(9, 5))
plt.semilogx(df["Frequency (Hz)"], df["Gain (dB)"], label="Gain (dB)")
plt.axhline(cutoff_gain, color="red", linestyle="--", label="-3 dB level")
plt.scatter(cutoff_freq, cutoff_db, color="red", zorder=5)
plt.axvline(cutoff_freq, color="gray", linestyle="--")

# Annotate cutoff frequency
plt.text(cutoff_freq, cutoff_db - 1, f"({cutoff_freq/1e6:.2f} MHz, {cutoff_db:.2f} dB)",
         color="red", fontsize=10, ha='right', va='top', bbox=dict(facecolor='white', alpha=0.8))

plt.title("JFET Amplifier Frequency Response")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain (dB)")
plt.grid(True, which='both', linestyle='--')
plt.legend()
plt.tight_layout()
plt.show()
