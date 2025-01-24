import os
from pandas import read_csv

basedir = os.path.dirname(__file__)

dsk_path = os.path.join(basedir,"res/DSK_tiny_formatted.csv")    
panda_db = read_csv(dsk_path)

print(f"""
    panda_db['ID'].dtype: {panda_db['ID'].dtype} \n 
    panda_db['kg_co2e_pr_kg'].dtype: {panda_db['kg_co2e_pr_kg'].dtype} \n 
    panda_db['product'].dtype: {panda_db['product'].dtype} \n 
    """)

synonym_table_path = os.path.join(basedir,"res/synonym_table.csv") 
synonym_table = read_csv(synonym_table_path)

print(f"""
    synonym_table['ID'].dtype: {synonym_table['ID'].dtype} \n 
    synonym_table['synonym'].dtype: {synonym_table['synonym'].dtype} \n 
    """)