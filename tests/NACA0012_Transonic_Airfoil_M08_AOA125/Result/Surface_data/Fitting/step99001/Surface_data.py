
import numpy as np
import re
import matplotlib.pyplot as plt
import os
import pandas as pd

print('\033[1m---------------------------------------------------------------\033[0m')
print('\033[1mTHIS PROGRAM\033[0m')
print('\033[1mFILTERS OUT THE SURFACE DATA FROM THE SOLUTION DATA (vvvv.dat)\033[0m')
print('\n\033[1mTHIS PROGRAM REQUIRES\033[0m')
print('\033[1m1. type.dat\033[0m')
print('\033[1m1. na00.1.poly\033[0m')
print('\033[1m2. vvvv.dat\033[0m')
print('\033[1m---------------------------------------------------------------\033[0m')

# File path
Type = "type.dat"
vvvv_file="vvvv.dat"
poly_file="na99001.1.poly"
all_nodes = []       
#*********************************************************************************************************#
#                           READS POLY FILE AND FILTERS OUT THE SURFACE NODES                             #
#*********************************************************************************************************#

with open(poly_file, "r") as f:
    f.readline()  # Skip first line
    N = int(f.readline().split()[0])  # Number of rows
data_poly = np.genfromtxt(poly_file, skip_header=2, max_rows=N, dtype=int)

# READS TYPE.DAT FILE AND FINDS THE FACE OF INVISID WALL BOUNDARY CONDITION (3)

with open("type.dat", 'r') as file:
    next(file)  # Skip header

    for line in file:
        if not line.strip() or line.strip().startswith('#'):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        face_ID = int(parts[0])
        type_value = parts[1]

        if type_value == '3': #CHECKS FOR INVISID WALL
            matching_rows = data_poly[data_poly[:, -1] == face_ID]
            nodes = matching_rows[:, 1:3].flatten()
            all_nodes.extend(nodes)

# Remove duplicates and sort
nodes = np.unique(all_nodes)

# Final vector of unique sorted nodes
#print("Sorted node IDs:")
print("✅ NUMBER OF SURFACE POINTS =", len(nodes))

#*********************************************************************************************************#
#                           READ THE VVVV.DAT FILE AND EXTRACT THE SURFACE VARIABLES                      #
#*********************************************************************************************************#

# Read all lines at once
with open(vvvv_file, "r") as f:
    lines = f.readlines()

# Extract header lines from the already-read content
title_line = lines[0].strip()
variables_line = lines[1].strip()
zone_line = lines[2].strip()

# Debug print
#print("VARIABLES line:", variables_line)

# Extract variable names
if '=' in variables_line:
    variable_names = variables_line.split('=')[1].strip().split()
    print("✅ VARIABLES=",variable_names)
else:
    raise ValueError(f"'=' not found in VARIABLES line: {variables_line}")

# Find number of nodes (N), elements (E), and where numeric data starts
N, E = None, None
numeric_start = 0

for i, line in enumerate(lines):
    if "ZONE" in line:
        match = re.search(r"N\s*=\s*(\d+)\s+E\s*=\s*(\d+)", line)
        if match:
            N, E = int(match.group(1)), int(match.group(2))
    if re.match(r"^\s*-?\d", line):  # Detect first numeric line
        numeric_start = i
        break

if N is None or E is None:
    raise ValueError("⚠️ WARNING: FAILED TO EXTRACT N (NODES) AND E (ELEMENTS).")

print(f"✅ Extracted N = {N}, E = {E}")

# Read node data (first N rows, starting from numeric_start)
node_data = np.genfromtxt(vvvv_file, skip_header=numeric_start, max_rows=N)

# ✅ Adjust node IDs (1-based to 0-based indexing)
zero_indexed_nodes = nodes - 1  # Make sure 'nodes' is defined earlier

# ✅ Extract the rows corresponding to these nodes
selected_node_data = node_data[zero_indexed_nodes]

# ✅ Output to CSV with headers
df = pd.DataFrame(selected_node_data, columns=variable_names)
df.to_csv("surface_data.csv", index=False)

print("✅ NODE DATA SAVED TO 'SURFACE_DATA.CSV' WITH HEADERS!")
