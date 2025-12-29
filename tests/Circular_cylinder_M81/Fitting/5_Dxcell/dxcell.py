import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the filenames
node_file = "na00.1.node"
element_file = "na00.1.ele"

# --- Read Nodes ---
with open(node_file, 'r') as f:
    lines = f.readlines()

total_nodes = int(lines[0].split()[0])
node_data = {}
for line in lines[1:1 + total_nodes]:
    parts = line.strip().split()
    node_id = int(parts[0])
    x = float(parts[1])
    y = float(parts[2])
    node_data[node_id] = (x, y)

# --- Read Elements ---
with open(element_file, 'r') as f:
    lines = f.readlines()

total_elements = int(lines[0].split()[0])
element_data = []
for line in lines[1:1 + total_elements]:
    parts = line.strip().split()
    element_id = int(parts[0])
    n1, n2, n3 = int(parts[1]), int(parts[2]), int(parts[3])
    element_data.append((element_id, n1, n2, n3))

# --- Compute Average Edge Length ---
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

edge_lengths = []

for _, n1, n2, n3 in element_data:
    p1, p2, p3 = node_data[n1], node_data[n2], node_data[n3]
    
    # Compute edge lengths
    l1 = distance(p1, p2)
    l2 = distance(p2, p3)
    l3 = distance(p3, p1)
    
    # Average edge length for this element
    avg_edge = (l1 + l2 + l3) / 3
    edge_lengths.append(avg_edge)

# Compute overall average
overall_avg_edge_length = np.mean(edge_lengths)

# Print result
print(f"\nOverall average edge length: {overall_avg_edge_length:.6f}")
# Save to file
with open("dxcell", "w") as f:
    f.write(f"{overall_avg_edge_length:.10f}\n")


