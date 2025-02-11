'''
example python script to get a subset of csv file with entries without alphafold sturctures
'''


import pandas as pd


df = pd.read_csv('hydrophobin.csv')
df = df.loc[df['AlphaFold'].isnull()]
df.to_csv('hydrophobin_noAF.csv', index=False) #save these entries without alphafold structures as a csv