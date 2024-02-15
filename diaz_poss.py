#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 20:51:57 2023

@author: damianesene
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import numpy as np
import pylab as pl
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

url = 'https://fbref.com/en/comps/9/possession/Premier-League-Stats'
response = requests.get(url)

tables = pd.read_html(response.text, header=1)

# Get the tables within the Comments
soup = BeautifulSoup(response.text, 'html.parser')
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for each in comments:
    if 'table' in str(each):
        try:
            poss_stats = pd.read_html(str(each), header=1)[0]
            poss_stats = poss_stats[poss_stats['Rk'].ne('Rk')].reset_index(drop=True)
            poss_stats.append(poss_stats)
        except:
            continue

poss_stats["90s"] = pd.to_numeric(poss_stats["90s"])
#poss_stats["Age"] = pd.to_numeric(poss_stats["Age"])
poss_stats["Succ"] = pd.to_numeric(poss_stats["Succ"])
poss_stats["1/3"] = pd.to_numeric(poss_stats["1/3"])
poss_stats["Succ/90"] = poss_stats["Succ"]/poss_stats["90s"]
poss_stats["1/3/90"] = poss_stats["1/3"]/poss_stats["90s"]
poss_stats=poss_stats[(poss_stats["Squad"]=="Liverpool")]
#poss_stats["Squad"]=poss_stats["Squad"]=="Liverpool"

poss_stats = poss_stats[poss_stats["90s"] >=3]

a = poss_stats['Succ/90']
b = poss_stats['1/3/90']
d= poss_stats['Player']
plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#2B547E'

fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(a,b, color = "white")
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(a, b, color='red')

fig= plt.figure(1, figsize=(8, 14), frameon=False, dpi=100)
for x,y,z in zip(a,b,d):
    label = "{}".format(z)
    plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center')
plt.ylabel('Carries into Final third/90',color='white')
plt.xlabel('Succ Take-on/90',color='white')
plt.hlines(poss_stats['1/3/90'].mean(), poss_stats['Succ/90'].min(), poss_stats['Succ/90'].max(), color='#c2c1c0')
plt.vlines(poss_stats['Succ/90'].mean(), poss_stats['1/3/90'].min(), poss_stats['1/3/90'].max(), color='#c2c1c0')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

plt.text(0,2.6,'Comparing LFC Players \n based on Carries into final 1/3 per 90\n and Successful take-ons per 90', size=9.5, color='white')

fig.savefig('/Users/damianesene/Downloads/diaz_poss.jpg', dpi=300)
