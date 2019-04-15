#!/usr/bin/env python
# coding: utf-8

# In[78]:


from bs4 import BeautifulSoup

import requests
import pandas as pd

import time;
ts = time.time()
ts = int(ts)
#print(ts)

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# In[102]:


endpoint = 'https://jobs.blognone.com/search'
company_endpoint = 'https://jobs.blognone.com/company/'
company_cover_endpoint = 'https://img.blognone.com/jobs/prod/730x365/cover/'
company_logo_endpoint = 'https://img.blognone.com/jobs/prod/118x118/logo/'


# In[96]:


def parse_data(content):
    soup = BeautifulSoup(content, 'html.parser')
    items = []
    for row in soup.select('a[href*="/company"]'):
        
        try:
            company_slug = row['href'].split("/")[2]
            company_url = company_endpoint + company_slug
            #company_cover = company_cover_endpoint + company_slug
            job_title = row.select('.css-12vb8u4 span')[0].text
            level = row.select('h4.text-muted')[0].text
            company_logo = row.select('img.img-fluid')[0].attrs['src']
            #company_logo = company_logo_endpoint + company_slug + ".jpg"
            company_logo_alt = row.select('img.img-fluid')[0].attrs['alt']
            company_name = company_logo_alt.replace('โลโก้บริษัท ', '')
            salary = row.select('span.text-success.css-1msjh1x span')
            salary_min = salary[1].text.replace(',', '')
            salary_max = salary[2].text.replace(',', '')
            location = row.select('span.text-muted')[0].text
            tags = [r.text for r in row.select('span.badge.mr-1.css-zf49go')]

            items.append({
                'job_title': job_title,
                'level':level ,
                'company_name': company_name,
                'company_slug': company_slug,
                'company_logo': company_logo,
                #'company_cover': company_cover,
                'company_url': company_url,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'location': location,
                'tags': ','.join(tags)
            })
            """
            print(job_title, level, company_name)
            print(salary_min, salary_max, location)
            print(','.join(tags))
            """
        except IndexError:
            continue
            
    return items


# In[106]:


all_items = []
for i in range(1, 50):
    #url = f"{endpoint}?page={i}"
    url = endpoint + "?page=" + str(i)
    print(url)
    r = requests.get(url)
    items = parse_data(r.content)
    if len(items) == 0:
        break
        
    all_items += items


# In[107]:


len(all_items)


# In[108]:


df = pd.DataFrame(all_items)


# In[113]:


df.info()


# In[112]:


df['company_name'] = pd.Categorical(df['company_name'])
df['salary_min'] = df['salary_min'].astype(int)
df['salary_max'] = df['salary_max'].astype(int)


# In[117]:


df.to_csv('data/data_'+str(ts)+'.csv')


# In[114]:


df.describe()


# In[116]:


df.head()


# In[115]:


df.sort_values('salary_max', ascending=False)


# In[124]:


df[df.tags.str.contains('python')].sort_values('salary_min', ascending=False)


# In[ ]:




