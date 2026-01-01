// GMSH Aircraft Model
SetFactory("OpenCASCADE");

// --- Fuselage and Nose ---
Cylinder(1) = {0, 0, 0, 5, 0, 0, 0.6}; // Main fuselage
Cone(2) = {5, 0, 0, 1.2, 0, 0, 0.6, 0.0}; // Nose cone
Cone(3) = {0, 0, 0, -1.5, 0, 0, 0.6, 0.2}; // Tail cone

// Union for smooth fuselage
BooleanUnion{ Volume{1, 2, 3}; }{}

// --- Cockpit Canopy (Ellipsoid) ---
Sphere(4) = {1.0, 0, 0.35, 0.35};
Dilate {{1.0, 0, 0.35}, {1, 0.8, 0}} { Volume{4}; }
BooleanUnion{ Volume{1}; }{ Volume{4}; }

// --- Main Wing (Trapezoidal, with Dihedral) ---
Point(10) = {2, -2.2, 0};
Point(11) = {3.9, -1.05, 0};
Point(12) = {3.9, 1.05, 0};
Point(13) = {2, 2.2, 0};
Line(10) = {10, 11};
Line(11) = {11, 12};
Line(12) = {12, 13};
Line(13) = {13, 10};
Curve Loop(20) = {10, 11, 12, 13};
Plane Surface(21) = {20};
outWing[] = Extrude {0, 0, 0.4} { Surface{21}; };
wing = outWing[1];
Rotate {{1, 0, 0}, {2.8, 0, 0.0}, 5*Pi/180} { Volume{wing}; }



// --- Tail Horizontal Wing (with Dihedral) ---
Point(30) = {4.25, -0.9, 0};
Point(31) = {5.25, -0.45, 0};
Point(32) = {5.25, 0.45, 0};
Point(33) = {4.25, 0.9, 0};
Line(30) = {30, 31};
Line(31) = {31, 32};
Line(32) = {32, 33};
Line(33) = {33, 30};
Curve Loop(40) = {30, 31, 32, 33};
Plane Surface(41) = {40};
outTail[] = Extrude {0, 0, 0.25} { Surface{41}; };
tailHorizontal = outTail[1];
Rotate {{1, 0, 0}, {4.75, 0, 0.0}, 3*Pi/180} { Volume{tailHorizontal}; }

// --- Vertical Stabilizer (Tail Fin) ---
Point(50) = {5.0, 0, 0};
Point(51) = {5.55, 0, 0.28};
Point(52) = {5.45, 0, 1.25};
Point(53) = {5.0, 0, 1.55};
Line(50) = {50, 51};
Line(51) = {51, 52};
Line(52) = {52, 53};
Line(53) = {53, 50};
Curve Loop(60) = {50, 51, 52, 53};
Plane Surface(61) = {60};
outVertTail[] = Extrude {0, 0.3, 0} { Surface{61}; };
tailVertical = outVertTail[1];

// --- Engines and Pylons ---
//Cylinder(200) = {2.5, -1.8, 0.05, 1.0, 0, 0, 0.25};
//Cylinder(201) = {2.5,  1.8, 0.05, 1.0, 0, 0, 0.25};
//Box(300) = {2.4, -1.85, 0.0, 0.3, 0.1, -0.35};
//Box(301) = {2.4,  1.75, 0.0, 0.3, 0.1, -0.35};
//Cone(302) = {2.3, -1.8, -0.3, 0.25, 0, 0, 0.22, 0.02};
//Cone(303) = {2.3,  1.8, -0.3, 0.25, 0, 0, 0.22, 0.02};
//Cone(304) = {3.5, -1.8, -0.3, 0.3, 0, 0, 0.22, 0.06};
//Cone(305) = {3.5,  1.8, -0.3, 0.3, 0, 0, 0.22, 0.06};

// --- Boolean Union All Parts ---
BooleanUnion{ Volume{1, wing,tailHorizontal, tailVertical, 200, 201,302, 303, 304, 305}; }{}

// --- Physical Groups for Meshing ---
Physical Volume("Fuselage") = {1};
Physical Volume("Wing") = {wing};
Physical Volume("WingletL") = {wingletL};
Physical Volume("WingletR") = {wingletR};
Physical Volume("TailHorizontal") = {tailHorizontal};
Physical Volume("TailVertical") = {tailVertical};
//Physical Volume("EngineL") = {200};
//Physical Volume("EngineR") = {201};

//Physical Volume("InletL") = {302};
//Physical Volume("InletR") = {303};
//Physical Volume("ExhaustL") = {304};
//Physical Volume("ExhaustR") = {305};


//+
Point(58) = {2, -2.2, 0, 1.0};
//+
Line(62) = {13, 12};
//+
Line(63) = {13, 58};
//+
Line(64) = {11, 58};
//+
Line(65) = {12, 11};
//+
//+
Curve Loop(66) = {4};
//+
Plane Surface(67) = {66};
//+
Curve Loop(67) = {4};
//+
Plane Surface(67) = {67};
//+
Curve Loop(68) = {4};
//+
Plane Surface(67) = {68};
//+
Curve Loop(69) = {65, 64, -63, 62};
//+
Plane Surface(67) = {69};
//+
Extrude {0, 0, -0.25} { Surface{67}; Recombine; }//+
Cylinder(9) = {2.1, -0.9, -0.6, 1, 0, 0, 0.35, 2*Pi};
//+
Cylinder(10) = {2.1, 0.9, -0.6, 1, 0, 0, 0.35, 2*Pi};
BooleanUnion { Volume{67}; }{ Volume{9}; }
BooleanUnion { Volume{67}; }{ Volume{10}; }


//+
Cone(11) = {3.0, -0.9, -0.6, 1, 0, 0, 0.35, 0, 2*Pi};
//+
Cone(12) = {3.0, 0.9, -0.6, 1, 0, 0, 0.35, 0, 2*Pi};
//+
Cylinder(13) = {2.1, -0.9, -0.6, 0.45, 0, 0, 0.2, 2*Pi};
//+
Cylinder(14) = {2.1, 0.9, -0.6, 0.45, 0, 0, 0.2, 2*Pi};
BooleanDifference{ Volume{9}; Delete; }{ Volume{13}; Delete; }
BooleanDifference{ Volume{10}; Delete; }{ Volume{14}; Delete; }
//+
Cone(133) = {1.5, 0, 0, 1, 0, 0, 0.2, 0, 2*Pi};
//+
Rotate {{0, 0, 1}, {0, 0, 0}, Pi} {
    Volume{133}; // Rotate the cone 
}

//+
Point(81) = {4, 0, 0, 1.0};
Point(82) = {5, 0, 0, 1.0};
BooleanUnion { Volume{2}; }{ Volume{133}; }

//+
Point(83) = {0.3, 0.2, -0.1, 1.0};
Point(84) = {0.3,0.2,-1,1.0};

Line(300) = {83,84};
Physical Volume("Wheel Line") = {300};
Extrude {1.5, 0, 0} { Surface{300}; Recombine; }

//+
Cylinder(134) = {0.3, -1.2, -0.2, 0, 0, 0.1, 0.3, 2*Pi};
Rotate {{1, 0, 0}, {0, 0, 0}, Pi/2} {
    Volume{134}; // Rotate the cone 
}


//+

Point(88) = {3.6,-0.3,-0.9,1.0};

Point(89) = {3.6,0.31,-0.5,1.0};
Point(90) = {3.6,0.3,-0.9,1.0};

Physical Volume("Rear Right Line") = {302};

//+
Line(304) = {89, 90};
//+
Point(91) = {3.6, -0.31, -0.5, 1.0};
Line(305) = {91,88};
Cylinder(135) = {3.6, -1.2, 0.3, 0, 0, 0.1, 0.3, 2*Pi};
Rotate {{1, 0, 0}, {0, 0, 0}, Pi/2} {
    Volume{135}; // Rotate the cone 
}
Cylinder(136) = {3.6, -1.2, -0.3, 0, 0, 0.1, 0.3, 2*Pi};
Rotate {{1, 0, 0}, {0, 0, 0}, Pi/2} {
    Volume{136}; // Rotate the cone 
}


//+
Sphere(137) = {1, 0.2, 0, 0.5, -Pi/2, Pi/2, Pi};
Rotate {{1, 0, 0}, {0, 0, 0}, Pi/2} {
    Volume{137}; // Rotate the cone 
}

