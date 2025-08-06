import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

basedir = os.path.dirname(__file__)

load_dotenv(os.path.join(basedir, "../.env"))

#TODO needs to establish connection using environment variables
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
