import os
from pandas import read_csv

basedir = os.path.dirname(__file__)

def set_path(file_name):
    
    return os.path.join(basedir,("res/" + file_name))     

# dsk_path = os.path.join(basedir,"res/DSK_tiny_formatted.csv")    
dsk_path = set_path("DSK_tiny_formatted.csv")    
dsk_table = read_csv(dsk_path)

print(f"""
    panda_db['ID'].dtype: {dsk_table['ID'].dtype} \n 
    panda_db['kg_co2e_pr_kg'].dtype: {dsk_table['kg_co2e_pr_kg'].dtype} \n 
    panda_db['product'].dtype: {dsk_table['product'].dtype} \n 
    """)

# synonym_table_path = os.path.join(basedir,"res/synonym_table.csv") 
synonym_table_path = set_path("synonym_table.csv")  
synonym_table = read_csv(synonym_table_path)

print(f"""
    synonym_table['ID'].dtype: {synonym_table['ID'].dtype} \n 
    synonym_table['synonym'].dtype: {synonym_table['synonym'].dtype} \n 
    """)

# conversion_table_path = os.path.join(basedir,"res/synonym_table.csv") 
conversion_table_path = set_path("conversion_table.csv") 
conversion_table = read_csv(conversion_table_path)