awk 'NR == 1 {
    # Save the headers in an array
    for (i = 4; i <= 28; i++) {
        header[i] = $i
    }
    next
}
NR > 1 && ($2 ~ /2NBH_D8QCG9_structure_0001_0001.pdb/ && $4 ~ /58A/ && $7 ~ /63A/) {
    # For each matching row, print the values under their corresponding header
    for (i = 4; i <= 28; i++) {
        printf "%-20s: %-20s\n", header[i], $i
    }
    print ""  # Blank line to separate rows
}' energy_breakdown.sc
