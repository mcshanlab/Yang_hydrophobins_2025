from Bio import SeqIO

# Read the FASTA file and collect sequences with their lengths
sequences = []
for rec in SeqIO.parse("uniprotkb_cerato_ulmin_hydrophobin_fami_2024_11_16.fasta", "fasta"):
    # Extract protein name from the description (after the UniProt accession number)
    description = rec.description.split(" ")[1:]  # Everything after the UniProt ID
    protein_name = " ".join(description)  # Join the words to form the full protein name
    
    sequences.append((protein_name, rec.id, len(rec), str(rec.seq)))

# Sort the sequences by length in descending order (longest first)
sequences_sorted = sorted(sequences, key=lambda x: x[2], reverse=True)

# Open the output file and write the sorted sequences
with open("class_II_longest-to-shortest.fasta", "w") as output_file:
    for protein_name, seq_id, seq_len, seq in sequences_sorted:
        output_file.write(f">{protein_name} | {seq_id} | Length: {seq_len}\n")
        output_file.write(f"{seq}\n")

print("Sorted sequences have been written to 'class_II_longest-to-shortest.fasta'")
