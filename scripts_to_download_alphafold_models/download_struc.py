'''
python script to 
(1) integrate the alphafold IDs and save the dataframe as hydrophobin.csv
(2) download all structures

Run: python download_struc.py
'''


import pandas as pd
from Bio.PDB import alphafold_db, PDBList 
import glob
import os
import wget
from pathlib import Path





# get mapping filenames
def list_mapping():
    prefix = 'UNI2AF'
    return glob.glob(os.path.join("./", f"{prefix}*"))


# funciton to download all structures in the dataframe from PDB and alphafold
def download(hydrophobin_df):
    Path("./PDB_structures").mkdir(parents=True, exist_ok=True)
    Path("./AF_structures").mkdir(parents=True, exist_ok=True)
    
    for _, row in hydrophobin_df.iterrows():
        if isinstance(row['PDB'], str): 
            pdbIDs = row['PDB'].strip(";").split(";")
            #print(pdbIDs)
            for pdbID in pdbIDs:
                print(f'downloading the PDB structure: {pdbID}')
                fetchPDB(pdbID, database='PDB')
       

        if isinstance(row['AlphaFold'], str):
            afID = row['AlphaFold']
            print(f'downloading the alphafold structure: {afID}')
            fetchPDB(afID, database='AF')


# subfunction of download
def fetchPDB(id, database='PDB'):
    pdbl = PDBList()
    if database == 'PDB':
        fn_ent = pdbl.retrieve_pdb_file(pdb_code=id, pdir='./PDB_structures', file_format='pdb')
        os.rename(fn_ent, fn_ent.replace('pdb','').replace('ent','pdb'))

    elif database == 'AF':
        url = f'https://alphafold.ebi.ac.uk/files/{id}-model_v4.pdb'
        fn_af = wget.download(url, out='./AF_structures')
        os.rename(fn_af, fn_af.replace('-F1-model_v4',''))



if __name__ == "__main__":

    # read dataframe with uniprot information
    hydrophobin_df = pd.read_csv('./hydrophobin_uniprot.csv')

    # read mappings of UniProtIDs to AlphaFoldIDs
    mappings_filenames = list_mapping()
    mappings_list = []
    for fn in mappings_filenames:
        try:
            df = pd.read_csv(fn, sep='\t', header=None)
            mappings_list.append(df)
        except:
            continue
    
    mapping_all = pd.concat(mappings_list)
    #mapping_all.to_csv('test-mapping.csv')
    mapping_all.columns = ['Entry', 'AlphaFold']
    
    # map dataframe with alphafold IDs
    hydrophobin_df = hydrophobin_df.merge(mapping_all, on='Entry', how='left')

    # Save the dataframe as a csv file
    hydrophobin_df.to_csv('hydrophobin.csv', index=False)
    print('final csv file is saved as hydrophobin.csv')
    
    
    # download all structures from PDB or AlphaFold:
    print('start downloading pdb or cif structures')
    download(hydrophobin_df)
    
    #for p in glob.glob('./*.cif', recursive=True):
    #    shutil.move(p, './AF_structures')
    
    
