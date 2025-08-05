import os
import mysql.connector
import pandas as pd
#from pandas import read_csv
from dotenv import load_dotenv

load_dotenv()

# basedir = os.path.dirname(__file__)

# def set_path(file_name):
    
#     return os.path.join(basedir,("res/" + file_name))     

# Database connect
db = mysql.connector.connect(
    host = os.getenv('dsk_mysql_host'),
    user = os.getenv('dsk_mysql_user'),
    password = os.getenv('dsk_mysql_pwd'),
    database = os.getenv('dsk_mysql_database')
) 

cursor = db.cursor()

#Carbon_footprint
query = "SELECT * FROM carbon_footprint"  # Replace with your table name
cursor.execute(query)
rows = cursor.fetchall()
column_names = [i[0] for i in cursor.description]
dsk_table = pd.DataFrame(rows, columns=column_names)

#Synonyms TODO: REDUNDANT TO ABOVE
query = "SELECT * FROM synonym_table"  # Replace with your table name
cursor.execute(query)
rows = cursor.fetchall()
column_names = [i[0] for i in cursor.description]
synonym_table = pd.DataFrame(rows, columns=column_names)

#Synonyms TODO: REDUNDANT TO ABOVE
query = "SELECT * FROM conversion_table"  # Replace with your table name
cursor.execute(query)
rows = cursor.fetchall()
column_names = [i[0] for i in cursor.description]
conversion_table = pd.DataFrame(rows, columns=column_names)

cursor.close()
db.close()

#Prints of databases
print(dsk_table)
print(f"synonym_table: \n{synonym_table.to_string(index=False)}\n")
print(f"conversion_table: \n{conversion_table.to_string(index=False)}\n")


# Print the DataFrame
# print(df)



# dsk_path = set_path("dsk_table.csv")    
# dsk_table = read_csv(dsk_path)

# print(f"dsk_table: \n{dsk_table.to_string(index=False)}\n")

# # print(f"""
# #     panda_db['ID'].dtype: {dsk_table['ID'].dtype} \n 
# #     panda_db['kg_co2e_pr_kg'].dtype: {dsk_table['kg_co2e_pr_kg'].dtype} \n 
# #     panda_db['product'].dtype: {dsk_table['product'].dtype} \n 
# #     """)



# synonym_table_path = set_path("synonym_table.csv")  
# synonym_table = read_csv(synonym_table_path)

# print(f"synonym_table: \n{synonym_table.to_string(index=False)}\n")

# # print(f"""
# #     synonym_table['ID'].dtype: {synonym_table['ID'].dtype} \n 
# #     synonym_table['synonym'].dtype: {synonym_table['synonym'].dtype} \n 
# #     """)

# conversion_table_path = set_path("conversion_table.csv") 
# conversion_table = read_csv(conversion_table_path)

# print(f"conversion_table: \n{conversion_table.to_string(index=False)}\n")