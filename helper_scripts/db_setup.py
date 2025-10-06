import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from source import databases

basedir = os.path.dirname(__file__)

load_dotenv(os.path.join(basedir, "../.env"))

def setup_dsk_table_orig():

    xlsfile = pd.read_excel(basedir + "/res/DSK_v1.2.xlsx", sheet_name="DK")
    xlsfile = xlsfile[['ID_Ra','Produkt', 'Kategori','Total kg CO2e/kg', 'Landbrug', 'ILUC', 'Forarbejdning', 'Emballage','Transport', 'Detail']]
    
    #Trimming ids, i.e. 'Ra00001' becomes '1'
    xlsfile['ID_Ra'] = xlsfile['ID_Ra'].str.replace('Ra', '', case=False).str.lstrip('0')
    xlsfile['ID_Ra'] = xlsfile['ID_Ra'].astype(int)
    
    xlsfile = xlsfile.round(2)

    def replace_negative_zero(x):
        if isinstance(x, (int, float)) and str(x) == '-0.0':
            return 0.0
        return x
    xlsfile = xlsfile.map(replace_negative_zero)
    #Exclude ready-made meals
    xlsfile = xlsfile[~xlsfile['Kategori'].isin(["Færdigretter"])]
    
    databases.insert_records_into_dsk_table_orig(xlsfile)


def setup():
    setup_dsk_table_orig()

setup()

def old_setup(): #TODO: Needs to be delegated to databases.py
    db = mysql.connector.connect(
        host = os.getenv('dsk_mysql_host'),
        user = os.getenv('dsk_mysql_user'),
        password = os.getenv('dsk_mysql_pwd'),
        database = os.getenv('dsk_mysql_database')
    ) 

    my_cursor = db.cursor()

    # CREATION===============================================================
    # CARBON FOOTPRINTS
    # my_cursor.execute("CREATE TABLE carbon_footprint (id INT PRIMARY KEY, product VARCHAR(255), kg_co2e_pr_kg DOUBLE(5,2))")

    # # SYNONYM TABLE
    # create_table_query = """
    # CREATE TABLE IF NOT EXISTS synonym_table (
    #     product_id INT,
    #     product_name VARCHAR(255),
    #     FOREIGN KEY (product_id) REFERENCES carbon_footprint(id)
    # )
    # """
    # my_cursor.execute(create_table_query)

    # # CONVERSION TABLE
    # create_table_query = """
    # CREATE TABLE IF NOT EXISTS conversion_table (
    #     product_id INT,
    #     unit VARCHAR(255),
    #     kg_conversion_factor FLOAT,
    #     FOREIGN KEY (product_id) REFERENCES carbon_footprint(id)
    # )
    # """
    # my_cursor.execute(create_table_query)

    #INSERTION===============================================================

    #CARBON FOOTPRINTS
    # df = pd.read_csv('res/footprint_data_tiny.csv', sep = ";")
    df = pd.read_csv(os.path.join(basedir, 'res/footprint_data.csv'), sep = ";")
    df['total_carbon'] = df['total_carbon'].astype(str).str.replace(',', '.').astype(float)

    for index, row in df.iterrows():
        sql = "INSERT INTO carbon_footprint (id, product, kg_co2e_pr_kg) VALUES (%s, %s, %s)"
        values = (row['id'], row['product'], row['total_carbon'])
        my_cursor.execute(sql, values)

    # SYNONYM TABLE
    #df = pd.read_csv(os.path.join(basedir, 'res/synonym_table_tiny.csv'), sep = ";")
    df = pd.read_csv(os.path.join(basedir, 'res/synonym_table.csv'), sep = ";")
    for index, row in df.iterrows():
        sql = "INSERT INTO synonym_table (product_id, product_name) VALUES (%s, %s)"
        values = (row['product_id'], row['product_name'])
        my_cursor.execute(sql, values)

    # CONVERSION TABLE
    df = pd.read_csv(os.path.join(basedir, 'res/conversion_table_tiny.csv'), sep = ";")
    for index, row in df.iterrows():
        sql = "INSERT INTO conversion_table (product_id, unit, kg_conversion_factor) VALUES (%s, %s, %s)"
        values = (row['id'], row['unit'], row['kg_conversion_factor'])
        my_cursor.execute(sql, values)

    db.commit()
    my_cursor.close()
    db.close()



