#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, timedelta
import requests 
import pandas as pd
import numpy as np
import sys

from Scrapper import NIFTY50


# In[2]:


today=datetime.now()
if(today.isoweekday()!=1):
    date=datetime.strftime( today- timedelta(1), '%d%m%Y')
else:
    date=datetime.strftime( today- timedelta(3), '%d%m%Y')
date


# ## Download Volatility File

# In[3]:


nifty50=NIFTY50()


# In[4]:


print("Downloading volatility File for "+date)
r=requests.get("http://nseindia.com/archives/nsccl/volt/CMVOLT_"+date+".CSV", stream = True) 
with open("./data/yesterday.csv","wb") as file: 
    for chunk in r.iter_content(chunk_size=1024):
         if chunk: 
            file.write(chunk)


# In[5]:


# print("Downloading Nifty50 list")
# r=requests.get("https://www.nseindia.com/content/indices/ind_nifty50list.csv", stream = True) 
# with open("data/nifty50.csv","wb") as file: 
#     for chunk in r.iter_content(chunk_size=1024):
#          if chunk: 
#             file.write(chunk) 


# In[6]:


def strtofloat(x):
    if(x=="-"):
        return None
    s=x.split("-")
    #print(s)
    if(len(s)>1):
        return round(float(s[1])*(-100),2)
    else:
        return round(float(s[0])*(100),2)


# In[7]:


yesterday=pd.read_csv("data/yesterday.csv")
yesterday=yesterday.drop(["Date",
                          "Underlying Close Price (A)",
                          "Underlying Previous Day Close Price (B)",
                          "Underlying Log Returns (C) = LN(A/B)",
                          "Previous Day Underlying Volatility (D)"]
                         ,axis=1)
yesterday.columns=["Symbol","Daily%","Yearly%"]
yesterday['Daily%']=yesterday['Daily%'].apply(lambda x: strtofloat(x))
yesterday['Yearly%']=yesterday['Yearly%'].apply(lambda x: strtofloat(x))
yesterday=yesterday.loc[yesterday.Symbol.apply(lambda x: nifty50.nifty50check(x))]
yesterday.sort_values(["Daily%","Yearly%"], axis = 0, ascending = False,inplace = True, na_position ='last')
yesterday=yesterday.reset_index(drop=True)

yesterday#yesterday[yesterday['Daily%']>=2]


# In[8]:


final_data=pd.merge(yesterday,nifty50.get_nifty50table())


# In[9]:


balance=int(input("Enter current balance in account:"))


# In[ ]:





# In[10]:


final_data["MIS Max"]=final_data.apply(lambda x: balance*x["Margin"]//x["LTP"],axis=1)
final_data["CNC Max"]=final_data.apply(lambda x: balance//x["LTP"],axis=1)
print(final_data[final_data["Daily%"]>2])


# In[ ]:





# In[ ]:




