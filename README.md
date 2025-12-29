##Overview

This repository hosts a modified and extended version of the original UnDiFi-2D shock-fitting solver. The baseline solver can be accessed at:

https://github.com/UnDiFi/UnDiFi-2D

The present work builds upon the original codebase with the objective of improving automation, robustness, and usability, while largely preserving the underlying numerical formulation of UnDiFi-2D.

##Scope of Modifications

The proposed developments consist of two complementary components:
(i) implementation-level enhancements aimed at streamlining the workflow, and
(ii) targeted solver-level extensions to improve the treatment of specific physical configurations.

##Implementation-Level Enhancements

A suite of Python-based utilities has been developed to reduce manual intervention and improve repeatability of the shock-fitting workflow. These enhancements include:

Automated mesh generation

Shock detection from shock-capturing solutions

Refined generation of shock points

Restart mesh creation for shock-fitting runs

Preparation of initial shock data files

Computation of DXCELL values

Boundary-specific data filtering

Collectively, these tools render the overall workflow more systematic, robust, and less dependent on ad hoc user input. In addition, provisions have been added to export convergence histories and diagnostic data, facilitating solver verification, debugging, and post-processing.

##Solver-Level Extensions

In addition to the workflow improvements, the special-point logic of UnDiFi-2D has been extended through the introduction of WDGX and WDGY points. These new special points enable a robust and consistent treatment of shocks emerging from walls or corner geometries, a class of problems that was not fully supported in the original framework.

Furthermore, a correction has been implemented in the handling of regular-reflection (RR) special points to ensure stable and physically consistent behavior.

##Status

The repository reflects ongoing development. Additional features, documentation, and validation cases will be added in future updates.
