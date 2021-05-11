import pandas as pd
import matplotlib.pyplot as plt


img = pd.read_excel(r"D:\DevOps\Python\Pandas\GOV_DATA\1-20.xlsx")
print(img.applymap())