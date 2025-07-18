from Bio import SeqIO
import numpy as np
import matplotlib.pyplot as plt
import pylab

# Initialize lists
sizes = []
pre_c_lengths = []

# Parse the FASTA file and collect filtered data
for rec in SeqIO.parse("uniprotkb_fungal_hydrophobin_family_2024_11_16.fasta", "fasta"):
    seq = str(rec.seq)
    if len(seq) < 250:
        sizes.append(len(seq))
        first_c_index = seq.find("C")
        if first_c_index != -1:
            pre_c_lengths.append(first_c_index)

# Separate based on threshold of 50 residues
pre_c_under_50 = [x for x in pre_c_lengths if x < 70]
pre_c_50_or_more = [x for x in pre_c_lengths if x >= 70]

# Print summary stats
mean_length = np.mean(sizes)
std_dev = np.std(sizes)
print(f"Average sequence length (<250 aa): {mean_length:.2f} ± {std_dev:.2f}")
print(f"Number of sequences with C: {len(pre_c_lengths)}")
print(f"  <50 residues before C: {len(pre_c_under_50)}")
print(f"  ≥50 residues before C: {len(pre_c_50_or_more)}")

# Plot: Histogram of sequence lengths < 250
plt.figure(figsize=(3.5, 1.5))
plt.hist(sizes, bins=100, edgecolor='black', color='#7CD3F7')
plt.title(f"{len(sizes)} Class I hydrophobins <250 aa")
plt.xlabel("Sequence length (amino acids)")
plt.ylabel("Count")
plt.xlim(0, 250)
plt.savefig("classI_hydrophobin_length_lt250.pdf", format="pdf", bbox_inches="tight")
plt.show()

# Plot: Overlaid histograms of residues before first C
plt.figure(figsize=(3.5, 1.5))
bins = range(0, max(pre_c_lengths) + 5, 5)

plt.hist(pre_c_under_50, bins=bins, edgecolor='black', color='#77DD77', alpha=0.8, label='<70 residues before first C')
plt.hist(pre_c_50_or_more, bins=bins, edgecolor='black', color='#FF6961', alpha=0.8, label='≥70 residues before first C')

plt.title("Amino acids before first C")
plt.xlabel("Residues before first C")
plt.ylabel("Count")
plt.legend()
plt.savefig("classI_hydrophobin_preC_split_histogram.pdf", format="pdf", bbox_inches="tight")
plt.show()
