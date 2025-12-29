#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/wait.h>

void helpFunction(char *progName) {
    printf("Usage: %s -s Solver -m Mode -f Flow\n", progName);
    printf("\t-s Solver: neo or eulfs\n");
    printf("\t-m Mode: capturing or fitting\n");
    printf("\t-f Flow: steady or unsteady\n");
    exit(1);
}

int main(int argc, char *argv[]) {
    char *Solver = NULL;
    char *Mode = NULL;
    char *Flow = NULL;
    int opt;

    // Parsing command-line options
    while ((opt = getopt(argc, argv, "s:m:f:")) != -1) {
        switch (opt) {
            case 's':
                Solver = optarg;
                break;
            case 'm':
                Mode = optarg;
                break;
            case 'f':
                Flow = optarg;
                break;
            case '?':
                helpFunction(argv[0]);
                break;
        }
    }

    // Check required options
    if (!Solver || !Mode || !Flow) {
        printf("Some or all of the parameters are empty!\n");
        helpFunction(argv[0]);
    }

    // Function to execute a bash command
    void executeBashCommand(const char* command) {
        if (fork() == 0) { // Child process
            execl("/bin/bash", "bash", "-c", command, (char *)NULL);
            perror("execl");
            exit(1);
        } else { // Parent process
            wait(NULL); // Wait for child process
        }
    }

    // Matching commands with conditions
    if (strcmp(Solver, "neo") == 0 && strcmp(Mode, "capturing") == 0 && strcmp(Flow, "steady") == 0) {
        executeBashCommand("../../bin/triangle2grd << !\nna00.1\n!");
        executeBashCommand("../../bin/na2vvvv << !\nna00.1\n!");
        executeBashCommand("cp NEO_data/textinput/inputfile-exp.txt.SC NEO_data/textinput/inputfile-exp.txt");
        executeBashCommand("echo \"\" > NEO_data/input/vel.dat");
        execl("../../bin/CRD_euler", "CRD_euler", (char *)NULL);
    } else if (strcmp(Solver, "neo") == 0 && strcmp(Mode, "capturing") == 0 && strcmp(Flow, "unsteady") == 0) {
        executeBashCommand("../../bin/triangle2grd << !\nna00.1\n!");
        executeBashCommand("../../bin/na2vvvv << !\nna00.1\n!");
        executeBashCommand("cp NEO_data/textinput/inputfile-exp.txt.SC NEO_data/textinput/inputfile-exp.txt");
        executeBashCommand("echo \"\" > NEO_data/input/vel.dat");
        execl("../../bin/CRD_euler", "CRD_euler", (char *)NULL);
    } else if (strcmp(Solver, "eulfs") == 0 && strcmp(Mode, "capturing") == 0 && strcmp(Flow, "steady") == 0) {
        executeBashCommand("../../bin/triangle2dat-NEW-x86_64 << !\nna00.1\nn\n!");
        executeBashCommand("rm ~/home/.petscrc");
        execl("../../bin/EulFS_x86_64", "EulFS_x86_64", "-itmax", "501", (char *)NULL);
    } else if (strcmp(Solver, "eulfs") == 0 && strcmp(Mode, "capturing") == 0 && strcmp(Flow, "unsteady") == 0) {
        executeBashCommand("../../bin/triangle2dat-NEW-x86_64 << !\nna00.1\nn\n!");
        executeBashCommand("rm ~/home/.petscrc");
        execl("../../bin/EulFS_x86_64", "EulFS_x86_64", "-itmax", "501", (char *)NULL);
    } else if (strcmp(Solver, "neo") == 0 && strcmp(Mode, "fitting") == 0 && strcmp(Flow, "steady") == 0) {
        executeBashCommand("cp NEO_data/textinput/inputfile-exp.txt.SF NEO_data/textinput/inputfile-exp.txt");
        executeBashCommand("echo \"\" > NEO_data/input/vel.dat");
        execl("../../bin/UnDiFi-2D_x86_64", "UnDiFi-2D_x86_64", "0", "100000", "false", "true", "NACA0012_M080_A0", (char *)NULL);
    } else if (strcmp(Solver, "neo") == 0 && strcmp(Mode, "fitting") == 0 && strcmp(Flow, "unsteady") == 0) {
        executeBashCommand("cp NEO_data/textinput/inputfile-exp.txt.SF NEO_data/textinput/inputfile-exp.txt");
        execl("../../bin/UnDiFi-2D_x86_64", "UnDiFi-2D_x86_64", "0", "100000", "false", "false", "NACA0012_M080_A0", (char *)NULL);
    } else if (strcmp(Solver, "eulfs") == 0 && strcmp(Mode, "fitting") == 0 && strcmp(Flow, "steady") == 0) {
        execl("../../bin/UnDiFi-2D_x86_64", "UnDiFi-2D_x86_64", "0", "100000", "true", "true", "NACA0012_M080_A0", (char *)NULL);
    } else if (strcmp(Solver, "eulfs") == 0 && strcmp(Mode, "fitting") == 0 && strcmp(Flow, "unsteady") == 0) {
        execl("../../bin/UnDiFi-2D_x86_64", "UnDiFi-2D_x86_64", "0", "100000", "true", "false", "NACA0012_M080_A0", (char *)NULL);
    }

    perror("execl");
    return 0;
}
