

# ============================================================================
# CONFIGURATION: File paths for input and output
# ============================================================================
input_file = "week15_3"    #  original Abaqus file
output_file = "week15_4"   # Output file with grouped ELEMENT blocks

# ============================================================================
# STEP 1: Read the entire Abaqus .inp file into memory
# ============================================================================
# This reads all lines from the input file and stores them in a list.
# Each line in the file becomes an entry in the 'lines' list.
# We need to read everything first so we can parse and reorganize the content.
with open(input_file, "r") as f:
    lines = f.readlines()

# ============================================================================
# STEP 2: Parse ELSET definitions and ELEMENT blocks from the file
# ============================================================================
# We need two dictionaries to organize the data:
# - elset_dict: Maps each ELSET name to a list of element IDs that belong to it
# - element_dict: Maps each element ID to its full definition line (node connectivity)
elset_dict = {}       # Format: {elset_name: [elem_id1, elem_id2, ...]}
element_dict = {}     # Format: {elem_id: "elem_id, node1, node2, node3, node4"}

current_elset = None  # Tracks which ELSET we're currently reading

# Loop through every line in the file to identify ELSETs and ELEMENT blocks
for line in lines:
    line_strip = line.strip()  # Remove leading/trailing whitespace
    
    # Check if this line starts a new *ELSET block
    # Example: "*ELSET, ELSET=Volume1"
    if line_strip.startswith("*ELSET"):
        # Extract the ELSET name from the line
        # Format is typically: "*ELSET, ELSET=Volume1"
        if "ELSET=" in line_strip:
            # Split on "ELSET=" and take everything after it, then split on comma
            # to get just the ELSET name 
            current_elset = line_strip.split("ELSET=")[1].split(",")[0].strip()
            elset_dict[current_elset] = []  # Initialize empty list for this ELSET
    
    # If we're inside an ELSET block, collect element IDs
    # ELSET blocks contain lists of element IDs that belong to that set
    elif current_elset and line_strip and not line_strip.startswith("*"):
        # Element IDs in ELSET blocks are comma-separated
        # Example: "996, 997, 998" or "996,997,998"
        # Convert each ID to integer and add to the current ELSET's list
        ids = [int(x.strip()) for x in line_strip.split(",") if x.strip()]
        elset_dict[current_elset].extend(ids)
    
    # Check if this line starts a new *ELEMENT block
    # Example: "*ELEMENT, type=C3D4, ELSET=Volume2"
    elif line_strip.startswith("*ELEMENT"):
        # When we hit an ELEMENT block, we're no longer reading an ELSET
        current_elset = None
    
    # If we're not in an ELSET block and this looks like an element definition line
    # Element lines have format: "elem_id, node1, node2, node3, node4"
    elif line_strip and current_elset is None and "," in line_strip:
        # Extract the element ID (first value) and store the entire line
        # This preserves the full element definition including node connectivity
        parts = line_strip.split(",")
        elem_id = int(parts[0].strip())  # First value is the element ID
        element_dict[elem_id] = line_strip  # Store the full line for later use

# ============================================================================
# STEP 3: Group elements by their ELSET names
# ============================================================================
# Create a new dictionary that groups element definition lines by ELSET name.
# This reorganizes the data so that all elements belonging to the same ELSET
# are grouped together, ready to be written as a single *ELEMENT block.
grouped_elements = {}
for elset_name, elem_ids in elset_dict.items():
    # For each ELSET, collect all the element definition lines
    # Only include elements that exist in element_dict (safety check)
    grouped_elements[elset_name] = [element_dict[eid] for eid in elem_ids if eid in element_dict]

# ============================================================================
# STEP 4: Write the new .inp file with grouped ELEMENT blocks
# ============================================================================
with open(output_file, "w") as f_out:
    # ------------------------------------------------------------------------
    # Part 4a: Copy all header information (everything before first *ELEMENT)
    # ------------------------------------------------------------------------
    # Abaqus files contain important header information like *HEADING, *NODE, etc.
    # We preserve all of this exactly as it appears in the original file.
    for line in lines:
        if line.strip().startswith("*ELEMENT"):
            break  # Stop when we reach the first ELEMENT block
        f_out.write(line)  # Write header lines as-is
    
    # ------------------------------------------------------------------------
    # Part 4b: Write grouped ELEMENT blocks (one block per ELSET)
    # ------------------------------------------------------------------------
    # Instead of having multiple *ELEMENT blocks scattered throughout the file,
    # we write one consolidated *ELEMENT block for each ELSET.
    # This makes the file more organized and easier to work with.
    for elset_name, elem_lines in grouped_elements.items():
        # Skip empty ELSETs (safety check)
        if not elem_lines:
            continue
        
        # Determine element type (C3D4 for tetrahedra, CPS3 for triangles, etc.)
        # For simplification, we assume all elements are C3D4 (tetrahedral volume elements)
        # Note: In reality, you might want to detect this from the original file
        elem_type = "C3D4"  # C3D4 = 4-node tetrahedral element
        # For surfaces it is CPS3, For simplicity I wrote all as C3D4 and later on it can be changed to CPS3 howver all surfaces are grouped appropriately regardless
        
        # Write the *ELEMENT block header with the ELSET name
        # Format: "*ELEMENT, TYPE=C3D4, ELSET=Volume1"
        f_out.write(f"*ELEMENT, TYPE={elem_type}, ELSET={elset_name}\n")
        
        # Write all element definition lines for this ELSET
        # Each line contains: element_id, node1, node2, node3, node4
        # These lines are already in the correct format from the original file
        for elem_line in elem_lines:
            f_out.write(f"{elem_line}\n")
        
        # Add a blank line after each ELEMENT block for readability
        f_out.write("\n")
    
    # ------------------------------------------------------------------------
    # Part 4c: Copy everything after the last ELEMENT block
    # ------------------------------------------------------------------------
    # Find the index of the last *ELEMENT block in the original file
    # This helps us identify where the ELEMENT section ends
    last_element_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("*ELEMENT"):
            last_element_index = i
    
    # Copy all remaining content from the original file
    # This includes any sections that come after ELEMENT blocks (boundary conditions,
    # material properties, etc.) - we preserve these exactly as they were
    for line in lines[last_element_index:]:
        # Skip any remaining *ELEMENT blocks since we've already written new ones
        if not line.strip().startswith("*ELEMENT"):
            f_out.write(line)