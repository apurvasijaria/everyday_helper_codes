import glob
import pandas as pd
import re

curr_st = glob.glob('out/*due*.csv')

print(curr_st)

account = {
 'hdfc':'HDFC Credit Card',
 'amz':'ICICI Credit Card',
 'axis':'Axis Credit Card',
 'sap': 'ICICI Sapphiro Mastercard',
 'hdfc2': 'HDFC Rupay Card',
 'sbi': 'SBI Credit Card'            
}

st1 = pd.read_csv(curr_st[0])
st1 = st1[['date','description','debit','credit']]
st1['account'] = account[curr_st[0].split("_")[1]]
for i in range(1,len(curr_st)):
    st = pd.read_csv(curr_st[i])
    st = st[['date','description','debit','credit']]
    st['account'] = account[curr_st[i].split("_")[1]]
    st1 = pd.concat([st,st1])


category_desc = {'IND*AMAZON HTTP://WWW.AM IN': 'Shopping'
             ,'CLICK TO PAY PAYMENT RECEIVED': 'AcctTrnsfer'
             ,'IND*AMAZON.IN - GROCER': 'Grocery'
             ,'AMAZON INDIA CYBS SI MUMBAI IN':  'Books',
            'BLINKIT': 'Grocery',
             'BOOKMYSHOW COM':'Hanging out',
             'CHANGS': 'Eating out',
             'FLIGHT' :'Trips',
             'LOUNGE':'Trips',
             'FLIPKART':'Shopping',
             'GYFTR':'Shopping',
             'HENNES N MAURITZ      ':'Clothes',
             'HOTEL':'Trips',
             'RETAIL':'Shopping',
             'IRCTC':'Trips',
             'LIC' : 'Policy Payment',
             'NETBANKING TRANSFER':'AcctTrnsfer',
             'Coffee':'Hanging Out',
             'URBANCLAP':'Grooming',
             'VELLORE INSTITUTE OF':'Family',
             'ZARA INDITEX TRENT':'Clothes'}

st1.index = range(len(st1.index))
st1['expense_category'] = st1['description'].apply(lambda x: ''.join([(category_desc[y[0]] if y != None else ' ') for y in [re.search(regex, x) for regex in category_desc.keys()]]))
st1.to_csv("Combine.csv")
