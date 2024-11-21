# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:04:48 2024

@author: mmora
"""

import pandas as pd
import matplotlib.pyplot as plt

# Define constants
# 0:fl, 1:fr, 2:rl, 3:rr 
wheels_ids = [0, 1, 2, 3]  # Replace with actual wheel IDs if different
columns = ["time", "id", "Flong", "Flat", "Frad", "Mz"]

# Load the data
file_path = "python_dirdyn_test.res"  # Replace with your file path
data = pd.read_csv(file_path, delim_whitespace=True, header=None)

# Extract the time column and reshape the rest into a table
time = data.iloc[:, 0]  # Time is the first column
data_table = data.iloc[:, 1:].values.reshape(-1, len(wheels_ids) * 5)  # Reshape to separate wheel data

# Initialize a dictionary to store data for each wheel
table_force = {i: pd.DataFrame(columns=columns) for i in wheels_ids}

# Populate the dictionary
for i in range(len(wheels_ids)):
    start_col = i * 5
    wheel_data = data_table[:, start_col:start_col + 5]  # Extract 5 columns for the wheel
    table_force[i] = pd.DataFrame(wheel_data, columns=columns[1:])  # Exclude time
    table_force[i].insert(0, "time", time)  # Add the time column back

# Plot data for each wheel
for i in wheels_ids:
    wheel_df = table_force[i]
    
    # Create subplots
    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
    fig.suptitle(f"Wheel Index: {i}", fontsize=16)
    
    # Plot each force/moment
    axes[0].plot(wheel_df["time"], wheel_df["Flong"], label="Force Long")
    axes[0].set_ylabel("Flong")
    axes[0].grid(True)
    
    axes[1].plot(wheel_df["time"], wheel_df["Flat"], label="Force Lat")
    axes[1].set_ylabel("Flat")
    axes[1].grid(True)
    
    axes[2].plot(wheel_df["time"], wheel_df["Frad"], label="Force Rad")
    axes[2].set_ylabel("Frad")
    axes[2].grid(True)
    
    axes[3].plot(wheel_df["time"], wheel_df["Mz"], label="Moment Mz")
    axes[3].set_ylabel("Mz")
    axes[3].set_xlabel("Time")
    axes[3].grid(True)
    
    # Add legends
    for ax in axes:
        ax.legend()
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Plot all indices superimposed
fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
fig.suptitle("All Indices Superimposed", fontsize=16)

for i in wheels_ids:
    wheel_df = table_force[i]
    
    # Superimpose each parameter
    axes[0].plot(wheel_df["time"], wheel_df["Flong"], label=f"Index {i}")
    axes[1].plot(wheel_df["time"], wheel_df["Flat"], label=f"Index {i}")
    axes[2].plot(wheel_df["time"], wheel_df["Frad"], label=f"Index {i}")
    axes[3].plot(wheel_df["time"], wheel_df["Mz"], label=f"Index {i}")

# Label axes for the superimposed plot
axes[0].set_ylabel("Flong")
axes[1].set_ylabel("Flat")
axes[2].set_ylabel("Frad")
axes[3].set_ylabel("Mz")
axes[3].set_xlabel("Time")

# Add legends and grid
for ax in axes:
    ax.legend()
    ax.grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
