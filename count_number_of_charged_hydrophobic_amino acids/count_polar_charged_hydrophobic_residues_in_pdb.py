import os
from Bio.PDB import PDBParser
from collections import defaultdict

# Define your three input folders
input_folders = [
    "/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/used-to-make/domains_rosetta_scoring_hydrophobin",
    "/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/used-to-make/domains_rosetta_scoring_ACP",
    "/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/used-to-make/domains_rosetta_scoring_SH3"
]

# Residue types
charged_residues = {"ASP", "GLU", "ARG", "LYS", "HIS"}
polar_uncharged_residues = {"SER", "THR", "ASN", "GLN", "TYR", "CYS"}
polar_plus_charged_residues = charged_residues.union(polar_uncharged_residues)
hydrophobic_residues = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TRP", "PRO"}

# Combined list for header order
all_tracked_residues = sorted(polar_plus_charged_residues.union(hydrophobic_residues))

# Output summary
output_file = "polar_charged_hydrophobic_summary_percent.txt"

# Initialize parser
parser = PDBParser(QUIET=True)

with open(output_file, "w") as out:
    # Write column header
    header = "Filename\tTotal_AAs\tPolar_Charged_Percent\tHydrophobic_Percent"
    for aa in all_tracked_residues:
        header += f"\t{aa}_Percent"
    out.write(header + "\n")

    for folder in input_folders:
        folder_label = os.path.basename(folder)
        out.write(f"\n### Folder: {folder_label} ###\n")

        for filename in sorted(os.listdir(folder)):
            if filename.endswith("_0001_0001.pdb"):
                filepath = os.path.join(folder, filename)
                try:
                    structure = parser.get_structure(filename, filepath)
                    residue_counts = defaultdict(int)
                    total_residues = 0

                    for model in structure:
                        for chain in model:
                            for residue in chain:
                                if residue.get_id()[0] != ' ':
                                    continue  # skip heteroatoms and water
                                resname = residue.get_resname()
                                total_residues += 1
                                if resname in all_tracked_residues:
                                    residue_counts[resname] += 1

                    if total_residues == 0:
                        continue  # avoid division by zero

                    polar_charged_total = sum(residue_counts[res] for res in polar_plus_charged_residues)
                    hydrophobic_total = sum(residue_counts[res] for res in hydrophobic_residues)

                    line = (
                        f"{filename}\t{total_residues}\t"
                        f"{(polar_charged_total / total_residues) * 100:.2f}\t"
                        f"{(hydrophobic_total / total_residues) * 100:.2f}"
                    )
                    for aa in all_tracked_residues:
                        percent = (residue_counts[aa] / total_residues) * 100
                        line += f"\t{percent:.2f}"
                    out.write(line + "\n")

                except Exception as e:
                    print(f"Error processing {filename}: {e}")
