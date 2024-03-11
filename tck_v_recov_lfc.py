#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 22:34:20 2024

@author: damianesene
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import numpy as np
import pylab as pl
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

url = "https://fbref.com/en/comps/9/misc/Premier-League-Stats"

response = requests.get(url)

tables = pd.read_html(response.text, header=1)

# Get the tables within the Comments
soup = BeautifulSoup(response.text, 'html.parser')
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for each in comments:
    if 'table' in str(each):
        try:
            rec_tkl_tbl = pd.read_html(str(each), header=1)[0]
            rec_tkl_tbl = rec_tkl_tbl[rec_tkl_tbl['Rk'].ne('Rk')].reset_index(drop=True)
            rec_tkl_tbl.append(rec_tkl_tbl)
        except:
            continue


rec_tkl_tbl["90s"]= pd.to_numeric(rec_tkl_tbl["90s"])
rec_tkl_tbl["Recov"]= pd.to_numeric(rec_tkl_tbl["Recov"])
rec_tkl_tbl["TklW"]= pd.to_numeric(rec_tkl_tbl["TklW"])
rec_tkl_tbl["Born"]=pd.to_numeric(rec_tkl_tbl["Born"])
rec_tkl_tbl['Recov/90'] = rec_tkl_tbl["Recov"] / rec_tkl_tbl["90s"]
rec_tkl_tbl["TklW/90"] = rec_tkl_tbl["TklW"]/ rec_tkl_tbl["90s"]

rec_tkl_tbl = rec_tkl_tbl[(rec_tkl_tbl["Pos"] == "DF") | (rec_tkl_tbl["Pos"]== "DF,MF") ]

rec_tkl_tbl.loc[rec_tkl_tbl['Pos'] == 'DF,MF', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Diogo Dalot', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Tyrick Mitchell', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Levi Colwill', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Axel Disasi', 'Player'] = ''
rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Jonny Evans', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Nayef Aguerd', 'Player'] = ''
rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Kyle Walker', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Thiago Silva', 'Player'] = ''
rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Max Kilman', 'Player'] = ''

rec_tkl_tbl.loc[rec_tkl_tbl['Player'] == 'Antonee Robinson', 'Player'] = ''

rec_tkl_tbl = rec_tkl_tbl[rec_tkl_tbl["90s"]>=10]

#Assign plot colors to different leagues
conditions = [
    (rec_tkl_tbl['Squad'] == 'Liverpool')
]

colors = ['red']

rec_tkl_tbl['team_color'] = np.select(conditions, colors, default='white')

a = rec_tkl_tbl["TklW/90"]
b = rec_tkl_tbl["Recov/90"]
d= rec_tkl_tbl['Player']
e= rec_tkl_tbl['team_color']
plt.rcParams.update({'font.size': 25})
bgcol = 'black'

fig, ax = plt.subplots(figsize=(50, 28), dpi=400)
ax.scatter(a,b, color = e)
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(a, b, color= e, s=500)

fig= plt.figure(1, figsize=(40, 14), frameon=False, dpi=100)
for x,y,z in zip(a,b,d):
    label = "{}".format(z)
    plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,15), # distance from text to points (x,y)
                 ha='center', color="white")
    

plt.xticks(color="white")
plt.yticks(color="white")
#plt.text(0.3,9,"Recoveries and Tackles Won per 90 | PL 23/24 ", color="white", size=50)
#plt.text(0.3, 8.7, "Min. of 8 90s played", style="italic", color="white")
#plt.text(x, y, s, kwargs)
plt.ylabel('Recoveries per 90',color='white')
plt.xlabel('Tackles Won per 90',color='white')
plt.hlines(rec_tkl_tbl["Recov/90"].mean(),  rec_tkl_tbl["TklW/90"].min(),  rec_tkl_tbl["TklW/90"].max(), color='#c2c1c0')
plt.vlines( rec_tkl_tbl["TklW/90"].mean(), rec_tkl_tbl["Recov/90"].min(), rec_tkl_tbl["Recov/90"].max(), color='#c2c1c0')
	
#ax.scatter(1.53846,5.76923, color="red", s =200)

#ax.spines['top'].set_visible(False)
#ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8') 
ax.spines['bottom'].set_color('#ccc8c8')

fig.savefig('/Users/damianesene/Desktop/statsbomb/recov_tckl.jpg', dpi=300)