import pandas as pd
import numpy as np
import random,string

str1 = string.ascii_uppercase
comm = random.sample(str1,k=7)


for x in range(10):
    su = pd.Series(index=comm)
    a = np.random.randn(7)
    n = pd.Series(index=comm,data=a)
    su.append(n,ignore_index=True)
print(su)
