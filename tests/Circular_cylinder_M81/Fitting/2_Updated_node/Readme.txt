################ The UpdateNodeDetectShock Script ################

Purpose:
This script updates the node file and filters out the shock points from a captured flow solution.

1. Required Input Files:
   - na00.1.node → Initial node file used for shock-capturing.
   - vvvv.dat → Captured solution file (e.g., pressure or flow variable data).

2. Output:
   - The script generates an updated node file named: UPDATED_na00.1.node

3. Usage:
   - After execution, replace the original na00.1.node with the UPDATED_na00.1.node.
   - Rename the updated file back to na00.1.node for compatibility.

4. Shock Point Filtering:
   - The script prompts the user to enter a value for Phi_max, used to filter shock points.
   - Recommended values:
     - For hypersonic flow over a cylinder: Phi_max = 3
     - For transonic airfoil: Phi_max between 1.1 and 1.4
     -For other cases see the scatter plot generated and refine the Phi_max accordingly untill the distinct shock appears.

5. Final Output:
   - SHOCK_DETECTED.xlsx → Contains the filtered shock points based on Phi_max.

6. Next Step:
   - These shock points can be used to generate the shock curve using curve fitting techniques.

