# written by andrew mcshan
# simple script to run rosetta calculations and scripts to filter results
# to run do ./idealize_relax_score_part1.sh

# idealize bonds to minimize xtal structure
# idealizing means bond lengths and angles will be their “ideal” state
idealize_jd2.static.macosclangrelease -s *.pdb

# remove idealized score file
rm score.sc

# relax side-chain rotamers to minimize xtal structure but keep overall structure roughly same
# relaxing means sampling most energetically favorable conformation in your protein
relax.static.macosclangrelease -s *_0001.pdb -ex1 -ex2

# summarize scores for all rosetta forcefield components
python3 extract_scores_part1.py

exit

# calculate per residue energy breakdown
residue_energy_breakdown.static.macosclangrelease -s *_0001_0001.pdb -out:file:silent energy_breakdown.sc

# extract and sort contributions only to the total score
awk '{print $4, $7, $28, $NF'} energy_breakdown.sc | sort -nk3 > sorted_energy_breakdown_totalscore.txt
