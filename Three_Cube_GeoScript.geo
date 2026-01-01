// Gmsh project created on Wed Nov 12 11:41:08 2025
SetFactory("OpenCASCADE");
//+
Box(1) = {-1, -0.5, 0, 1, 1, 1}; //Extreme Left
//+
Box(2) = {1, -0.5, 0, 1, 1, 1}; //Extreme Right
//+
Box(3) = {0, -0.5, 0, 1, 1, 1}; //Middle
Physical Volume ("Middle Cube") = {3};
Physical Volume ("Left&Right Cube") = {1,2};
//Physical Volume ("Right") = {2};
Physical Surface("ExternalFaces") = {
  1,
  3,
  4,
  5,
  6,
  8,
  9,
  10,
  11,
  12,
  15,
  16,
  17,
  18
};
Mesh (3);

Mesh.SaveAll = 0;              // Only export physical groups
Mesh.SaveGroupsOfNodes = 0;    // Avoid automatic NSETS
Mesh.SaveGroupsOfElements = 1; // Only physical ELSETs
Mesh.ElementOrder = 1;
Mesh.Format = 1;

