
# SetFactory("OpenCASCADE");
import gmsh
import sys

# Initialize gmsh
gmsh.initialize()

# Create a new model
gmsh.model.add("three_cubes")

# Mesh size parameter
lc = 0.2  # mesh size - adjust this value to make mesh finer

# --------------------------------------------------------
# 1. Geometry: Three touching cubes
# --------------------------------------------------------
left  = gmsh.model.occ.addBox(-1, -0.5, 0, 1, 1, 1, tag=1)
mid   = gmsh.model.occ.addBox( 0, -0.5, 0, 1, 1, 1, tag=2)
right = gmsh.model.occ.addBox( 1, -0.5, 0, 1, 1, 1, tag=3)

# Using fragment instead of fuse - this merges touching surfaces but keeps volumes separate

# (3,left) == volume 1 as tag = 1 so on for others
out_dim_tags, out_dim_tags_map = gmsh.model.occ.fragment(
    [(3, left), (3, mid), (3, right)], []
) 
#I tried to use fuse instead of fragment but it didn't work so I used fragment instead so that the surfaces that are touching are merged and the volumes are still separate
# Fuse  == Boolean Union will make the volumes as one which is not what we want

# Synchronize to get the volumes
gmsh.model.occ.synchronize()

# Get all volumes after fragment
all_volumes = gmsh.model.getEntities(3)
print(f"Volumes after fragment: {all_volumes}")
print(f"Fragment output: {out_dim_tags}")
print(f"Fragment map: {out_dim_tags_map}")

# After fragment, we need to identify which volumes correspond to which original cubes
# The fragment map tells us this
# out_dim_tags contains the resulting volumes
# out_dim_tags_map contains the mapping from input to output

# Extract the new volume tags
# Fragment preserves the volumes but may renumber them
volume_tags = [tag for dim, tag in out_dim_tags if dim == 3]
print(f"Volume tags after fragment: {volume_tags}")

# For this simple case with 3 non-overlapping cubes, fragment should preserve them
# We can identify them by their center positions
middle_volumes = []
outer_volumes = []

for dim, tag in out_dim_tags:
    if dim == 3:  # Only volumes
        # Get the center of mass of this volume
        mass = gmsh.model.occ.getCenterOfMass(dim, tag) # We need to get the center of mass of the volume to identify which cube it is in
        x_center = mass[0] #x_center is the x coordinate of the center of mass of the volume mass[0] is the x coordinate and so on for y and z
        print(f"Volume {tag} center X: {x_center}")
        
        # Middle cube is centered around x=0.5
        if -0.1 < x_center < 0.6:  # Middle cube (x: 0 to 1) -0.1 is the left side of the middle cube and 0.6 is the right side of the middle cube
            middle_volumes.append(tag)
        else:  # Left or right cube
            outer_volumes.append(tag)

print(f"Middle volumes: {middle_volumes}")
print(f"Outer volumes: {outer_volumes}")

# --------------------------------------------------------
# 2. Find external surfaces
# --------------------------------------------------------
# Now all touching surfaces are merged, so we just get the boundary
all_surfaces = []
for dim, tag in out_dim_tags:
    if dim == 3:
        volume_surfaces = gmsh.model.getBoundary([(dim, tag)], oriented=False) #If oriented=True, the surfaces are oriented in the same direction as the volume
        for surf_dim, surf_tag in volume_surfaces: #we are just getting the surface tags here they can be negative or positive and we need to make them positive
            if abs(surf_tag) not in all_surfaces: #we are adding the surface tags to the list if they are not already in the list
                all_surfaces.append(abs(surf_tag))

print(f"Total external surfaces: {len(all_surfaces)}")
print(f"External surface tags: {all_surfaces}")

all_external_surfaces = []
for surf_tag in all_surfaces:
    # Check how many volumes this surface is adjacent to and volume tags that the surface is adjacent to
    adjacent_volumes = gmsh.model.getAdjacencies(2, surf_tag) #list of volumes that the surface is adjacent to
    num_adjacent = len(adjacent_volumes[1])   #this is the number of volumes that the surface is adjacent to
    
    print(f"Surface {surf_tag}: adjacent to {num_adjacent} volume(s)")
    
    if num_adjacent == 1:  # External surface (only touches one volume)
        all_external_surfaces.append(surf_tag)
    # else: internal surface (touches 2 volumes)

print(f"External surfaces (filtered): {len(all_external_surfaces)}")
print(f"External surface tags: {all_external_surfaces}")

# --------------------------------------------------------
# 3. Define Physical Groups
# --------------------------------------------------------

# Create Physical Group for external surfaces
if all_surfaces:
    gmsh.model.addPhysicalGroup(2, all_surfaces, tag=3)
    gmsh.model.setPhysicalName(2, 3, "ExternalSurfaces") #dim = 2 and tag = 3 dim =2 is the surface and tag = 3 is the physical group
    print(f"Created physical group for {len(all_surfaces)} external surfaces")

# Volume Block 1: Middle cube only
if middle_volumes:
    gmsh.model.addPhysicalGroup(3, middle_volumes, tag=1)
    gmsh.model.setPhysicalName(3, 1, "MiddleCube") #dim = 3 and tag = 1 dim =3 is the volume and tag = 1 is the physical group

# Volume Block 2: Left and right cubes
if outer_volumes:
    gmsh.model.addPhysicalGroup(3, outer_volumes, tag=2) 
    gmsh.model.setPhysicalName(3, 2, "OuterCubes") #dim = 3 and tag = 2 dim =3 is the volume and tag = 2 is the physical group

# --------------------------------------------------------
# 4. Mesh options for Abaqus export
# --------------------------------------------------------
gmsh.option.setNumber("Mesh.SaveAll", 0)  
gmsh.option.setNumber("Mesh.SaveGroupsOfNodes", 0)
gmsh.option.setNumber("Mesh.SaveGroupsOfElements", 1)
gmsh.option.setNumber("Mesh.ElementOrder", 1)

# Set mesh size
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)

# --------------------------------------------------------
# 5. Generate mesh
# --------------------------------------------------------
# Generate 2D mesh on surfaces first
print("\nGenerating 2D mesh...")
gmsh.model.mesh.generate(2)

# Generate 3D mesh
print("Generating 3D mesh...")
gmsh.model.mesh.generate(3)

# --------------------------------------------------------
# 6. Export
# --------------------------------------------------------
# Export to Abaqus .inp format
gmsh.write("three_cubes_2.inp")
print("\nExported to three_cubes_2.inp")






# Finalize
gmsh.finalize()


print("Summary:")
print("- Volume Block 1 (ELSET): MiddleCube (middle cube only)")
print("- Volume Block 2 (ELSET): OuterCubes (left and right cubes)")
print("- Surface Block (ELSET): ExternalSurfaces (all external faces)")
print("- Touching surfaces between cubes are now merged (conformal mesh)")

