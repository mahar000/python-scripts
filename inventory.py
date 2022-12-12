import re
pattern = r'(va2[a-z]+crm[0-9]+)'
p=re.compile(pattern)
import pandas as pd
import numpy as np

#print(dir(pd))
df = pd.read_excel('example.xlsx')

df1 = df.replace(np.nan, '', regex=True)
#print(df1.head())
df3=df[df1['Hostname'].str.contains(p)]

df4=df3[['Hostname',  'Mgmt Access']]
#df4=df3[['Mgmt Access']]
df4['Mgmt Access'] = 'ansible_host=' + df4['Mgmt Access']
df5=df4.to_string(index=False)
#print(df4.to_string(index=False))
print(df5)

