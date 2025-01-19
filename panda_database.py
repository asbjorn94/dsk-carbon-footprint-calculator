import os
from pandas import read_csv

# basedir = os.getcwd()
basedir = os.path.dirname(__file__)
print("basedir: " + basedir)
full_path = os.path.join(basedir,"res/DSK_tiny.csv")    
print("full_path: " + full_path)
panda_db = read_csv(full_path, sep=";")


