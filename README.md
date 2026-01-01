GMSH FEM Examples & Python Automation
Project Overview / Context
  - This repository was developed as part of the VIP CQEM team at Purdue University. Its purpose is to demonstrate and automate workflows using GMSH for geometry creation, meshing, and preparing Abaqus-ready input files. The repo addresses common challenges in FEM simulations, including creating complex multi-material geometries, generating conformal meshes with shared nodes across interfaces, assigning physical groups for materials and boundaries, and automating post-processing for Abaqus export.

Features / What’s Included
  - Geometry Creation: Boxes, cylinders, rotations, and extrusions.
  - Fragmentation and Boolean Operations: Ensures conformal meshes for multi-material systems.
  - Physical Group Assignment: Assign materials and boundary conditions for FEM solvers.
  - Python Automation for Abaqus Export: Converts raw GMSH output into solver-ready .inp files with grouped *ELEMENT blocks.
  - Example Scripts and Demo Geometries: Airplane model and three cubes joined by faces, ready for inspection and experimentation.

Getting Started / Usage
Dependencies:
  - Python 3.x
  - .geo Script
  - GMSH Python API

Usage Instructions:
  - Run the Python scripts to generate conformal meshes and export Abaqus .inp files.
  - Open GMSH GUI to visually inspect the generated geometry and mesh:
      = gmsh.fltk.run()
  - Refer to the provided documentation for step-by-step workflow guidance.

Learning / Notes for Students
  - All scripts are heavily commented to explain workflow logic, geometry handling, meshing, and Abaqus export.
  - Designed to help future VIP students understand the full GMSH pipeline from geometry creation to solver-ready output.

Acknowledgments / Credits
  - Developed as part of the VIP CQEM team under Dr. Thomas Roth at Purdue University, Fall 2025.
