import os
import mysql.connector
import pandas as pd
#from pandas import read_csv
from dotenv import load_dotenv
import sqlalchemy as sa

load_dotenv()

host = os.getenv('dsk_mysql_host')
user = os.getenv('dsk_mysql_user')
password = os.getenv('dsk_mysql_pwd')
database = os.getenv('dsk_mysql_database')

engine = sa.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

def fetch_table(table_name) -> pd.DataFrame:
    with engine.connect() as connection:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, connection)

def insert_records_into_table(dataframe, table_name="conversion_table2"):
    with engine.connect() as connection:
        dataframe.to_sql(table_name, connection, if_exists="replace", index=False)

dsk_table = fetch_table("carbon_footprint")
synonym_table = fetch_table("synonym_table")
conversion_table = fetch_table("conversion_table")

# print(dsk_table.to_markdown())
# print(synonym_table.to_markdown())
# print(conversion_table.to_markdown())