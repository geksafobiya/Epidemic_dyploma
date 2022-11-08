import os
import pandas as pd


os.chdir("C:/Users/asja6/Documents/Projects/Epidemic_dyploma/data/")
file = "Ukraine.xlsx"
Ukraine = pd.ExcelFile(file)
print(Ukraine.sheet_names)