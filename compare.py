import pandas as pd
import numpy as np

files =('paneltimeres_False_0.csv', 'paneltimeres_False_1.csv', 
        'paneltimeres_False_2.csv', 'paneltimeres_True_0.csv',
        'paneltimeres_True_1.csv', 'paneltimeres_True_2.csv')

res = []
for f in files:
    test = True
    try:
        a = pd.read_csv(f, delimiter=';')
    except:
        test = False
    if True:
        r = [f]
        for i in [1,2]:
            m = np.mean(a.iloc[:,i])
            s = np.std(a.iloc[:,i])
            r.extend([m,s])
        res.append(r)

print(np.array(res))
