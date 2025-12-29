import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read Excel data
Type = "type.dat"
vvv_file = "vvvv.dat"
poly_file = "na00.1.poly"
node_file = "na00.1.node"
all_nodes = []
detected_shocks = 'SHOCK_DETECTED.xlsx'
data = pd.read_excel(detected_shocks)

# Extract x and y
x = data.iloc[:, 0].values
y = data.iloc[:, 1].values

# Scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='blue', label='Data Points')
plt.title('Scatter Plot with Reverse Fit Line')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

# Reverse linear fit: x = a*y + b
p_rev = np.polyfit(y, x, 1)
a_inv = 1 / p_rev[0]
b_inv = -p_rev[1] / p_rev[0]

# Fit line: y = a_inv * x + b_inv
x_fit = np.linspace(0, 1, 100)
y_fit = a_inv * x_fit + b_inv
plt.plot(x_fit, y_fit, color='red', linewidth=2, label='Inverted Fit')

# Print and prepare equation
print(f"Inverted Linear Equation: y = {a_inv:.4f}x + {b_inv:.4f}")
eqn_text = f'y = {a_inv:.4f}x + {b_inv:.4f}'

# Smart positioning of equation text (top-left)
xlims = plt.xlim()
ylims = plt.ylim()
x_pos = xlims[0] + 0.05 * (xlims[1] - xlims[0])
y_pos = ylims[1] - 0.05 * (ylims[1] - ylims[0])

plt.text(x_pos, y_pos, eqn_text,
         fontsize=12, color='red', weight='bold',
         bbox=dict(facecolor='white', edgecolor='black'))

# Move legend to bottom right
plt.legend(loc='lower right')

# Save plot
plt.tight_layout()
plt.savefig('reverse_fit_plot.png', dpi=300, bbox_inches='tight')
plt.show()

#*************************************************************************************************#
# BOUNDARY COORDINATES AND PLOT                                                                   #
#*************************************************************************************************#

with open("na00.1.poly", "r") as f:
    f.readline()
    N = int(f.readline().split()[0])
data_poly = np.genfromtxt("na00.1.poly", skip_header=2, max_rows=N, dtype=int)

# READS TYPE.DAT FILE AND FINDS THE FACE OF INVISID WALL BOUNDARY CONDITION (3)

with open("type.dat", 'r') as file:
    next(file)
    for line in file:
        if not line.strip() or line.strip().startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        face_ID = int(parts[0])
        type_value = parts[1]
        if type_value == '3':
            matching_rows = data_poly[data_poly[:, -1] == face_ID]
            nodes = matching_rows[:, 1:3].flatten()
            all_nodes.extend(nodes)

nodes = np.unique(all_nodes)
print("✅ NUMBER OF SURFACE POINTS =", len(nodes))

# Extract node coordinates
with open("na00.1.node", "r") as f:
    header = f.readline().split()
    num_nodes = int(header[0])
    dim = int(header[1])

data_node = np.genfromtxt("na00.1.node", skip_header=1)
surface_coords = data_node[np.isin(data_node[:, 0], nodes), 1:3]
surface_node_ids = data_node[np.isin(data_node[:, 0], nodes), 0]

plt.figure(figsize=(8, 6))
plt.scatter(surface_coords[:, 0], surface_coords[:, 1], color='green', s=10)
plt.title("Scatter Plot of Surface Nodes (Type 3)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis("equal")
plt.tight_layout()
plt.savefig("surface_nodes_plot.png", dpi=300)
plt.show()

# Export to Excel
df_surface = pd.DataFrame({
    'NodeID': surface_node_ids,
    'x': surface_coords[:, 0],
    'y': surface_coords[:, 1]
})
df_surface.to_excel('surface_node_coordinates.xlsx', index=False)
print("✅ Coordinates exported to surface_node_coordinates.xlsx")

# Find the intersection point with surface
a = a_inv
b = b_inv
x_surf = surface_coords[:, 0]
y_surf = surface_coords[:, 1]
distances = np.abs(a * x_surf - y_surf + b) / np.sqrt(a**2 + 1)
closest_indices = np.argsort(distances)[:2]
closest_points = surface_coords[closest_indices]
closest_ids = surface_node_ids[closest_indices]

print("✅ Closest surface points to the fitted line:")
for i, (nid, pt) in enumerate(zip(closest_ids, closest_points)):
    print(f"Point {i+1}: Node {nid}, x = {pt[0]:.6f}, y = {pt[1]:.6f}")

# plt.scatter(closest_points[:, 0], closest_points[:, 1], color='red', s=50, label='Closest Nodes')
# plt.legend()
# plt.savefig("surface_intersection_nodes.png", dpi=300)
# plt.show()

# Find actual intersecting segments
print("\n🔍 Searching segments that intersect the fitted line:")
found_segments = []
for nid in closest_ids:
    matching_segments = data_poly[(data_poly[:, 1] == nid) | (data_poly[:, 2] == nid)]
    for segment in matching_segments:
        node1_id = segment[1]
        node2_id = segment[2]
        try:
            idx1 = np.where(surface_node_ids == node1_id)[0][0]
            idx2 = np.where(surface_node_ids == node2_id)[0][0]
        except IndexError:
            continue
        x1, y1 = surface_coords[idx1]
        x2, y2 = surface_coords[idx2]
        y_line1 = a * x1 + b
        y_line2 = a * x2 + b
        t1 = y_line1 - y1
        t2 = y_line2 - y2
        if t1 * t2 < 0:
            found_segments.append(((node1_id, x1, y1), (node2_id, x2, y2)))

for i, ((id1, x1, y1), (id2, x2, y2)) in enumerate(found_segments, 1):
    print(f"✅ Segment {i}: Between Node {id1} ({x1:.6f}, {y1:.6f}) and Node {id2} ({x2:.6f}, {y2:.6f})")

# for (pt1, pt2) in found_segments:
    # plt.plot([pt1[1], pt2[1]], [pt1[2], pt2[2]], 'orange', linewidth=3, label='Intersecting Segment')

# plt.legend()
# plt.savefig("highlighted_intersecting_segments.png", dpi=300)
# plt.show()

# Ask user for segment choice
if found_segments:
    while True:
        try:
            choice = int(input(f"\nEnter segment number (1 to {len(found_segments)}): "))
            if 1 <= choice <= len(found_segments):
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    pt1, pt2 = found_segments[choice - 1]
    x1, y1 = pt1[1], pt1[2]
    x2, y2 = pt2[1], pt2[2]

    # Solve for intersection of lines: surface line (pt1-pt2) and shock line (a*x + b)
    m1 = (y2 - y1) / (x2 - x1)
    c1 = y1 - m1 * x1
    m2 = a
    c2 = b

    x_int = (c2 - c1) / (m1 - m2)
    y_int = m1 * x_int + c1

    print(f"\n📍 Intersection Point: x = {x_int:.6f}, y = {y_int:.6f}")

    # Export intersection point with equation
    with open("intersection_point.dat", "w") as f:
        f.write("# Intersection Point of Shock with Segment\n")
        f.write(f"# Shock Equation: y = {a:.6f}x + {b:.6f}\n")
        f.write("x y\n")
        f.write(f"{x_int:.6f} {y_int:.6f}\n")

    print("📁 Exported intersection_point.dat with equation")

    # Check if point lies on segment
    toler = 1e-8
    tline = (y_int - y1) * (x2 - x1) - (x_int - x1) * (y2 - y1)
    print(f"Tolerance Check Value: {abs(tline):.10f}")
    if abs(tline) <= toler:
        if abs(y2 - y1) > abs(x2 - x1):
            s = (y_int - y1) / (y2 - y1) if y2 != y1 else float('inf')
        else:
            s = (x_int - x1) / (x2 - x1) if x2 != x1 else float('inf')

        if 0.0 <= s <= 1.0:
            print("✅ The intersection point lies on the selected segment.")
        else:
            print("❌ The point lies on the line but outside the segment.")
    else:
        print("❌ The point does NOT lie on the line.")

    # Plot intersection point
    # plt.figure(figsize=(8, 6))
    # plt.plot([x1, x2], [y1, y2], 'orange', label='Chosen Segment')
    # plt.plot(x_fit, y_fit, 'red', label='Shock Fit')
    # plt.scatter(x_int, y_int, color='black', s=60, label='Intersection Point')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.grid(True)
    # plt.legend()
    # plt.axis("equal")
    # plt.title("Intersection of Shock with Surface Segment")
    # plt.savefig("intersection_with_user_segment.png", dpi=300)
    # plt.show()

    # Generate points from intersection using shock equation
    dx = float(input("Enter step size dx: "))
    num_pts = int(input("Enter number of points to generate: "))
    x_vals = x_int + np.arange(0, dx * num_pts, dx)
    y_vals = a * x_vals + b

    points = np.column_stack((x_vals, y_vals))
    np.savetxt("shock_line_points.dat", points, header=f"# Points along shock line from intersection\n# y = {a:.6f}x + {b:.6f}\nx y", fmt="%.6f")
    print("📁 Generated and exported shock_line_points.dat")

else:
    print("❌ No intersecting segments found.")
