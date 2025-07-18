import os
import shutil
from Bio import SeqIO
from collections import defaultdict

# Configuration
pdb_source_dir = "/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/hydrophobin_models/AF_structures/"

# Output structure for both Tri and Penta
categories = {
    "Trihydrophobin": {
        "name": "Trihydrophobin",
        "pdb_dir": "classII-trihydrophobin",
        "fasta_file": "classII_Trihydrophobin_seqs.txt",
        "species_file": "classII_Trihydrophobin_species_table.txt",
        "count_file": "classII_Trihydrophobin_total_count.txt",
        "species_count": defaultdict(int),
        "seq_count": 0
    },
    "Pentahydrophobin": {
        "name": "Pentahydrophobin",
        "pdb_dir": "classII-pentahydrophobin",
        "fasta_file": "classII_Pentahydrophobin_seqs.txt",
        "species_file": "classII_Pentahydrophobin_species_table.txt",
        "count_file": "classII_Pentahydrophobin_total_count.txt",
        "species_count": defaultdict(int),
        "seq_count": 0
    }
}

# Ensure output directories exist
for cat in categories.values():
    os.makedirs(cat["pdb_dir"], exist_ok=True)

# Open FASTA output files
fasta_handles = {
    name: open(info["fasta_file"], "w")
    for name, info in categories.items()
}

# Parse input FASTA
for record in SeqIO.parse("uniprotkb_cerato_ulmin_hydrophobin_fami_2024_11_16.fasta", "fasta"):
    desc = record.description
    seq = str(record.seq)

    for cat_key, cat in categories.items():
        if cat_key in desc:
            cat["seq_count"] += 1
            fasta_handles[cat_key].write(f">{record.id} {desc}\n{seq}\n")

            # Extract species name
            if "OS=" in desc:
                species = desc.split("OS=")[1].split(" ")[0]
            else:
                species = desc.split()[0]
            cat["species_count"][species] += 1

            # Copy matching PDB to category's directory
            try:
                uniprot_id = record.id.split("|")[1] if "|" in record.id else record.id
                pdb_filename = f"AF-{uniprot_id}.pdb"
                pdb_src_path = os.path.join(pdb_source_dir, pdb_filename)
                pdb_dst_path = os.path.join(cat["pdb_dir"], pdb_filename)

                if os.path.exists(pdb_src_path):
                    shutil.copy(pdb_src_path, pdb_dst_path)
                else:
                    print(f"Skipped: {pdb_filename} not found.")
            except IndexError:
                print(f"Could not parse UniProt ID from: {record.id}")
            break  # Only match one category per record

# Close FASTA files
for fh in fasta_handles.values():
    fh.close()

# Write species tables and total counts
for cat in categories.values():
    with open(cat["species_file"], "w") as sf:
        sf.write("Species\tCount\n")
        for species, count in sorted(cat["species_count"].items(), key=lambda x: x[1], reverse=True):
            sf.write(f"{species}\t{count}\n")

    with open(cat["count_file"], "w") as cf:
        cf.write(f"Total {cat['name']} sequences: {cat['seq_count']}\n")
