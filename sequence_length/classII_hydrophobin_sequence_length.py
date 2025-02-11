from Bio import SeqIO
import numpy as np
import pylab
import matplotlib.pyplot as plt
from tabulate import tabulate

# Get the sequence lengths from the FASTA file
sizes = [len(rec) for rec in SeqIO.parse("uniprotkb_cerato_ulmin_hydrophobin_fami_2024_11_16.fasta", "fasta")]

# Calculate the mean and standard deviation
mean_length = np.mean(sizes)
std_dev_length = np.std(sizes)

# Print the average length plus or minus the standard deviation
print(f"Average sequence length: {mean_length:.2f} ± {std_dev_length:.2f}")

plt.figure(figsize=(3.5, 1.5))

# Create the histogram
counts, bin_edges, _ = pylab.hist(sizes, bins=200)

# Title for the plot with average and standard deviation
pylab.hist(sizes, bins=200, edgecolor='black', color='#E88FBC')
pylab.title("%i Class II hydrophobins\nLengths %i to %i\nAverage length: %.2f ± %.2f" \
% (len(sizes), min(sizes), max(sizes), mean_length, std_dev_length))
pylab.xlabel("Sequence length (amino acids)")
pylab.ylabel("Count")
plt.xlim(0,400)
plt.rcParams['pdf.fonttype'] = 42
plt.savefig("classII_hydrophobin_sequencelength_histogram.pdf", format="pdf", bbox_inches = "tight")
pylab.show()

# Print X and Y values (bin edges and counts)
# table = zip(bin_edges, counts)
# print(tabulate(table, headers=['bin_edges', 'counts']))
