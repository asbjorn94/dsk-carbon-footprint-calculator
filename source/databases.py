import os
import pandas as pd
#from pandas import read_csv
from dotenv import load_dotenv
from .dsk_item import DSKItem
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

load_dotenv(os.path.dirname(__file__) + '/.env')

host = os.getenv('dsk_mysql_host')
user = os.getenv('dsk_mysql_user')
password = os.getenv('dsk_mysql_pwd')
database = os.getenv('dsk_mysql_database')

engine = sa.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}") #mysql-connector-python needs to be installed for this to work
Session = sessionmaker(bind=engine)
metadata = sa.MetaData()

carbon_footprint_table = sa.Table(
    "carbon_footprint",
    metadata,
    autoload_with=engine
)

def fetch_table(table_name) -> pd.DataFrame:
    with engine.connect() as connection:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, connection)
    
def get_dsk_item_by_id(id: int) -> DSKItem:
    with Session() as session:
        query = sa.select(carbon_footprint_table).where(carbon_footprint_table.c.id == id)
        result = session.execute(query).fetchone()._mapping
        result = DSKItem(
            id = result.id,
            product = result.product,
            footprint = result.kg_co2e_pr_kg
        )
        
        return result

def insert_records_into_table(dataframe, table_name="conversion_table2"):
    with engine.connect() as connection:
        dataframe.to_sql(table_name, connection, if_exists="replace", index=False)

def insert_records_into_dsk_table_orig(dataframe, table_name="carbon_footprint_detailed"):
    with engine.connect() as connection:
        dataframe.to_sql(table_name, connection, if_exists="replace", index=False)

dsk_table = fetch_table("carbon_footprint")
synonym_table = fetch_table("synonym_table")
conversion_table = fetch_table("conversion_table")

# print(dsk_table.to_markdown())
# print(synonym_table.to_markdown())
# print(conversion_table.to_markdown())