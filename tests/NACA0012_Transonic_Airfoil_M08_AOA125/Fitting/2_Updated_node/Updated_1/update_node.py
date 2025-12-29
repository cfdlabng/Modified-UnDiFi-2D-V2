# This program uses the solution file (vvvv.dat) and updates the na00.1.node file.
# Calculates the roe variables √ρ, √ρH, √ρu, √ρv using the values from the solution
# updates the na00.1.node file to be used during shock fitting
# Extracts the shock points based on the maximum pressure ratio of each element
# which is filtered out by the value of phi_max

import numpy as np
import re
import matplotlib.pyplot as plt
import os
import pandas as pd

print('\033[1m---------------------------------------------------------------\033[0m')
print('\033[1mTHIS PROGRAM\033[0m')
print('\033[1m1. UPDATES THE na00.1.node FILE USING THE SOLUTION DATA (vvvv.dat)\033[0m')
print('\033[1m2. DETECTS THE SHOCK POINT AND EXPORTS THEM TO A FILE\033[0m')
print('\n\033[1mTHIS PROGRAM REQUIRES\033[0m')
print('\033[1m1. na00.1.node\033[0m')
print('\033[1m2. vvvv.dat\033[0m')
print('\033[1m---------------------------------------------------------------\033[0m')

# File path
vvvv_file = "vvvv.dat"
node_file = "na00.1.node"
updated_node_file = "UPDATED_na00.1.node"
check_read_data = "check_data.xlsx"

# Check if required files are present
missing_files = []
if not os.path.isfile(vvvv_file):
    missing_files.append(vvvv_file)
if not os.path.isfile(node_file):
    missing_files.append(node_file)

if missing_files:
    print(f"\033[1m⚠️ WARNING: THE FOLLOWING REQUIRED FILE(S) ARE MISSING: {', '.join(missing_files)}\033[0m")
    exit(1)
box_text = "➡️  UPDATING na00.1.node File"
border = "─" * (len(box_text))
print(f"┌{border}┐")
print(f"│ {box_text}│")
print(f"└{border}┘")

# Read file to find N (nodes) and E (elements)
with open(vvvv_file, "r") as f:
    lines = f.readlines()

N, E = None, None
numeric_start = 0

for i, line in enumerate(lines):
    if "ZONE" in line:
        match = re.search(r"N\s*=\s*(\d+)\s+E\s*=\s*(\d+)", line)
        if match:
            N, E = int(match.group(1)), int(match.group(2))
    if re.match(r"^\s*-?\d", line):  # First numeric data line handles -ve values also
        numeric_start = i
        break

if N is None or E is None:
    raise ValueError("⚠️ WARNING: FAILED TO EXTRACT N (NODES) AND E (ELEMENTS).")

print(f"✅ \033[1mExtracted N = {N}, E = {E}\033[0m")

# Read node data (first N rows, 12 columns)
node_data = np.genfromtxt(vvvv_file, skip_header=numeric_start, max_rows=N)

# stores the data 
rho = node_data[:, 2]  # Density
H = node_data[:, 6]  # Total enthalpy
u = node_data[:, 3]  # Velocity in x-direction
v = node_data[:, 4]  # Velocity in y-direction

# Calculate roe variable
sqrt_rho = np.sqrt(rho)  # √ρ
sqrt_rho_H = sqrt_rho * H  # √ρH
sqrt_rho_u = sqrt_rho * u  # √ρu
sqrt_rho_v = sqrt_rho * v  # √ρv


# Read the .node file
with open(node_file, "r") as f:
    node_lines = f.readlines()

header = node_lines[0]
node_values = np.loadtxt(node_file, skiprows=1)

# Ensure first and last columns remain integers
node_values[:, 0] = node_values[:, 0].astype(int)
node_values[:, -1] = node_values[:, -1].astype(int)

# Update columns 4-7 with Roe variables
node_values[:, 3:7] = np.column_stack((sqrt_rho, sqrt_rho_H, sqrt_rho_u, sqrt_rho_v))

# Write updated data back to a new .node file
with open(updated_node_file, "w") as f:
    f.write(header)
    np.savetxt(f, node_values, fmt=["%d", "%.6f", "%.6f", "%.6f", "%.6f", "%.6f", "%.6f", "%d"])
print('\033[1m---------------------------------------------------------\033[0m')
print(f"✅ \033[1mUPDATED ROE VARIABLES AND SAVED AS {updated_node_file}\033[0m")
print('\033[1m---------------------------------------------------------\033[0m')

box_text = "➡️  DETECTING SHOCK POINTS"
border = "─" * (len(box_text))
print(f"┌{border}┐")
print(f"│ {box_text}│")
print(f"└{border}┘")
# Process element data and shock detection
element_data = np.genfromtxt(vvvv_file, skip_header=numeric_start + N, max_rows=E, usecols=(0, 1, 2), dtype=int)

# Compute maximum pressure ratio and identify the corresponding nodes
check_data = []
max_pressure_ratio = 0
max_pressure_element = None
element_number = 0
for i in range(len(element_data)):
    q, r, s = element_data[i] - 1  # Convert to 0-based indexing
    p_values = [node_data[q, 5], node_data[r, 5], node_data[s, 5]]  # Pressure values
    max_p = max(p_values)
    min_p = min(p_values)
    p_ratio = max_p / min_p
    check_data.append([q + 1, r + 1, s + 1, *p_values, max_p, min_p, p_ratio])
# Checking for the element with highest pressure value 
    if p_ratio > max_pressure_ratio:
        max_pressure_ratio = p_ratio
        max_pressure_element = (q+1, r+1, s+1)  # Convert back to 1-based indexing
        pressure_values= p_values
        element_number=i+1
        
# Check if the data read is correct
df_shock = pd.DataFrame(check_data, columns=["Node1", "Node2", "Node3", "P1", "P2", "P3", "Max Pressure", "Min Pressure", "Pressure Ratio"])
df_shock.to_excel(check_read_data, index=False)

print('\033[1m-----------------------------------------------------\033[0m')
print(f"✅ \033[1mELEMENT NUMBER WITH MAX PRESSURE RATIO:{element_number}\033[0m")
print(f"✅ \033[1mELEMENT WITH MAX PRESSURE RATIO: Nodes {max_pressure_element}\033[0m")
print(f"✅ \033[1mTHE PRESSURE VALUES:{pressure_values}\033[0m")
print(f"✅ \033[1mMAXIMUM PRESSURE VALUE = {max(pressure_values)}\033[0m")
print(f"✅ \033[1mMINIMUM PRESSURE VALUE = {min(pressure_values)}\033[0m")
print(f"✅ \033[1mMAXIMUM PRESSURE RATIO = {max_pressure_ratio}\033[0m")
print('\033[1m-----------------------------------------------------\033[0m')

# Ask user for phi_max
print('\033[1m--------------------------------------------------------------------------\033[0m')
while True:
    try:
        max_phi = float(input('\033[1mENTER THE VALUE OF PHI_MAX (< MAXIMUM PRESSURE RATIO) =  \033[0m'))
        if max_phi < max_pressure_ratio:
            break
        else:
            print('\n\033[1m⚠️ PHI_MAX MUST BE LESS THAN MAXIMUM PRESSURE RATIO!\n\033[0m')
    except ValueError:
        print('\n\033[1m⚠️ INVALID INPUT! PLEASE ENTER A VALID NUMBER FOR PHI_MAX.\n\033[0m')
print('\033[1m--------------------------------------------------------------------------\033[0m')

shock_data = []
for i in range(len(element_data)):
    q, r, s = element_data[i] - 1
    p_values = [node_data[q, 5], node_data[r, 5], node_data[s, 5]]
    max_p, max_index = max((val, idx) for idx, val in enumerate(p_values))
    min_p, min_index = min((val, idx) for idx, val in enumerate(p_values))
    
    max_index = [q, r, s][max_index]
    min_index = [q, r, s][min_index]
    
    p_ratio = max_p / min_p
    if p_ratio > max_phi:
        x_shock = node_data[max_index, 0]
        y_shock = node_data[max_index, 1]
        shock_data.append([x_shock, y_shock, p_ratio])

if not shock_data:
    print('\033[1m------------------------------------------------------------------------------\033[0m')
    print(f'\033[1m⚠️ WARNING: NO SHOCK POINTS FOUND FOR THE ENTERED PHI_MAX\033[0m')
    print(f'\033[1mCHECK: PHI_MAX < MAXIMUM PRESSURE RATIO\033[0m')
    print('\033[1m------------------------------------------------------------------------------\033[0m')
else:
    print('\033[1m-------------------------------------------------------------------------------\033[0m')
    print('\033[1m✅ SHOCK POINTS HAVE BEEN SUCCESSFULLY IDENTIFIED AND ARE DISPLAYED IN THE PLOT\033[0m')
    print('\033[1m✅ SHOCK POINTS WILL BE EXPORTED ONCE THE PLOT IS CLOSED\033[0m')
    print('\033[1m-------------------------------------------------------------------------------\033[0m')
    
    shock_data = np.array(shock_data)
    x_shock, y_shock = shock_data[:, 0], shock_data[:, 1]
    
    plt.scatter(x_shock, y_shock, color='r', marker='*')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Shock Points')
    # Save as PNG
    plt.savefig("shock_points_plot.png", dpi=300)
    plt.show()
    
    y_sorted = np.sort(y_shock)[::-1]  # Sort y in descending order
    x_sorted = x_shock[np.argsort(y_shock)[::-1]]
    shock_detected = np.column_stack((x_sorted, y_sorted))
    
    if shock_detected.size > 0:
        df = pd.DataFrame(shock_detected, columns=["X", "Y"])
        df.to_excel("SHOCK_DETECTED.xlsx", index=False, float_format="%.6f")
        #np.savetxt('SHOCK_DETECTED.xlsx', shock_detected, fmt='%.6f')
    print('\033[1m-------------------------------------------------------\033[0m')
    print('\033[1m✅ SHOCK POINTS HAVE BEEN EXPORTED TO SHOCK_DETECTED.xlsx\033[0m')
    print('\033[1m-------------------------------------------------------\033[0m')
    
