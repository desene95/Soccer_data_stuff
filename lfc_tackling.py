#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:24:33 2023

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

url = "https://fbref.com/en/comps/9/defense/Premier-League-Stats"
response = requests.get(url)
tables = pd.read_html(response.text, header=1)
tables = tables[0]

tables["90s"] = pd.to_numeric(tables["90s"])
tables['Att/90'] = tables['Att'] / tables['90s']
tables['Lost/90'] = tables['Lost'] / tables['90s']

a = tables['Att/90']
b= tables['Tkl%']
c= tables['Squad']

plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#2B547E'


fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(a,b, color = "white")
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(a, b, color='yellow')
ax.scatter(20.2727,39.5, color="red")
fig= plt.figure(1, figsize=(8, 14), frameon=False, dpi=100)
for x,y,z in zip(a,b,c):
    label = "{}".format(z)
    plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center')
plt.ylabel('Tackles won %',color='white')
plt.xlabel('Tackles Attempted/90',color='white')
#plt.grid(linestyle = '--', alpha=0.3)

plt.hlines(tables['Tkl%'].mean(), tables['Att/90'].min(), tables['Att/90'].max(), color='#c2c1c0')
plt.vlines(tables['Att/90'].mean(), tables['Tkl%'].min(), tables['Tkl%'].max(), color='#c2c1c0')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

plt.text(11,60, "How are PL Teams Tackling this Season", color="white", size=15)
#plt.Rectangle([14,55],10,5)

fig.savefig('/Users/damianesene/Downloads/pl_tackling.jpg', dpi=300)

#prog_tbl["Prog"] = pd.to_numeric(prog_tbl["Prog"])
#prog_tbl["Prog/90"] = prog_tbl["Prog"]/prog_tbl["90s"]