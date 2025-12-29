################ Calculating DXCELL ################

1. DXCELL represents the average cell edge length of the computational domain.

2. It is an essential parameter used to:
   - Uniformly distribute the shock points along the shock curve.
   - Define the shock edge length for mesh reconstruction.

3. Using an appropriate DXCELL value helps in generating a high-quality mesh during the remeshing process.

4. The script dxcell.py requires the following input files:
   - na00.1.node → Contains the node coordinates of the mesh.
   - na00.1.ele  → Contains the element connectivity information.

5. Output:
   - The script produces a file named dxcell , which contains the computed DXCELL value.




