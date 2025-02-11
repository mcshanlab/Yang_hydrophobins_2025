
1. Activate the conda environment

2. run get_data.py to get the uniprot information
`python get_data`

3. get a mapping of uniprotID to alphafoldID
`source submit_map_AF.sh` (this will submit slurm scripts to run map_AF.py)

4. map the alphafoldID to the uniprot dataset to get a csv file, and download all structures
`python download_struc.py`

5. example script to get the entries without alphafold models: `python example.py` (this will produce the file hydrophobin_noAF.csv)