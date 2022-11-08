import os
import pandas as pd
import matplotlib.pyplot as plt

os.chdir("C:/Users/asja6/Documents/Projects/Epidemic_dyploma/data/")
file = "Ukraine.xlsx"
#Ukraine = pd.ExcelFile(file).parse('Лист1')
Ukraine = pd.read_excel(file)
#print(Ukraine.sheet_names)

new_cases = []
days = []

new_cases = Ukraine.values[:, 5]
days = Ukraine.values[:, 3]
#new_cases.append(Ukraine['total_cases'])
#days.append(Ukraine['date'])
#print(days, new_cases)

#stringVal = "2020"
#list = [x for x in days if stringVal not in x]
#print(list)

#stringVal1 = "2021"
#list1 = [x for x in list if stringVal1 not in x]
days_filtered = []
new_cases_filtered = []
for i in range(1, len(days)):
    if "2021" not in days[i] and "2020" not in days[i]:
        if "-01-" in days[i]:
            days_filtered.append(days[i])
            new_cases_filtered.append(new_cases[i])

#print(len(new_cases_filtered), len(days_filtered))
plt.figure(figsize=(10, 10))
plt.plot(days_filtered, new_cases_filtered)
plt.show()
#pltData(days, new_cases)