################ Steps for Running the Case in VSCode ################

1. Shock-Capturing Mode (NEO Solver)
- The number of iterations for the shock-capturing mode can be set in the file:  
  NEO_data/textinput/inputfile-exp.txt.SC  
- Modify the parameter under the option "Maximum number of time steps" to adjust the iteration count.

2. Shock-Fitting Mode
- The number of iterations for the shock-fitting mode can be configured in the run.c file located in the current directory.
- Compile run.c in debug mode to generate the executable run, which should be placed in the test case folder.
- Modify the following line in run.c to set the desired number of time steps:
  
  execl("../../bin/UnDiFi-2D_x86_64", "UnDiFi-2D_x86_64", "0", "100000", "false", "true", "NACA0012_M080_A0", (char *)NULL);

  - The second argument "100000" represents the number of iterations.
  - Other flags represent different mode combinations – modify them as needed.
- Note: This setup is applicable only for the NEO Solver.

3. Terminal Execution
- Running the code directly from the terminal may result in errors.
- It is recommended to use VSCode for building and running the code.

4. VSCode Configuration
- VSCode setup files launch.json and tasks.json are provided for easy configuration.

launch.json:
- Contains two launch configurations:
  - One for shock-capturing
  - One for shock-fitting
- Enable only one configuration at a time by commenting out the other.

tasks.json:
- Used to build the code.
- Compilation directories:
  - NEO/src/ → for shock-capturing (NEO)
  - source/   → for shock-fitting
- Comment/uncomment the respective task sections based on the selected mode.

5. Shock-Fitting Code Compilation
- The shock-fitting code resides in the source/ directory.
- It is compiled using the provided Makefile.
- The Makefile includes the "-g" debug flag by default, ensuring the code is built in debug mode.




