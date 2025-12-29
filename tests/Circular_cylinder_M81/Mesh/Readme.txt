################ Generating Triangle Format Mesh from SU2 Mesh ################

1. First, create a SU2 mesh with clearly defined boundary names using your preferred mesh generation tool.

2. The script SU2_triangle.py is used to convert the SU2 mesh into Triangle-compatible input files:
   - na00.node
   - na00.poly

3. These files serve as input to the Triangle mesh generator. It produces the full set of mesh files:
   - na00.1.node
   - na00.1.poly
   - na00.1.edge
   - na00.1.ele
   - na00.1.neigh

   These files collectively define the complete triangular mesh.

4. The SU2_triangle.py script automatically calls the Triangle mesh generator provided within the UnDiFi-2D framework.
   - Make sure the path to the Triangle executable is correctly specified in the script.
   -triangle_executable = "../../../../bin/triangle_x86_64"

5. Alternatively, if na00.node and na00.poly are already generated, you can manually run the Triangle mesh generator to produce the remaining files using the command from the terminal
./triangle_x86_64 -nep na00.poly

6. 





