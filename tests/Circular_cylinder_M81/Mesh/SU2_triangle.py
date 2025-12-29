import numpy as np
import subprocess
import math
print("\n\033[1m--------------------------------------------------------\033[0m")
print("\033[1mTHIS PROGRAM CONVERTS SU2 MESH TO TRIANGLE MESH FORMAT \033[0m")
print("\033[1m--------------------------------------------------------\033[0m")

# Ask user for input values
print("\n\033[1m----------------------------------------------------\033[0m")
print("\033[1mFREESTREAM PROPERTIES\033[0m")
print("\033[1m----------------------------------------------------\033[0m")
rho = float(input("ENTER DENSITY (ρ): "))  # Density
U = float(input("ENTER THE FREESTREAM VELOCITY (U): ")) #Freestream velocity
aoa = float(input("ENTER THE ANGLE OF ATTACK(AOA) IN DEGREE: ")) #Angle of attack
aoa_rad=math.radians(aoa)
u=U*math.cos(aoa_rad)
v=U*math.sin(aoa_rad)
print("VELOCITY IN X DIRECTION: ",u)
print("VELOCITY IN Y DIRECTION: ",v)
#u = float(input("ENTER VELOCITY IN X-DIRECTION (u): "))  # Velocity in x-direction
#v = float(input("ENTER VELOCITY IN Y-DIRECTION (v): "))  # Velocity in y-direction
Ma = float(input("ENTER MACH NUMBER (Ma): "))  # Mach number
gm=1.4
#gm = float(input("GAS CONSTANT (γ): "))# Gas constant (γ)
with open("BoundaryConditions.dat", "w") as f:
    f.write(f"rho: {rho}\n")
    f.write(f"U: {U}\n")
    f.write(f"AOA: {aoa}\n")
    f.write(f"u: {u}\n")
    f.write(f"v: {v}\n")
    f.write(f"Ma: {Ma}\n")
    
    
print("\033[1m----------------------------------------------------\033[0m")

# Ask user if there are any holes in the mesh
holes = []
print("\n\033[1m----------------------------------------------------\033[0m")
print("\033[1mGEOMETRY INFORMATION\033[0m")
print("\033[1m----------------------------------------------------\033[0m")
has_holes = input("DOES THE MESH CONTAIN ANY HOLES? (y/n): ").strip().lower()
if has_holes in ["yes", "y"]:
    num_holes = int(input("ENTER THE NUMBER OF HOLES: "))
    for i in range(num_holes):
        x_hole = float(input(f"\nENTER THE CENTER X-COORDINATE OF HOLE {i+1}: "))
        y_hole = float(input(f"ENTER THE CENTER Y-COORDINATE OF HOLE {i+1}: "))
        holes.append((x_hole, y_hole))
print("\033[1m----------------------------------------------------\n\033[0m")
# File paths
su2_file = "mesh.su2"
nodes_file = "na00.node"
boundaries_file = "na00.poly"

# Initialize variables
npoin = 0
nmark = 0
points = []  # Stores computed values for each node
boundary_data = []  # Stores boundary information
serial_num = 1  # Serial number for boundary elements
marker_dict = {}  # Dictionary to store marker tags with numerical index

# Compute basic properties
rhoE = (1 / (Ma**2 * gm * (gm - 1))) + 0.5  # Total energy per unit mass
e = (rhoE / rho) - 0.5 * (u**2 + v**2)  # Internal energy per unit mass
p = (gm - 1) * rho * e  # Pressure
H = (gm * p / ((gm - 1) * rho)) + 0.5 * (u**2 + v**2)  # Total enthalpy
T = e * (gm**2 / (gm - 1))  # Temperature
s = p / (rho**gm)  # Entropy

# Compute the roe variables
sqrt_rho = np.sqrt(rho)    # √ρ
sqrt_rho_H = sqrt_rho * H  # √ρ H
sqrt_rho_u = sqrt_rho * u  # √ρ u
sqrt_rho_v = sqrt_rho * v  # √ρ v

# Read SU2 file
with open(su2_file, "r") as file:
    lines = file.readlines()
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Extract NPOIN (number of nodes)
        if line.startswith("NPOIN="):
            npoin = int(line.split('=')[1].strip())
            ndime = 2  # Since it's 2D
            
            for j in range(npoin):
                i += 1
                data = list(map(float, lines[i].strip().split()))
                node_num = int(data[2]) + 1  # Shift node number by +1
                
                # Store computed values in correct order
                points.append([
                    node_num, data[0], data[1], sqrt_rho, sqrt_rho_H, sqrt_rho_u, sqrt_rho_v
                ])

        # Extract NMARK (boundary markers)
        if line.startswith("NMARK="):
            nmark = int(line.split('=')[1].strip())
            
            for marker_index in range(1, nmark + 1):  # Assign marker indices from 1
                i += 1  # Move to MARKER_TAG
                marker_tag = lines[i].strip().split('=')[1]  # Extract marker name
                marker_dict[marker_tag] = marker_index  # Store numeric marker index
                
                i += 1
                num_elems = int(lines[i].strip().split('=')[1])  # Extract marker elements
                
                # Read boundary elements
                for _ in range(num_elems):
                    i += 1
                    data = list(map(int, lines[i].strip().split()))
                    boundary_data.append([serial_num, data[1] + 1, data[2] + 1, marker_index])  # Shift node numbers +1
                    serial_num += 1
        
        i += 1  # Move to next line

# Convert to NumPy arrays
points = np.array(points)
boundary_data = np.array(boundary_data, dtype=int)

# Identify boundary nodes
boundary_nodes = set(boundary_data[:, 1]) | set(boundary_data[:, 2])  # Unique nodes in boundary

# Add boundary marker column
boundary_marker_column = np.array([2 if node in boundary_nodes else 0 for node in points[:, 0]])

# Append boundary marker column to points
points = np.column_stack((points, boundary_marker_column))

# Save nodes to text file with the required header
with open(nodes_file, "w") as f:
    f.write(f"{npoin}  {ndime}  4  1\n")  # First row header
    np.savetxt(f, points, fmt="%-12d %-12.6f %-12.6f %-12.6f %-12.6f %-12.6f %-12.6f %-4d")

# Save boundaries to text file with required headers
last_serial = serial_num - 1  # Last serial number in boundary data
with open(boundaries_file, "w") as f:
    f.write(f"0  {ndime}  4  1\n")  # First row
    f.write(f"{last_serial}  1\n")  # Second row
    np.savetxt(f, boundary_data, fmt="%-12d %-8d %-8d %-8d")
    
    # Add hole information at the end of the boundary file
    f.write("\n%number of holes\n")  # Comment
    f.write(f"{len(holes)}\n")  # Number of holes
    for i, (x, y) in enumerate(holes):
        f.write(f"{i+1} {x} {y}\n")  # Hole index and coordinates

# Print marker dictionary (optional)
print("\033[1m----------------------------------------------------\033[0m")
print("MARKER TAGS AND ASSIGNED INDEX:\n")
print("\033[1m----------------------------------------------------\033[0m")
for tag, index in marker_dict.items():
    print(f"{tag}: {index}")
# Print to a file 
with open("marker_tags.dat", "w") as f:
    f.write("MARKER TAGS AND ASSIGNED INDEX:\n")
    f.write("----------------------------------------------------\n")
    for tag, index in marker_dict.items():
        f.write(f"{tag}: {index}\n")

print("\033[1m----------------------------------------------------\033[0m")
print(f"\n\033[1m✅  NODES SAVED IN: {nodes_file}\033[0m")
print(f"\n\033[1m✅  BOUNDARIES SAVED IN: {boundaries_file}\033[0m")
if holes:
    print(f"\n\033[1m✅ HOLE INFORMATION APPENDED TO {boundaries_file}\033[0m")

# Define relative path to executable (go 3 levels up and into bin/)
triangle_executable = "../../../../bin/triangle_x86_64"
boundaries_file = "na00.poly"
print("\n\033[1m----------------------------------------------------\033[0m")
print("▶  RUNNING TRIANGLE MESH GENERATOR...")
print("\033[1m----------------------------------------------------\033\n[0m")
try:
    result = subprocess.run(
        [triangle_executable, "-nep", boundaries_file],
        capture_output=True, text=True, check=True
    )
    print("✅ TRIANGLE EXECUTION SUCCESSFUL!\n")
    print(result.stdout)  # Print Triangle output
    
except subprocess.CalledProcessError as e:
    print("❌ Error executing Triangle:")
    print(e.stderr)
    
#Launch showme for mesh visualization

print("▶ Launching ShowMe for mesh visualization...")
result = subprocess.run(["showme", "na00.1"])

if result.returncode == 0:
    print("✅ ShowMe executed successfully!")
else:
    print(f"⚠️ ShowMe exited with return code {result.returncode}. (This might be normal if you closed the window manually.)")



