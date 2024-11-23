 # -*- coding: utf-8 -*-
"""
Spyder Editor

Script for getting credit card transactions for HDFC DCB Card.

Provide - filename and password of the file

"""

import os
import sys
from names_password import *
print('Operating from Folder:')
print(os.getcwd())
print('************** /n')

st_pass = hdfc_pass
print('************** getting FILENAME:')
st_filename = '1'
print(''.join(["reading: ",'in/',st_filename,'.pdf']))
name = ''.join(['in/',st_filename,'.PDF'])


import pandas as pd
import camelot
import datetime
import PyPDF2
import re 

reader = PyPDF2.PdfReader(name)
reader.decrypt(st_pass)
numpg = reader.numPages


print('************** READING TABLES:')
tables = camelot.read_pdf(name,password=st_pass, flavor='stream', table_areas=['10,420,850,160'])[0].df


for i in range(1,reader.numPages):
    print(i)
    page = reader.getPage(i)
    output = page.extractText()
    output = str(output)[0:8]
    
    if output == 'Domestic':
        tables2 = camelot.read_pdf(name,password=st_pass, pages=str(i+1),flavor='stream', table_areas=['10,790,850,300'])[0].df
        tables = pd.concat([tables,tables2])
    if output == 'Rewards ':
        rewards = camelot.read_pdf(name,password=st_pass, pages= str(i+1),flavor='stream', table_areas=['100,800,850,700'])[0].df
    if output == 'Internat':
        tables3 = camelot.read_pdf(name,password=st_pass, pages=str(i+1),flavor='stream', table_areas=['10,790,850,300'])[0].df
        tables3 = tables3[[1,2,3,4]]
        tables3.columns = [0,1,2,3]
        tables3[[2]] =0 
        tables = pd.concat([tables,tables3])
        
 
      
    
balance = camelot.read_pdf(name,password=st_pass, flavor='stream', table_areas=['150,680,850,640'])[0].df
balance.columns = ['d','credit','debit','d1','due']
balance.drop(['d','d1'],axis = 1, inplace = True)
balance['credit'] = balance['credit'].apply(lambda x: str.replace(str.replace(x,",",""),"`",""))
balance['debit'] = balance['debit'].apply(lambda x: str.replace(str.replace(x,",",""),"`",""))


print('READ BALANCE INFO')


transactions = tables
transactions.columns = ['date','description','points','amt']
transactions['date'] = transactions['date'].apply(lambda x: str.split(x,' ')[0] if len(x) > 10 else x)
transactions['date'] = transactions['date'].apply(lambda x: datetime.datetime.strptime(x,'%d/%m/%Y'))

transactions['credit'] = transactions['amt'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if len(str.split(x," ")) == 2 else 0)
transactions['debit'] = transactions['amt'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if len(str.split(x," ")) == 1 else 0)
transactions.drop('amt',axis = 1, inplace = True)
transactions['credit']= pd.to_numeric(transactions.credit)
transactions['debit']= pd.to_numeric(transactions.debit)
transactions['points'] = transactions['points'].apply(lambda x: str.replace(str(x)," ",""))
transactions['points']= pd.to_numeric(transactions.points)

rewards2 = transactions[(transactions.points.notna())]
reward_multi = {'IRCTC VIA SMARTBUY':3,
                'GYFTR VIA SMARTBUY':3,
                'SB GI FLIGHT':5,
                'GOIBIBO FLIGHT VIA SMAR':5                
               }

reward_multi_compiled=[re.compile(""+i+"") for i in list(reward_multi.keys())]
#[re.match(regex, rewards2.description[1]) for regex in reward_multi_compiled]
#max([(reward_multi[x[0]] if x != None else 1) for x in [re.match(regex, rewards2.description[1]) for regex in reward_multi_compiled]])

rewards2.index = range(len(rewards2.index))
rewards2['multiplier'] = rewards2['description'].apply(lambda x: max([(reward_multi[y[0]] if y != None else 1) for y in [re.match(regex, x) for regex in reward_multi_compiled]]))
rewards2['bonus_points'] = (rewards2.multiplier - 1)*rewards2.points
rewards2['year']= rewards2.date.map(lambda x: x.year)
rewards2['month']= rewards2.date.map(lambda x: x.month)
rewards2['rev']= rewards2.bonus_points.map(lambda x: 1 if x < 0 else 0)
rewards_comb = pd.pivot_table(rewards2, values =['bonus_points','points'], index =['rev','month','multiplier'], aggfunc = np.sum) 

print('READ TRANSACTION INFO')

print('************** CHECKING IF TRANSACTION AND BALANCE ARE ALINGED')
##check records capture rate
a1 = int(transactions.credit.sum() - pd.to_numeric(balance.credit[0]))
b1 = int(transactions.debit.sum() - pd.to_numeric(balance.debit[0]))

s = a1 + b1


if s != 0:
    print('MISMATCH FOUND PLEASE CHECK THE STATEMENT')
    print('Recorded, Actual, Difference')
    print(transactions.credit.sum(),pd.to_numeric(balance.credit[0]),a1)
    print(transactions.debit.sum(), pd.to_numeric(balance.debit[0]),b1)
    
    #sys.exit()
else:
    print('ALL TRANSACTIONS CAPTURED')

print('----------------------------------------------')
print('************** REFORMATTING DESCRIPTIONS')
# print(transactions.description.value_counts())

print(transactions.description.value_counts())
print('----------------------------------------------')


tables2 =  camelot.read_pdf(name,password=st_pass, flavor='stream', table_areas=['150,790,800,770'])[0].df
print('************** STATEMENT DUE ON')
print(tables2[0][0])
print('************** AMOUNT DUE')
print(tables2[1][0])
print('----------------------------------------------')

a = str.replace(str.replace(str.replace('_'.join([tables2[0][0],tables2[1][0]]),' ','_'),',',''),'/','_')
transactions.to_csv(''.join(['out/',st_filename,'_ due_',a,'.csv']))
rewards_comb.to_csv(''.join(['out/',st_filename,'_rewards.csv']))
print('************** FILE SAVED, END OF PROGRAM')
print('----------------------------------------------')
