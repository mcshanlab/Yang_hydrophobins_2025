import heapq
from collections import defaultdict

# Function to process the input file
def extract_top_10_lowest_energies(input_file, output_file):
    # Open and read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Dictionary to store energy values by structure
    structure_energies = defaultdict(list)
    
    # Parse the lines and group by structure
    for line in lines:
        parts = line.split()
        try:
            energy = float(parts[2])  # The energy score is in the 3rd column
            structure = parts[-1].split('_')[0]  # Get structure name (e.g., 2GVM_P52754_structure)
            structure_energies[structure].append((energy, line))
        except ValueError:
            continue  # In case there are any malformed lines
    
    # Open the output file to write the results
    with open(output_file, 'w') as out_file:
        # Iterate over each structure and find the top 10 lowest energy values
        for structure, energy_lines in structure_energies.items():
            # Get the 10 lowest energies using heapq.nsmallest for efficiency
            lowest_10 = heapq.nsmallest(10, energy_lines, key=lambda x: x[0])
            
            # Write the structure name as a header
            out_file.write(f"Top 10 lowest energies for {structure}:\n")
            
            # Write out the lines with the lowest 10 energy values, maintaining original format
            for _, line in lowest_10:
                out_file.write(line)
            
            out_file.write("\n")  # Add a blank line between structures for clarity

# Main execution block
if __name__ == "__main__":
    input_file = "sorted_energy_breakdown_totalscore.txt"
    output_file = "final_interaction_pairs_best10.txt"
    extract_top_10_lowest_energies(input_file, output_file)
