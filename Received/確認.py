#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import pulp

import pulp
class_df = pd.read_csv('class.csv')
teg_df = pd.read_csv('teg.csv')
S=teg_df['id'].tolist()
teggaku=teg_df['list'].tolist()
C=class_df['class2'].tolist()

flag=class_df['flag'].tolist()
SC = [(s,c) for s in S for c in C]

score = {row.id:row.list for row in teg_df.itertuples()}
seikyu=class_df['base'].tolist()
class_df
flag =class_df['flag'].tolist()
x = pulp.LpVariable.dicts('x', SC, cat='Binary')

prob = pulp.LpProblem('ClassAssignmentProblem', pulp.LpMaximize)

for s in S:
    prob += pulp.lpSum([x[s,c] for c in C]) <=1




status=0
while status==0:
    for c,z,f  in zip(C,seikyu,flag):
        if f == 'm':
            prob += pulp.lpSum(x[s,c] * score[s] for s in S) >= z 
            prob +=  z +10000 >= pulp.lpSum(x[s,c] * score[s] for s in S)
        elif z >= 500000:
            prob += pulp.lpSum(x[s,c] * score[s] for s in S) >= z-50000
            prob +=  z +50000 >= pulp.lpSum(x[s,c] * score[s] for s in S)
        else:
            prob += pulp.lpSum(x[s,c] * score[s] for s in S) >= z -10000
            prob +=  z +10000 >= pulp.lpSum(x[s,c] * score[s] for s in S)
    status = prob.solve(pulp.PULP_CBC_CMD(options=['maxsol 1'],timeLimit=60))
    print(status)
    print(pulp.LpStatus[status])


C2Ss = {}
for c in C:
    C2Ss[c] = [s for s in S if x[s,c].value()==1]
            
for c, Ss in C2Ss.items():
    print('Class:', c)
    print('Num:', len(Ss))
    print('teg:', Ss)
    print()

for s in S:
    # 割り当てられたクラスを取得
    assigned_class = [x[s,c].value() for c in C if x[s,c].value()==1]

    # 1つのクラスに割り当てられているか確認
    if len(assigned_class) != 1:
        print('error:', s, assigned_class)

result_df =teg_df.copy()
S2C = {s:c for s in S for c in C if x[s,c].value()==1}
result_df['asclass'] = result_df['id'].map(S2C)
result_df
s2d = {row.class2:row.base for row in class_df.itertuples()}
result_df['new'] = result_df['asclass'].map(s2d)
result_df
result_df.to_csv('out.csv')






# In[ ]:




