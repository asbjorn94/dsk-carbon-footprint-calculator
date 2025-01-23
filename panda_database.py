import os
from pandas import read_csv

basedir = os.path.dirname(__file__)
full_path = os.path.join(basedir,"res/DSK_tiny_formatted.csv")    
panda_db = read_csv(full_path)


