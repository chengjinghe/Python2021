import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np
import random
df = pd.read_excel(r"D:\np\np3.xlsx")
# s1 = df.iloc[999:1000]
# print(s1)
s2 = np.random.randint(0,50,size=20)
# plt.plot(s1,'o')
plt.plot(s2,'o')
plt.xlabel('x_Python')
plt.ylabel('y_Python')
plt.legend()
plt.show()
