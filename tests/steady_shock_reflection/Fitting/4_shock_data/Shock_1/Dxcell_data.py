import numpy as np

x_vals = []
y_vals = []

with open('sh00.dat', 'r') as f:
    lines = f.readlines()

# Get number of shock points from line 2
nshockpoints = int(lines[1].split()[0])

# Read only nshockpoints lines from the data starting after header
for line in lines[2:2 + nshockpoints]:
    parts = line.strip().split()
    if len(parts) >= 2:
        try:
            x = float(parts[0])
            y = float(parts[1])
            x_vals.append(x)
            y_vals.append(y)
        except ValueError:
            continue  # Skip bad lines

# Convert to numpy arrays
x = np.array(x_vals)
y = np.array(y_vals)

# Print basic info
print(f"Extracted {len(x)} shock points.")
print("First 5 points:")
print(np.column_stack((x, y))[:5])


# Compute total length of the shock curve
diffs = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
total_length = np.sum(diffs)

# Original number of points
n_original = len(x)

print(f"Total shock length = {total_length:.4f}")
print(f"Original number of points = {n_original}")

# Desired number of points: 1 less than original
#n_new = n_original - 1
n_new = int(input("Enter the desired number of shock points: "))

dxcell = total_length / (n_new - 1)

# Print the result
print(f"dxcell to get {n_new} points = {dxcell:.4f}")

# Save to a .dat file
with open("dxcell_info.dat", "w") as f:
    f.write(f"Total shock length = {total_length:.4f}\n")
    f.write(f"Original number of points = {n_original}\n")
    f.write(f"Desired number of points = {n_new}\n")
    f.write(f"dxcell = {dxcell:.4f}\n")
