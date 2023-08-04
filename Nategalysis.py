# -*- coding: utf-8 -*-
# Created by asmpro 
# 03/08/2023
# @asmprotk

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

start_id = 1664845
number_of_students = 100
response=requests.get(f'https://alnateega.com/api/student/{start_id}')
response = response.json()
idNum=response['data']['seat_number']
data = pd.DataFrame(response['data']['results'][0]['subjects']).transpose()
data['id'] = idNum
data = data.reset_index()
data.rename(columns={'index':'subject'},inplace=True)
data = data.set_index(['id','subject'])
data = data.drop(columns=['average','students_count'])
Grade = (data['grade'] / data['max'] ) * 100
data.insert(loc=0,column='Grade',value= Grade)
data = data.drop(columns=['grade','max','rank'])
data['Grade'] = data['Grade'].apply(lambda x: round(x, 2))
print('1 = Done!')
ide = start_id + 1
missed_ids=[]

for i in range(number_of_students-1):
    try:
        response=requests.get(f'https://alnateega.com/api/student/{ide}')
        response = response.json()
        idNum=response['data']['seat_number']
        data1 = pd.DataFrame(response['data']['results'][0]['subjects']).transpose()
        data1['id'] = idNum
        data1 = data1.reset_index()
        data1.rename(columns={'index':'subject'},inplace=True)
        data1 = data1.set_index(['id','subject'])
        data1 = data1.drop(columns=['average','students_count'])
        Grade = (data1['grade'] / data1['max'] ) * 100
        data1.insert(loc=0,column='Grade',value= Grade)
        data1 = data1.drop(columns=['grade','max','rank'])
        data1['Grade'] = data1['Grade'].apply(lambda x: round(x, 2))
        data = pd.concat([data,data1])
        ide += 1
        print(f'{i+2} = Done!')
    except: 
        missed_ids.append(ide) ; ide += 1
        
print(data)
group_data = data.groupby('subject')['Grade'].agg(np.mean)
print(group_data)
group_data.plot(kind='bar',color=['green','#FF5733', '#33FF57', '#5733FF', '#FF33A8', '#33A8FF', '#A8FF33', '#FF3333', '#33FF33', '#3333FF', '#FFFF33'])
plt.title('Mean of Subject Grades')
plt.ylabel('Mean Grades')
plt.show()
print(missed_ids)
data.to_csv('natega.csv')
