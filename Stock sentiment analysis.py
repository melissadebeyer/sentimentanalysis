#!/usr/bin/env python
# coding: utf-8

# In[29]:


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# NLTK VADER for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.express as px



finwiz_url = 'https://finviz.com/quote.ashx?t='


# In[30]:


stocks=['AAPL','ING']


# In[31]:


news_tables = {}

for stock in stocks:
    url = finwiz_url + stock
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
    response = urlopen(req)    
    html = BeautifulSoup(response)
    news_table = html.find(id='news-table')
    news_tables[stock] = news_table


# In[32]:


parsed_news = []

for file_name, news_table in news_tables.items():
    # Iterate through all tr tags in 'news_table'
    for x in news_table.findAll('tr'):
        text = x.a.get_text() 
        date_scrape = x.td.text.split()

        if len(date_scrape) == 1:
            time = date_scrape[0]
            
        else:
            date = date_scrape[0]
            time = date_scrape[1]
       
        ticker = file_name.split('_')[0]
        
        parsed_news.append([ticker, date, time, text])


# In[33]:


vader = SentimentIntensityAnalyzer()

columns = ['ticker', 'date', 'time', 'headline']

parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)

scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()

scores_df = pd.DataFrame(scores)

parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')

parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date


# In[34]:


plt.rcParams['figure.figsize'] = [30, 6]

mean_scores = parsed_and_scored_news.groupby(['ticker','date']).mean()
mean_scores = mean_scores.unstack()
mean_scores = mean_scores.xs('compound', axis="columns").transpose()
mean_scores.plot(kind = 'bar')
plt.grid()


# In[35]:


mean_scores


# In[28]:


mean_scores.tail()


# In[36]:


mean_scores.to_excel('Stock sentiment output.xlsx', engine='xlsxwriter')  


# In[ ]:




