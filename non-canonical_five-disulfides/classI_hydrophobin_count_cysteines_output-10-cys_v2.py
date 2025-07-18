import os
import shutil
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from collections import defaultdict

# Configuration
pdb_source_dir = "/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/hydrophobin_models/AF_structures/"
pdb_dest_dir = "./10cys_pdbs_classI/"  # destination directory for copied PDBs

# Ensure destination directory exists
os.makedirs(pdb_dest_dir, exist_ok=True)

# List to store the number of cysteines in each sequence
cysteine_counts = []

# Dictionary to count 10-cysteine proteins per species
species_10cys_count = defaultdict(int)

# Counter for total 10-cysteine sequences
total_10cys = 0

# Open output file to write proteins with exactly 10 cysteines
with open("10cys_classI.txt", "w") as output_file:
    # Grab sequences
    for record in SeqIO.parse("uniprotkb_fungal_hydrophobin_family_2024_11_16.fasta", "fasta"):
        seq = str(record.seq)
        X = ProteinAnalysis(seq)

        # Count the number of cysteines ('C') in the sequence
        cysteine_count = X.count_amino_acids()['C']
        cysteine_counts.append(cysteine_count)

        if cysteine_count == 10:
            total_10cys += 1
            output_file.write(f">{record.id} {record.description}\n{seq}\n")

            # Extract species name
            desc = record.description
            if "OS=" in desc:
                species = desc.split("OS=")[1].split(" ")[0]
            else:
                species = desc.split()[0]
            species_10cys_count[species] += 1

            # Extract UniProt accession (e.g., A0A067NFL5 from record.id)
            try:
                uniprot_id = record.id.split("|")[1] if "|" in record.id else record.id
                pdb_filename = f"AF-{uniprot_id}.pdb"
                pdb_src_path = os.path.join(pdb_source_dir, pdb_filename)
                pdb_dst_path = os.path.join(pdb_dest_dir, pdb_filename)

                if os.path.exists(pdb_src_path):
                    shutil.copy(pdb_src_path, pdb_dst_path)
                else:
                    print(f"Skipped: {pdb_filename} not found.")
            except IndexError:
                print(f"Could not parse UniProt ID from: {record.id}")

# Write species table
with open("10cys_species_table_classI.txt", "w") as table_file:
    table_file.write("Species\tCount\n")
    for species, count in sorted(species_10cys_count.items(), key=lambda x: x[1], reverse=True):
        table_file.write(f"{species}\t{count}\n")

# Write total count
with open("10cys_total_count_classI.txt", "w") as count_file:
    count_file.write(f"Total sequences with exactly 10 cysteines: {total_10cys}\n")
