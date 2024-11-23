# -*- coding: utf-8 -*-
"""
Spyder Editor

Script for getting credit card transactions for Axis Card.

Provide - filename and password of the file

"""

import os
import sys
from names_password import *
print('Operating from Folder:')
print(os.getcwd())
print('************** /n')

import pandas as pd
import camelot
import datetime

st_pass = axis_pass
print('************** Getting FILENAME:')
st_filename = axis_name
name = ''.join(['in/',st_filename,'.pdf'])

print('************** READING TABLES:')
cashback = camelot.read_pdf(name,password=st_pass, flavor='stream', table_areas=['10,420,850,410'])[0].df
tables = camelot.read_pdf(name,password=st_pass, pages='1',flavor='stream', table_areas=['10,740,850,400'])[0].df

balance = camelot.read_pdf(name,password=st_pass, pages='1',flavor='stream', table_areas=['10,790,500,780'])[0].df

balance  = balance[[0,1,2,3,6]]
balance.columns = ['last_due','last_credit','last_cashback','debit','due']
balance= balance.map(lambda x: str.replace(str.replace(x,"Dr",""),",",""))
balance.map(lambda x: pd.to_numeric(x))
balance['credit'] =  pd.to_numeric(balance['last_credit'][0]) + pd.to_numeric(balance['last_cashback'][0])

print('READ BALANCE INFO')


transactions = pd.concat([tables])
transactions.columns = ['date','description','type','amt','cashback']
transactions = transactions.loc[transactions.date != '']
transactions['date'] = transactions['date'].apply(lambda x: datetime.datetime.strptime(x,'%d/%m/%Y'))
transactions['credit'] = transactions['amt'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if str.split(x," ")[1] == 'Cr' else 0)
transactions['debit'] = transactions['amt'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if str.split(x," ")[1] == 'Dr' else 0)
transactions['cb_credit'] = transactions['cashback'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if str.split(x," ")[1] == 'Cr' else 0)
transactions['cb_debit'] = transactions['cashback'].apply(lambda x: str.replace(str.split(x," ")[0],",","") if str.split(x," ")[1] == 'Dr' else 0)
transactions.drop(['amt','cashback'],axis = 1, inplace = True)
transactions['credit']= pd.to_numeric(transactions.credit)
transactions['debit']= pd.to_numeric(transactions.debit)
transactions['cb_credit']= pd.to_numeric(transactions.cb_credit)
transactions['cb_debit']= pd.to_numeric(transactions.cb_credit)

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

transactions['description']= transactions.description.map(lambda x: desc_dict.get(x,x))

print(transactions.description.value_counts())
print('----------------------------------------------')


tables2 = camelot.read_pdf(name,password=st_pass, pages='1',flavor='stream', table_areas=['10,850,850,840'])[0].df
tables2  = tables2[[0,3]]

print('************** STATEMENT DUE ON')
print(tables2[0][0])
print('************** AMOUNT DUE')
print(tables2[3][0])
print('----------------------------------------------')

a = str.replace(str.replace(str.replace('_'.join([tables2[3][0],tables2[0][0]]),'   Dr',''),',',''),'/','_')
transactions.to_csv(''.join(['out/',st_filename,'_ due_',a,'.csv']))
print('************** FILE SAVED, END OF PROGRAM')
print('----------------------------------------------')
