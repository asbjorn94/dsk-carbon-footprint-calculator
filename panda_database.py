import os
from pandas import read_csv

basedir = os.getcwd()
full_path = os.path.join(basedir,"res/DSK_tiny.csv")    
panda_db = read_csv(full_path, sep=";")


