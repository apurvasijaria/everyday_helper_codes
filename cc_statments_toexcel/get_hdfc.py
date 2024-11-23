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
st_filename = hdfc_name
print(''.join(["reading: ",'in/',st_filename,'.pdf']))
name = ''.join(['in/',st_filename,'.pdf'])


import pandas as pd
import camelot
import datetime

print('************** READING TABLES:')
tables = camelot.read_pdf(name,password=st_pass, flavor='stream', table_areas=['10,420,850,160'])[0].df
tables2 = camelot.read_pdf(name,password=st_pass, pages='2',flavor='stream', table_areas=['10,790,850,300'])[0].df
rewards = camelot.read_pdf(name,password=st_pass, pages='3',flavor='stream', table_areas=['100,800,850,700'])[0].df
balance = camelot.read_pdf(name,password=st_pass, flavor='stream', table_areas=['150,680,850,640'])[0].df

balance.columns = ['d','credit','debit','d1','due']
balance.drop(['d','d1'],axis = 1, inplace = True)
balance['credit'] = balance['credit'].apply(lambda x: str.replace(str.replace(x,",",""),"`",""))
balance['debit'] = balance['debit'].apply(lambda x: str.replace(str.replace(x,",",""),"`",""))

print('READ BALANCE INFO')


transactions = pd.concat([tables,tables2])
transactions.columns = ['date','description','points','amt']
transactions['date'] = transactions['date'].apply(lambda x: str.split(x,' ')[0] if len(x) > 10 else x)
transactions['date'] = transactions['date'].apply(lambda x: datetime.datetime.strptime(x,'%d/%m/%Y'))

transactions['credit'] = transactions['amt'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if len(str.split(x," ")) == 2 else 0)
transactions['debit'] = transactions['amt'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if len(str.split(x," ")) == 1 else 0)
transactions.drop('amt',axis = 1, inplace = True)
transactions['credit']= pd.to_numeric(transactions.credit)
transactions['debit']= pd.to_numeric(transactions.debit)

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

desc_dict = {'IND*AMAZON HTTP://WWW.AM IN': 'Shopping'
             ,'CLICK TO PAY PAYMENT RECEIVED': 'CC_payment'
             ,'IND*AMAZON.IN - GROCER': 'grocery'
             ,'AMAZON INDIA CYBS SI MUMBAI IN':  'audible' }

transactions.description = transactions.description.apply(lambda x: ' '.join(str.split(x," ")[:-1]))
transactions['description']= transactions.description.map(lambda x: desc_dict.get(x,x))

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
print('************** FILE SAVED, END OF PROGRAM')
print('----------------------------------------------')
