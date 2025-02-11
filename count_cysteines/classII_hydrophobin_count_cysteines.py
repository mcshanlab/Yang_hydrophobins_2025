from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import numpy as np
import pylab
import matplotlib.pyplot as plt
from tabulate import tabulate

# List to store the number of cysteines in each sequence
cysteine_counts = []

plt.figure(figsize=(3.5, 1.5))

# Grab sequences
for record in SeqIO.parse("uniprotkb_cerato_ulmin_hydrophobin_fami_2024_11_16.fasta", "fasta"):
    seq = str(record.seq)
    X = ProteinAnalysis(seq)
    
    # Count the number of cysteines ('C') in the sequence
    cysteine_count = X.count_amino_acids()['C']
    
    # Print sequence and its cysteine count (optional)
    #print(f"Sequence: {seq}")
    #print(f"Cysteine count: {cysteine_count}")
    
    # Append the cysteine count to the list
    cysteine_counts.append(cysteine_count)
    
    sizes=cysteine_counts
    
# Create the histogram
counts, bin_edges, _ = pylab.hist(sizes, bins=58)

# Title for the plot
pylab.hist(sizes, bins=58, edgecolor='black', color='#E88FBC')
pylab.title("%i Class II hydrophobins\nCysteine Counts %i to %i" \
% (len(sizes),min(sizes),max(sizes)))
pylab.xlabel("Number of cysteines")
pylab.ylabel("Count")
plt.xticks(np.arange(int(min(bin_edges)) - 4, int(max(bin_edges)) + 1, 2))
plt.xlim(0,20)
plt.rcParams['pdf.fonttype'] = 42
plt.savefig("classII_hydrophobin_cysteinecount_histogram.pdf", format="pdf", bbox_inches = "tight")
pylab.show()

# Print X and Y values (bin edges and counts)
#table = zip(bin_edges, counts)
#print(tabulate(table, headers=['bin_edges', 'counts']))
