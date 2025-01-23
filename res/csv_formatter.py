import os
from pandas import read_csv

#Responsibility: Converts the CSV file generated from Numbers (.numbers file) into a formatted
#CSV file, that is suited for import into program.
basedir = os.path.dirname(__file__)
df = read_csv(os.path.join(basedir,"DSK_tiny.csv"), sep=";")
df.rename(columns={'Produkt': 'product', 'Total kg CO2e/kg': 'kg_co2e_pr_kg'}, inplace=True)
df['kg_co2e_pr_kg'] = df['kg_co2e_pr_kg'].str.replace(",",".")
df = df.astype({'product': str, 'kg_co2e_pr_kg': float})
df.index.name = "ID"
df.to_csv(os.path.join(basedir,"DSK_tiny_formatted.csv"))