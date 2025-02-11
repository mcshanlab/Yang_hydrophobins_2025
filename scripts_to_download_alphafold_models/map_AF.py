
'''
python script to get mappings from uniprotID to AF ID from hydrophobin_uniprot.csv 

Run: python map_AF.py
Submit: source submit_map_AF.sh
'''

import pandas as pd
from Bio.PDB import alphafold_db, PDBList 
import argparse





# function to get alphafold ID for each uniprot ID
def mappingAF(uniprotID):
    try:
        out = alphafold_db.get_predictions(uniprotID)
        for o in out:
            af_ID = o['entryId']  
        return af_ID 
    
    except Exception as e:
        #print(e)
        return None #, None





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start', help='Start Index', required=True)
    parser.add_argument('-e','--end', help='End Index', required=True)
    args = parser.parse_args()

    STARTIDX = args.start
    ENDIDX = args.end
    print(f'running on the subset: {STARTIDX} to {ENDIDX}')
    hydrophobin_df = pd.read_csv('hydrophobin_uniprot.csv')
    if ENDIDX == "end":
        uniprotIDs = hydrophobin_df['Entry'].to_list()[int(STARTIDX):]
    else:
        uniprotIDs = hydrophobin_df['Entry'].to_list()[int(STARTIDX):int(ENDIDX)]

    
    

    with open(f"UNI2AF_{STARTIDX}.txt", "w") as f:
        
        for uniID in uniprotIDs:
            print(f'fetching: {uniID}')
            afID = mappingAF(uniID)
            
            if afID is not None:
                f.write(uniID + "\t" + afID)
                f.write("\n")
                print(afID)
    
    


    
