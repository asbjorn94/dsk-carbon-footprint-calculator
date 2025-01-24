import os
import pandas as pd
from pandas import DataFrame
from typing import List
# from pandas import read_csv

from numbers_parser import Document

#Helper functions
def set_path(file_name):
    
    return os.path.join(basedir, file_name) 

def export_to_csv(table : DataFrame, file_location : str) -> None:
    
    table.to_csv(file_location, index=False)

#Responsibility: Converts the CSV file generated from Numbers (.numbers file) into a formatted
#CSV file, that is suited for import into program.
basedir = os.path.dirname(__file__)

print(f"basedir: {basedir}")    

# out_path = os.path.join(basedir,"temp_out")
# file_dest = os.path.join(out_path,"dsk_table.csv")

doc = Document(os.path.join(basedir, "databases_tiny.numbers"))

tables : list[DataFrame] = []

for sheet in doc.sheets:
    for table in sheet.tables:
        data = table.rows(values_only=True)
        # print(f"\ndata, type: {type(data)}\n")
        # print(f"data: {data}\n")
        pd_df = pd.DataFrame(data[1:], columns=data[0])
        tables.append(pd_df)


dsk_table = tables[0]
dsk_table = dsk_table.astype({'ID' : int}) #Somehow ID is not recognized as int...

synonym_table = tables[1]
synonym_table = synonym_table.astype({'ID' : int})

conversion_table = tables[2]
conversion_table = conversion_table.astype({'ID' : int})


print(f"dsk_table: {dsk_table.to_string(index = False)}")
print(f"synonym_table: {synonym_table.to_string(index = False)}")
print(f"conversion_table: {conversion_table.to_string(index = False)}")

export_to_csv(dsk_table, set_path("dsk_table.csv"))
export_to_csv(synonym_table, set_path("synonym_table.csv"))
export_to_csv(conversion_table, set_path("conversion_table.csv"))


    
    