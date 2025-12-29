import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read Shock Coordinates
shock_coordinates = pd.read_excel("Top_shock_points.xlsx").values
x = shock_coordinates[:, 0]
y = shock_coordinates[:, 1]

# Read upstream values from freestream.dat
with open("freestream.dat", "r") as file:
    lines = file.readlines()
    rho = float(lines[0].split('=')[1].strip())
    H = float(lines[1].split('=')[1].strip())
    Uu_x = float(lines[2].split('=')[1].strip())
    Uu_y = float(lines[3].split('=')[1].strip())

gm = 1.4  # Define gm explicitly
Uu = np.array([Uu_x, Uu_y])

# Compute derivatives using central differences
dx = np.gradient(x)
dy = np.gradient(y)

# Compute unit tangent vectors
T_mag = np.sqrt(dx**2 + dy**2)
T_unit = np.column_stack((dx / T_mag, dy / T_mag))

# Compute unit normal vectors (initial, uncorrected)
N_unit = np.column_stack((-T_unit[:, 1], T_unit[:, 0]))  # Rotate counterclockwise

# Ensure normals point towards the upstream (incoming flow)
flip_mask = np.dot(N_unit, Uu) > 0
N_unit[flip_mask] *= -1

# Plot the curve
plt.figure()
plt.plot(x, y, 'bo-', linewidth=1.5)
plt.quiver(x, y, T_unit[:, 0], T_unit[:, 1], color='r', scale=10)
plt.quiver(x, y, N_unit[:, 0], N_unit[:, 1], color='g', scale=10)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Curve with Corrected Normal Vectors')
plt.legend(['Curve', 'Tangents', 'Normals'])
plt.axis('equal')
plt.grid()
plt.show()

# Upstream velocity magnitude
Uu_mag = np.linalg.norm(Uu)
Pu = ((gm - 1) / gm) * rho * (H - 0.5 * Uu_mag**2)  # Upstream Pressure Calculation

# Normal and tangential velocity calculation
Uun = np.array([np.dot(Uu, N_unit[i, :]) for i in range(len(x))])
Uut = np.array([np.dot(Uu, T_unit[i, :]) for i in range(len(x))])

# Downstream variables calculation
Udn = np.zeros(len(x))
Ud = np.zeros((len(x), 2))
rhod = np.full(len(x), np.nan)  # Initialize with NaNs to detect missing assignments

# Solving the quadratic equation using Rankine-Hugoniot equations
G = gm / (gm - 1)
for i in range(len(x)):
    C1 = rho * Uun[i]
    C2 = rho * Uun[i]**2 + Pu
    C3 = G * (Pu / rho) + 0.5 * Uun[i]**2
    a = 0.5 - G
    b = G * C2 / C1
    c = -C3
    roots_Udn = np.roots([a, b, c])
    #print(roots_Udn)
    
    # Selecting the valid root
    #tol = 1e-6  # Adjust tolerance if needed
    min_root = roots_Udn[np.argmin(np.abs(roots_Udn))]  # Find root with smallest absolute value
    #print(min_root)
    for j in range(len(roots_Udn)):
        if abs(min_root) < abs(Uun[i]):  # Downstream velocity must be less than Upstream velocity
            Udn[i] = min_root
            break
    #print(Udn[i])
    # Computing the downstream x-velocity and y-velocity
    A = np.array([[N_unit[i, 0], N_unit[i, 1]], [T_unit[i, 0], T_unit[i, 1]]])
    B = np.array([Udn[i], Uut[i]])
    Ud[i, :] = np.linalg.solve(A, B)
    rhod[i] = C1 / Udn[i]
   
# Replace NaN values before stacking
rhod = np.nan_to_num(rhod, nan=1.0)

# Ensure rho has the same length as x
rho_array = np.full_like(x, np.sqrt(rho))

# Prepare data for export
Shock_data = np.column_stack([
    x, y, np.sqrt(rhod), np.sqrt(rhod) * H, np.sqrt(rhod) * Ud[:, 0],
    np.sqrt(rhod) * Ud[:, 1], rho_array, rho_array * H, rho_array * Uu[0], rho_array * Uu[1]
])

# Save to Excel
# Convert to DataFrame
df = pd.DataFrame(Shock_data)

# Write to Excel with scientific notation using xlsxwriter
with pd.ExcelWriter('Top_shock_data.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, header=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Apply scientific format to all cells
    scientific_format = workbook.add_format({'num_format': '0.000000E+00'})
    worksheet.set_column(0, df.shape[1] - 1, None, scientific_format)

