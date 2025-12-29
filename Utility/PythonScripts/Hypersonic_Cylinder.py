# === IMPORTS ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === STEP 1: Load Shock Points from Excel ===
shock_data = pd.read_excel("SHOCK_DETECTED.xlsx")
x = shock_data.iloc[:, 0].values
y = shock_data.iloc[:, 1].values

# === STEP 2: Fit a Parabola (x = a*y^2 + b*y + c) ===
coeffs = np.polyfit(y, x, 2)
a, b, c = coeffs
fit_func = lambda y_val: a * y_val**2 + b * y_val + c

print(f"Fitted Equation: x = {a:.4f}y² + {b:.4f}y + {c:.4f}")

# === STEP 3: Load Node Coordinates from .node File ===
with open('na00.1.node') as f:
    lines = f.readlines()
node_count = int(lines[0].split()[0])
node_data = {}
for line in lines[1:node_count + 1]:
    parts = line.strip().split()
    if len(parts) < 3:
        continue
    nid = int(parts[0])
    x_n = float(parts[1])
    y_n = float(parts[2])
    node_data[nid] = (x_n, y_n)

# === STEP 4: Load Boundary Edges from .poly File ===
with open('na00.1.poly') as f:
    lines = f.readlines()
edge_count = int(lines[1].split()[0])
edges = []
for line in lines[2:2 + edge_count]:
    parts = line.strip().split()
    if len(parts) < 3:
        continue
    edge_id = int(parts[0])
    n1 = int(parts[1])
    n2 = int(parts[2])
    edges.append((edge_id, n1, n2))

# === STEP 5: Function to Check Parabola-Edge Intersection ===
def intersects_with_parabola(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    y_samples = np.linspace(min(y1, y2), max(y1, y2), 200)
    x_line = x1 + (x2 - x1) * (y_samples - y1) / (y2 - y1 + 1e-12)
    x_curve = fit_func(y_samples)
    diff = x_line - x_curve
    sign_changes = np.where(np.diff(np.sign(diff)) != 0)[0]
    if len(sign_changes) > 0:
        i = sign_changes[0]
        y_int = y_samples[i]
        x_int = fit_func(y_int)
        return True, (x_int, y_int)
    return False, None

# === STEP 6: Find All Intersections ===
intersections = []
for edge_id, n1, n2 in edges:
    if n1 not in node_data or n2 not in node_data:
        continue
    p1 = node_data[n1]
    p2 = node_data[n2]
    does_intersect, point = intersects_with_parabola(p1, p2)
    if does_intersect:
        intersections.append((edge_id, point))

# === STEP 7: Print Intersections ===
print("\nIntersections with boundary edges:")
for eid, (x_int, y_int) in intersections:
    print(f"Edge {eid}: intersects at ({x_int:.8f}, {y_int:.8f})")

# === STEP 8: Plot Domain, Parabola, and Intersections ===
plt.figure(figsize=(10, 6))

# Plot boundary edges
for _, n1, n2 in edges:
    if n1 in node_data and n2 in node_data:
        x_vals = [node_data[n1][0], node_data[n2][0]]
        y_vals = [node_data[n1][1], node_data[n2][1]]
        plt.plot(x_vals, y_vals, 'k-', linewidth=0.4)

# Plot fitted parabola
y_dense = np.linspace(min(y), max(y), 500)
x_dense = fit_func(y_dense)
plt.plot(x_dense, y_dense, 'r-', label='Fitted Parabola')

# Plot intersection points
for _, pt in intersections:
    plt.plot(pt[0], pt[1], 'go', markersize=5)

# Plot original shock points
plt.scatter(x, y, color='blue', s=10, label='Shock Points')

# Annotate parabola equation
eqn_text = f"x = {a:.4f}y² + {b:.4f}y + {c:.4f}"
x_text = np.min(x) + 0.05 * (np.max(x) - np.min(x))
y_text = np.min(y) + 0.85 * (np.max(y) - np.min(y))
plt.text(x_text, y_text, eqn_text, fontsize=12, color='red', weight='bold')

plt.title('Shock Curve Intersections with Domain Boundary')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("shock_curve_intersections.png", dpi=300)
plt.show()

# === STEP 9: Generate Equally Spaced Points Along Parabola ===
num_points = int(input("Enter number of equally spaced points on the curve: "))

if len(intersections) < 2:
    raise ValueError("At least two intersection points are required to define the range.")

# Use intersection points with min and max y
sorted_intersections = sorted([pt for _, pt in intersections], key=lambda p: p[1])
y_start = sorted_intersections[0][1]
y_end = sorted_intersections[-1][1]

# Generate points
y_eq = np.linspace(y_start, y_end, num_points)
x_eq = fit_func(y_eq)

# === STEP 10: Plot and Save Equally Spaced Points ===
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', s=10, label='Shock Points')
plt.plot(x_dense, y_dense, 'r-', label='Fitted Parabola')
plt.plot(x_eq, y_eq, 'go', label='Equally Spaced Points')

plt.title(f'Parabolic Fit with {num_points} Equally Spaced Points')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f'equally_spaced_{num_points}_points_plot.png', dpi=300)
plt.show()

# Export to Excel
shock_points_df = pd.DataFrame({'x': x_eq, 'y': y_eq})
shock_points_df.to_excel("shockpoints.xlsx", index=False)
print(f"\nEqually spaced points saved to 'shockpoints.xlsx'")

