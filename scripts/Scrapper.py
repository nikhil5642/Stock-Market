#!/usr/bin/env python
# coding: utf-8

# In[1]:


#from selenium import webdriver
import pandas as pd
import re
from tqdm import tqdm
import time
import requests


# In[2]:


margins=pd.read_csv("data/zerodhamargin.csv")
margins["Stocks allowed for MIS"]=margins["Stocks allowed for MIS"].apply(lambda x: x[:-3])
margins["Margin allowed"]=margins["Margin allowed"].apply(lambda x: float(x[:-1]))
margins.head()


# In[3]:


def get_margin(symbol):
    data=list(margins.loc[margins["Stocks allowed for MIS"]==symbol,"Margin allowed"])
    if(len(data)>0):
        return data[0]
    else:
        return 1.0


# In[4]:


#using selenium
# class NIFTY50:
#     def __init__(self):
#         print("Loading Browser...")
#         self.driver=self.loaddriver()
        
#     def loaddriver(self):
#         driver=webdriver.Firefox()
#         driver.get("https://www.nse-india.com/live_market/dynaContent/live_watch/equities_stock_watch.htm")
#         time.sleep(3)
#         return driver
#     def get_nifty50table(self):
#         try:
#             _ = self.driver.window_handles
#         except:
#             print("Restarting closed browser ...")
#             self.driver=self.loaddriver()
#         table=[]
#         for x in tqdm(self.driver.find_elements_by_xpath('//tr')[3:]):
#             data=re.split(' |\n',x.text)
#             table.append([data[0].strip(),float("".join(data[4].split(","))),float(data[6]),get_margin(data[0].strip())])
#         table=pd.DataFrame(table,columns=["Symbol","LTP","% Change","Margin"])
#         return table


# In[5]:


class NIFTY50:
    def __init__(self):
        self.nifty50=list(pd.read_csv("data/nifty50.csv")['Symbol'])
    def get_nifty50table(self):
        table=[]
        for data in requests.get("https://www.nse-india.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json").json()["data"]:
            table.append([data["symbol"],float("".join(data["ltP"].split(","))),float(data["per"]),get_margin(data["symbol"])])
        table=pd.DataFrame(table,columns=["Symbol","LTP","% Change","Margin"])
        return table
    
    def nifty50check(self,symbol):
        if symbol in self.nifty50:
            return True
        return False


# In[6]:


# nifty50=NIFTY50()
# print(nifty50.nifty50check("ABB"))
# nifty50.get_nifty50table()


# In[7]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




