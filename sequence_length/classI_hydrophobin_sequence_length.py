from Bio import SeqIO
import numpy as np
import pylab
import matplotlib.pyplot as plt
from tabulate import tabulate

# Get the sequence lengths from the FASTA file
sizes = [len(rec) for rec in SeqIO.parse("uniprotkb_fungal_hydrophobin_family_2024_11_16.fasta", "fasta")]

# Calculate the average length and standard deviation
mean_length = np.mean(sizes)
std_dev = np.std(sizes)

# Print out the average length and standard deviation
print(f"Average sequence length: {mean_length:.2f} ± {std_dev:.2f}")

plt.figure(figsize=(3.5, 1.5))

# Create the histogram
counts, bin_edges, _ = pylab.hist(sizes, bins=600)

# Title for the plot
pylab.hist(sizes, bins=600, edgecolor='black', color='#7CD3F7')
pylab.title("%i Class I hydrophobins\nLengths %i to %i" \
% (len(sizes), min(sizes), max(sizes)))
pylab.xlabel("Sequence length (amino acids)")
pylab.ylabel("Count")
plt.xlim(0, 400)
plt.rcParams['pdf.fonttype'] = 42
plt.savefig("classI_hydrophobin_sequencelength_histogram.pdf", format="pdf", bbox_inches="tight")
pylab.show()
