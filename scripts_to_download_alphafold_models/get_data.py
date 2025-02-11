
'''
python script to get hydrophobin_uniprot.csv that gets all the data from uniprot

Run: python get_data.py
'''


import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
from Bio.PDB import alphafold_db, PDBList 
from pathlib import Path
import os
import wget
import shutil
import glob



# ---------- SETTINGS: Customize the fields to get from uniprot ------------:

# fields to get from uniprot
extrafields = ["accession", "id", "organism_name", "protein_name", "protein_families", "xref_pdb", "sequence"] #full list: https://www.uniprot.org/help/return_fields and https://www.uniprot.org/help/return_fields_databases


# maunally identified uniprotIDs (by searching PDB database) related to hydrophobin
#extraUniProtIDS = ["F8NJA2", "Q7S3P5", "D8QCG9", "K5VRK4", "R9A9N7", "Q04571", "D8QCG9", "F8NJA2", "D8QCG9", "B0Y4B1", "P39632" ]
# ---------- SETTINGS: Customize the fields to get from uniprot ------------:



#functions:

# function to get a dataframe from uniprot with all entries associated with hydrophobins
def get_hydrophobin_df(extrafields):

    #Query from UniProt using family fields
    '''
    url_fieldstring="&fields=" + ",".join(extrafields)
    url_query= ["cerato-ulmin%20hydrophobin%20family", "fungal%20hydrophobin%20family", "cerato-ulmin%20hydrophobin%20family+OR+fungal%20hydrophobin%20family", "cerato-ulmin%20hydrophobin%20family+AND+fungal%20hydrophobin%20family"]
    prefix = 'https://rest.uniprot.org/uniprotkb/search?&query=family:'
    suffix = f'{url_fieldstring}&format=tsv'
    urls = [prefix+q+suffix for q in url_query]
    

    for extra_uniprotID in extraUniProtIDS:
        url = f'https://rest.uniprot.org/uniprotkb/search?query=accession:{extra_uniprotID}' + suffix
        urls.append(url)

    '''
    #Query from UniProt using query directly
    url_fieldstring="fields=" + "%2C".join(extrafields)
    url_query= ["%28Fungal+hydrophobin+family%29", "%28Cerato-ulmin+hydrophobin+family%29"]
    prefix = 'https://rest.uniprot.org/uniprotkb/stream?'
    suffix = f'{url_fieldstring}&format=tsv'
    urls = [prefix+suffix+"&query="+q for q in url_query]
    

    filenames = []
    idx = 0
    for url in urls:
        with requests.get(url, stream=True) as request:
            request.raise_for_status()
            with open(f'out{idx}.tsv', 'wb') as f: 
                filenames.append(f'out{idx}.tsv')
                print(f'generating file: out{idx}.tsv')
                for chunk in request.iter_content(chunk_size=2**20):
                    f.write(chunk)
            idx += 1

    # Combine outputs as dataframe
    dfs = [pd.read_csv(fn, sep='\t') for fn in filenames]
    hydrophobin_df = pd.concat(dfs)
    hydrophobin_df.drop_duplicates(subset='Entry', keep="first", inplace=True)

    return hydrophobin_df







if __name__ == "__main__":
    
    # get a dataframe of hydrophobin from uniprot:
    print('start fetching from UniProt')
    hydrophobin_df = get_hydrophobin_df(extrafields)
    hydrophobin_df.to_csv('hydrophobin_uniprot.csv', index=False)
    print('finished running')    
    
    
    
    
  
