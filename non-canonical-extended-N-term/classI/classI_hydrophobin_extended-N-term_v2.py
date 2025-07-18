import os
import shutil
from Bio import SeqIO
from collections import defaultdict

# Configuration
pdb_source_dir = "/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/hydrophobin_models/AF_structures/"

# Single category for Hydrophobin
category = {
    "name": "Hydrophobin",
    "pdb_dir": "classI-hydrophobin_filtered",
    "fasta_file": "classI_Hydrophobin_filtered_seqs.txt",
    "species_file": "classI_Hydrophobin_filtered_species_table.txt",
    "count_file": "classI_Hydrophobin_filtered_total_count.txt",
    "species_count": defaultdict(int),
    "seq_count": 0
}

# Ensure output directory exists
os.makedirs(category["pdb_dir"], exist_ok=True)

# Open output FASTA file
fasta_handle = open(category["fasta_file"], "w")

# Parse input FASTA
for record in SeqIO.parse("uniprotkb_fungal_hydrophobin_family_2024_11_16.fasta", "fasta"):
    desc = record.description
    seq = str(record.seq)

    # Filter: must mention Hydrophobin, length 110–250, and first Cys after position 80
    if (
        "Hydrophobin" in desc and
        70 <= len(seq) <= 250 and
        seq.find('C') > 70
    ):
        category["seq_count"] += 1
        fasta_handle.write(f">{record.id} {desc}\n{seq}\n")

        # Extract species name
        if "OS=" in desc:
            species = desc.split("OS=")[1].split(" ")[0]
        else:
            species = desc.split()[0]
        category["species_count"][species] += 1

        # Copy matching PDB to category's directory
        try:
            uniprot_id = record.id.split("|")[1] if "|" in record.id else record.id
            pdb_filename = f"AF-{uniprot_id}.pdb"
            pdb_src_path = os.path.join(pdb_source_dir, pdb_filename)
            pdb_dst_path = os.path.join(category["pdb_dir"], pdb_filename)

            if os.path.exists(pdb_src_path):
                shutil.copy(pdb_src_path, pdb_dst_path)
            else:
                print(f"Skipped: {pdb_filename} not found.")
        except IndexError:
            print(f"Could not parse UniProt ID from: {record.id}")

# Close FASTA file
fasta_handle.close()

# Write species table and total count
with open(category["species_file"], "w") as sf:
    sf.write("Species\tCount\n")
    for species, count in sorted(category["species_count"].items(), key=lambda x: x[1], reverse=True):
        sf.write(f"{species}\t{count}\n")

with open(category["count_file"], "w") as cf:
    cf.write(f"Total {category['name']} sequences: {category['seq_count']}\n")

