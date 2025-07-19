import pandas as pd

# Load the CSV file ; update the path
df = pd.read_csv('/Users/amcshan3/Desktop/Manuscripts/Russo_Hydrophobins_2024/Yang_hydrophobins_2025/tree_structures/sequence_tree/hydrophobin_extra.csv')

# Open a FASTA file to write
with open('hydrophobin_extra_trimmedCys.fasta', 'w') as fasta_file:
    for _, row in df.iterrows():
        title = row['Entry']
        sequence = row['Sequence']

        # Find indices of all Cys residues
        cys_positions = [i for i, aa in enumerate(sequence) if aa == 'C']

        # Proceed only if there are at least two cysteines
        if len(cys_positions) >= 2:
            trimmed_sequence = sequence[cys_positions[0]:cys_positions[-1]+1]
            fasta_file.write(f">{title}\n{trimmed_sequence}\n")
        else:
            print(f"Skipped {title} (fewer than 2 Cys residues)")
