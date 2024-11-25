"""
import os
import matplotlib.pyplot as plt
import numpy as np

# Get the current working directory (where the script is located)
parent_dir = os.getcwd()

# Dictionaries to store extracted data
data_q = {}
data_qd = {}
data_force = {}

# Iterate through folder numbers
for folder in ["0", "1", "2", "3"]:
    folder_path = os.path.join(parent_dir, folder)
    if os.path.isdir(folder_path):  # Ensure it's a valid folder
        # Process python_dirdyn_q.res
        file_path_q = os.path.join(folder_path, "python_dirdyn_q.res")
        if os.path.isfile(file_path_q):
            with open(file_path_q, "r") as file:
                t, x, y = [], [], []
                for line in file:
                    if line.strip():
                        cols = line.split()
                        t.append(float(cols[0]))
                        x.append(float(cols[1]))
                        y.append(float(cols[2]))
                data_q[int(folder)] = {"t": t, "x": x, "y": y}

        # Process python_dirdyn_qd.res
        file_path_qd = os.path.join(folder_path, "python_dirdyn_qd.res")
        if os.path.isfile(file_path_qd):
            with open(file_path_qd, "r") as file:
                t, vx, vy, speed = [], [], [], []
                for line in file:
                    if line.strip():
                        cols = line.split()
                        t.append(float(cols[0]))
                        vx.append(float(cols[1]))
                        vy.append(float(cols[2]))
                        speed.append(np.sqrt(float(cols[1])**2 + float(cols[2])**2))
                data_qd[int(folder)] = {"t": t, "speed": speed}

        # Process python_dirdyn_force_wheel.res
        file_path_force = os.path.join(folder_path, "python_dirdyn_force_wheel.res")
        if os.path.isfile(file_path_force):
            with open(file_path_force, "r") as file:
                t, forces = [], {2: {"Flong": [], "Flat": [], "Frad": [], "Mz": []},
                                 1: {"Flong": [], "Flat": [], "Frad": [], "Mz": []},
                                 3: {"Flong": [], "Flat": [], "Frad": [], "Mz": []},
                                 4: {"Flong": [], "Flat": [], "Frad": [], "Mz": []}}
                for line in file:
                    if line.strip() and "wheels_ids" not in line:
                        cols = line.split()
                        t.append(float(cols[0]))
                        for i, wheel_id in enumerate([2, 1, 3, 4]):
                            base_idx = i * 5 + 1
                            forces[wheel_id]["Flong"].append(float(cols[base_idx + 1]))
                            forces[wheel_id]["Flat"].append(float(cols[base_idx + 2]))
                            forces[wheel_id]["Frad"].append(float(cols[base_idx + 3]))
                            forces[wheel_id]["Mz"].append(float(cols[base_idx + 4]))
                data_force[int(folder)] = {"t": t, "forces": forces}

# Plot (x, y)
plt.figure(figsize=(10, 8))
for folder, values in data_q.items():
    x, y = values["x"], values["y"]
    plt.plot(-np.array(y), x, label=f'Folder {folder}')
plt.title('(x, y) Plot')
plt.xlabel('y')
plt.ylabel('x')
plt.legend()
plt.grid(True)
plt.show()

# Plot (x, t)
plt.figure(figsize=(10, 8))
for folder, values in data_q.items():
    t, x = values["t"], values["x"]
    plt.plot(t, x, label=f'Folder {folder}')
plt.title('(x, t) Plot')
plt.xlabel('Time (t)')
plt.ylabel('x')
plt.legend()
plt.grid(True)
plt.show()

# Plot (y, t)
plt.figure(figsize=(10, 8))
for folder, values in data_q.items():
    t, y = values["t"], values["y"]
    plt.plot(t, y, label=f'Folder {folder}')
plt.title('(y, t) Plot')
plt.xlabel('Time (t)')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

# Plot Absolute Speed vs. Time
plt.figure(figsize=(10, 8))
for folder, values in data_qd.items():
    t, speed = values["t"], values["speed"]
    plt.plot(t, speed, label=f'Folder {folder}')
plt.title('Absolute Speed vs. Time')
plt.xlabel('Time (t)')
plt.ylabel('Speed (m/s)')
plt.legend()
plt.grid(True)
plt.show()

# Plot Forces for Wheels
force_types = ["Flong", "Flat", "Frad", "Mz"]
for force_type in force_types:
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'{force_type} for All Wheels', fontsize=16)

    for folder, values in data_force.items():
        t = values["t"]
        forces = values["forces"]

        for i, wheel_id in enumerate([2, 1, 3, 4]):
            row, col = divmod(i, 2)
            axs[row, col].plot(t, forces[wheel_id][force_type], label=f'Folder {folder}')
            axs[row, col].set_title(f'Wheel ID={wheel_id}')
            axs[row, col].set_xlabel('Time (t)')
            axs[row, col].set_ylabel(force_type)
            axs[row, col].legend()
            axs[row, col].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Get the current working directory (where the script is located)
parent_dir = os.getcwd()


plot_1 = 0
plot_2 = 0
plot_3 = 0
plot_4 = 1
plot_5 = 1
# Initialize dictionaries to hold dataframes
data_q = {}
data_qd = {}
data_force = {}
data_anglis = {}

# Iterate through folder numbers
for folder in ["0", "1", "2", "3"]:
    folder_path = os.path.join(parent_dir, folder)
    if os.path.isdir(folder_path):  # Ensure it's a valid folder
        # Process python_dirdyn_q.res
        file_path_q = os.path.join(folder_path, "python_dirdyn_q.res")
        if os.path.isfile(file_path_q):
            df_q = pd.read_csv(file_path_q, delim_whitespace=True, header=None)
            df_q = df_q.iloc[:, :3] 
            df_q.columns = ["t", "x", "y"]
            data_q[int(folder)] = df_q
            print(df_q["x"])
            

        # Process python_dirdyn_qd.res
        file_path_qd = os.path.join(folder_path, "python_dirdyn_qd.res")
        if os.path.isfile(file_path_qd):
            df_qd = pd.read_csv(file_path_qd, delim_whitespace=True, header=None)
            df_qd = df_qd.iloc[:, :3] 
            df_qd.columns = ["t", "vx", "vy"]
            df_qd["speed"] = np.sqrt(df_qd["vx"]**2 + df_qd["vy"]**2)
            data_qd[int(folder)] = df_qd
            
        # Process python_dir_dyn_anglis.res    
        file_path_anglis = os.path.join(folder_path, "python_dirdyn_anglis.res")
        if os.path.isfile(file_path_qd):
            df_anglis = pd.read_csv(file_path_anglis, delim_whitespace=True, header=None)
            df_anglis.columns = ["t"] + [
                f"{wheel_id}_{anglis}" for wheel_id in [2, 1, 3, 4] for anglis in ["Id", "anglis"]
            ]
            data_anglis[int(folder)] = df_anglis

        # Process python_dirdyn_force_wheel.res
        file_path_force = os.path.join(folder_path, "python_dirdyn_force_wheel.res")
        if os.path.isfile(file_path_force):
            df_force = pd.read_csv(file_path_force, delim_whitespace=True, header=None)
            df_force.columns = ["t"] + [
                f"{wheel_id}_{force}" for wheel_id in [2, 1, 3, 4] for force in ["Id","Flong", "Flat", "Frad", "Mz"]
            ]
            data_force[int(folder)] = df_force
            
            
if ( plot_1 ):
    # Plot (x, y)
    plt.figure(figsize=(10, 8))
    for folder, df in data_q.items():
        plt.plot(-df["y"], df["x"], label=f'Folder {folder}')
    plt.title('(x, y) Plot')
    plt.xlabel('y')
    plt.ylabel('x')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot (x, t)
    plt.figure(figsize=(10, 8))
    for folder, df in data_q.items():
        plt.plot(df["t"], df["x"], label=f'Folder {folder}')
    plt.title('(x, t) Plot')
    plt.xlabel('Time (t)')
    plt.ylabel('x')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot (y, t)
    plt.figure(figsize=(10, 8))
    for folder, df in data_q.items():
        plt.plot(df["t"], df["y"], label=f'Folder {folder}')
    plt.title('(y, t) Plot')
    plt.xlabel('Time (t)')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot Absolute Speed vs. Time
    plt.figure(figsize=(10, 8))
    for folder, df in data_qd.items():
        plt.plot(df["t"], df["speed"], label=f'Folder {folder}')
    plt.title('Absolute Speed vs. Time')
    plt.xlabel('Time (t)')
    plt.ylabel('Speed (m/s)')
    plt.legend()
    plt.grid(True)
    plt.show()

if(plot_2):
    # Plot Forces for Wheels
    force_types = ["Flong", "Flat", "Frad", "Mz"]
    for force_type in force_types:
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'{force_type} for All Wheels', fontsize=16)

        for folder, df in data_force.items():
            t = df["t"]
            for i, wheel_id in enumerate([2, 1, 3, 4]):
                force_col = f"{wheel_id}_{force_type}"
                row, col = divmod(i, 2)
                axs[row, col].plot(t, df[force_col], label=f'Folder {folder}')
                axs[row, col].set_title(f'Wheel ID={wheel_id}')
                axs[row, col].set_xlabel('Time (t)')
                axs[row, col].set_ylabel(force_type)
                axs[row, col].legend()
                axs[row, col].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

if( plot_3):    
    # Plot Forces for Wheels as a function of Speed (with decreasing speed discarded)
    force_types = ["Flong", "Flat", "Frad", "Mz"]
    for force_type in force_types:
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'{force_type} vs Speed for All Wheels (Speed Decreasing Discarded)', fontsize=16)

        for folder, df in data_force.items():
            t = df["t"]
            # Merge with speed data from df_qd using the "t" column
            df_qd_speed = data_qd[folder]
            merged_df = pd.merge(df, df_qd_speed, on="t", how="left")
            first_index_above_x = merged_df[merged_df['t'] > 2.2].index[0] if not df[df['t'] > 2.2].empty else None
            merged_df = merged_df.iloc[first_index_above_x :].reset_index(drop=True)
            
            # Detect when the speed starts decreasing
            speed = merged_df["speed"]
            speed_derivative = speed.diff()  # First derivative of speed
            first_decreasing_idx = speed_derivative[speed_derivative < 0].index.min()  # First index where speed decreases
            
            if not pd.isna(first_decreasing_idx):  # If a decrease is found
                merged_df = merged_df.iloc[:first_decreasing_idx]  # Discard data after speed starts decreasing

            for i, wheel_id in enumerate([2, 1, 3, 4]):
                force_col = f"{wheel_id}_{force_type}"
                row, col = divmod(i, 2)
                axs[row, col].plot(merged_df["speed"], merged_df[force_col], label=f'Folder {folder}')
                axs[row, col].set_title(f'Wheel ID={wheel_id}')
                axs[row, col].set_xlabel('Speed (m/s)')
                axs[row, col].set_ylabel(force_type)
                axs[row, col].legend()
                axs[row, col].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
             
if(plot_4):    
    # Plot Forces for Wheels as a function of Speed (with decreasing speed discarded)
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'Anlgis vs Speed for All Wheels (Speed Decreasing Discarded)', fontsize=16)

        for folder, df in data_anglis.items():
            t = df["t"]
            # Merge with speed data from df_qd using the "t" column
            df_qd_speed = data_qd[folder]
            merged_df = pd.merge(df, df_qd_speed, on="t", how="left")
            first_index_above_x = merged_df[merged_df['t'] > 2.2].index[0] if not df[df['t'] > 2.2].empty else None
            merged_df = merged_df.iloc[first_index_above_x :].reset_index(drop=True)
            
            # Detect when the speed starts decreasing
            speed = merged_df["speed"]
            speed_derivative = speed.diff()  # First derivative of speed
            first_decreasing_idx = speed_derivative[speed_derivative < 0].index.min()  # First index where speed decreases
            
            if not pd.isna(first_decreasing_idx):  # If a decrease is found
                merged_df = merged_df.iloc[:first_decreasing_idx]  # Discard data after speed starts decreasing

            for i, wheel_id in enumerate([2, 1, 3, 4]):
                anglis_col = f"{wheel_id}_anglis"
                row, col = divmod(i, 2)
                axs[row, col].plot(merged_df["speed"], merged_df[anglis_col], label=f'Folder {folder}')
                axs[row, col].set_title(f'Wheel ID={wheel_id}')
                axs[row, col].set_xlabel('Speed (m/s)')
                axs[row, col].set_ylabel("Anglis (°)")
                axs[row, col].legend()
                axs[row, col].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

if plot_5:
    # Create delta values for front and rear wheel differences
    delta_front = {}
    delta_rear = {}
    delta_front_rear = {}

    # Calculate the delta values for each folder
    for folder, df_anglis in data_anglis.items():
        # Calculate delta front and rear as the average of angles
        delta_front[folder] = (df_anglis["2_anglis"] + df_anglis["1_anglis"]) / 2
        delta_rear[folder] = (df_anglis["3_anglis"] + df_anglis["4_anglis"]) / 2
        
        # Calculate delta front-rear angle difference in degrees
        delta_front_rear[folder] = (delta_front[folder] - delta_rear[folder]) * 180 / np.pi
        
        # Merge with speed data from df_qd using the "t" column
        df_qd_speed = data_qd[folder]
        merged_df = pd.merge(df_anglis, df_qd_speed, on="t", how="left")
        
        # Find the first index where time is above 2.2 and slice the data from there
        first_index_above_x = merged_df[merged_df['t'] > 2.2].index[0] if not merged_df[merged_df['t'] > 2.2].empty else None
        if first_index_above_x is not None:
            merged_df = merged_df.iloc[first_index_above_x:].reset_index(drop=True)
        
        # Detect when the speed starts decreasing
        speed = merged_df["speed"]
        speed_derivative = speed.diff()  # First derivative of speed
        first_decreasing_idx = speed_derivative[speed_derivative < 0].index.min()  # First index where speed decreases
        
        # If a decrease is found, discard data after the speed starts decreasing
        if not pd.isna(first_decreasing_idx):  
            merged_df = merged_df.iloc[:first_decreasing_idx]
        
        # Add the delta front-rear to the merged dataframe
        merged_df["delta_front_rear"] = delta_front_rear[folder]

        # Plot the delta front-rear values for each folder
        plt.plot(merged_df["speed"], merged_df["delta_front_rear"], label=f'Folder {folder}')
    
    # Finalize plot
    plt.xlabel('speed [m/s]')
    plt.ylabel('Delta Anglis [°]')
    plt.legend()
    plt.grid(True)
    plt.show()

