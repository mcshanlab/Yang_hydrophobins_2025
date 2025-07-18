def generate_pymol_selections(input_file, output_file):
    # Open the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Prepare to store the selection commands
    selection_commands = []

    # A counter for naming the interactions
    interaction_counter = 1

    # Loop through each line in the input file
    for line in lines:
        # Skip empty lines or lines that don't have enough columns
        columns = line.split()
        
        if len(columns) < 4:  # Check if there are enough columns
            print(f"Skipping malformed line: {line.strip()}")
            continue

        try:
            # Extract the residue numbers and structure filename
            residue1 = columns[0][:-1]  # Removing the last character (e.g., 'A')
            residue2 = columns[1][:-1]  # Removing the last character (e.g., 'A')
            structure_filename = columns[3]

            # Remove the part after the '.pdb' from the structure filename
            structure_filename = structure_filename.split('.pdb')[0]  # Remove '.pdb' extension

            # Construct the PyMOL selection command
            selection_command = f"select interaction{interaction_counter}, resi {residue1}+{residue2} and {structure_filename}"

            # Skip the specific line format: "select interaction1, resi To+1 and energies.pdb"
            if "resi To+1 and energies" in selection_command:
                print(f"Skipping unwanted selection: {selection_command}")
                continue

            # Append the selection command to the list
            selection_commands.append(selection_command)

            # Increment the interaction counter
            interaction_counter += 1

        except IndexError:
            print(f"Skipping malformed line: {line.strip()}")

    # Write the selection commands to a file, adding a blank line every 10 commands
    with open(output_file, 'w') as out_file:
        for i, command in enumerate(selection_commands):
            out_file.write(command + "\n")
            # Add a blank line after every 10 commands
            if (i + 1) % 10 == 0:
                out_file.write("\n")  # Write a blank line

# Specify the input and output file names
input_file = 'final_interaction_pairs_best10.txt'
output_file = 'pymol_selections.txt'

# Call the function to generate the PyMOL selections and write them to the output file
generate_pymol_selections(input_file, output_file)
