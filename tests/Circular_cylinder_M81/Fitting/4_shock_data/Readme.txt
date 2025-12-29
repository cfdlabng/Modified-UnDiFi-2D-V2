################ Shock Data Generation ################

1. The script shock_data.py requires the following input files:
   - shockpoints.xlsx → Contains the coordinates of shock points.
   - freestream.dat → Contains upstream freestream flow properties.

2. Functionality:
   - The script applies the Rankine-Hugoniot (R-H) relations to compute the downstream flow properties.
   - It uses the upstream flow conditions provided in freestream.dat to calculate the downstream Roe variables at each shock point.

3. Format of freestream.dat:
   - The file should contain upstream flow values in the following format:

        rho = 1
        H   = 0.511949397957628
        u   = 1
        v   = 0

   - Where:
     - rho = Density
     - H   = Total enthalpy
     - u   = x-direction velocity
     - v   = y-direction velocity

Important:
For subsonic Mach numbers, it is recommended to extract (probe) the freestream parameters from a point located just upstream of the shock.  
Use these probed values to populate the freestream.dat file for accurate downstream shock data computation.



