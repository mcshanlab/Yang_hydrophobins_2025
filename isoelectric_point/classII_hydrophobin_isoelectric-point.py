from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import numpy as np
import pylab
import matplotlib.pyplot as plt
from tabulate import tabulate

# List to store the gravy scores in each sequence
isoelectric_counts = []

plt.figure(figsize=(3.5, 1.5))

# Grab sequences
for record in SeqIO.parse("uniprotkb_cerato_ulmin_hydrophobin_fami_2024_11_16.fasta", "fasta"):
    seq = str(record.seq)
    
    if 'X' in seq:
        print(f"Skipping sequence with ambiguous residue: {record.id}")
        continue
        
    X = ProteinAnalysis(seq)
    
    # Get the gravy score
    isoelectric_count = X.isoelectric_point()
    
    # Append the score to the list
    isoelectric_counts.append(isoelectric_count)
    
    sizes=isoelectric_counts
    
# Create the histogram
counts, bin_edges, _ = pylab.hist(sizes, bins=50)

# Title for the plot
pylab.hist(sizes, bins=50, edgecolor='black', color='#E88FBC')
pylab.title("%i Class II hydrophobins\nIsoelectric Point %i to %i" \
% (len(sizes),min(sizes),max(sizes)))
pylab.xlabel("Isoelectric Point")
pylab.ylabel("Count")
plt.xlim(3.5,11)
plt.rcParams['pdf.fonttype'] = 42
#plt.xticks(np.arange(int(min(bin_edges)) - 2, int(max(bin_edges)) +1, 1))
plt.savefig("classII_hydrophobin_isoelectricpoint_histogram.pdf", format="pdf", bbox_inches = "tight")
pylab.show()

# Print X and Y values (bin edges and counts)
#table = zip(bin_edges, counts)
#print(tabulate(table, headers=['bin_edges', 'counts']))
