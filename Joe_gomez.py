#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 20:29:33 2024

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


url="https://fbref.com/en/comps/9/misc/Premier-League-Stats"
response = requests.get(url)

tables = pd.read_html(response.text, header=1)

# Get the tables within the Comments
soup = BeautifulSoup(response.text, 'html.parser')
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for each in comments:
    if 'table' in str(each):
        try:
            def_tbl = pd.read_html(str(each), header=1)[0]
            def_tbl = def_tbl[def_tbl['Rk'].ne('Rk')].reset_index(drop=True)
            def_tbl.append(def_tbl)
        except:
            continue
        
def_tbl["90s"]= pd.to_numeric(def_tbl["90s"])
def_tbl["TklW"]= pd.to_numeric(def_tbl["TklW"])
def_tbl["Recov"]=pd.to_numeric(def_tbl["Recov"])

def_tbl = def_tbl[def_tbl["90s"]>8]
def_tbl = def_tbl[(def_tbl["Pos"] == "DF") | (def_tbl["Pos"]== "DF,MF")]

def_tbl["TklWp90"]= def_tbl["TklW"] / def_tbl["90s"]
def_tbl["Recovp90"]= def_tbl["Recov"] / def_tbl["90s"]

def_tbl.loc[0,['Player']] = ['']
def_tbl.loc[9:12,['Player']] = ['']
def_tbl.loc[28,['Player']] = ['']
def_tbl.loc[236,['Player']] = ['']
def_tbl.loc[250,['Player']] = ['']
def_tbl.loc[106:110,['Player']] = ['']
def_tbl.loc[190:195,['Player']] = ['']
def_tbl.loc[335,['Player']] = ['']

a = def_tbl["TklWp90"]
b = def_tbl["Recovp90"]
d= def_tbl['Player']
plt.rcParams.update({'font.size': 25})
bgcol = 'black'

fig, ax = plt.subplots(figsize=(30,28), dpi=400)
ax.scatter(a,b, color = "white")
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(a, b, color='white')

fig= plt.figure(1, figsize=(28, 14), frameon=False, dpi=100)
for x,y,z in zip(a,b,d):
    label = "{}".format(z)
    plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center', color="white")
    
plt.xticks(color="white")
plt.yticks(color="white")
plt.text(0.3,9,"Recoveries and Tackles Won per 90 | PL 23/24 ", color="white", size=50)
plt.text(0.3, 8.7, "Min. of 8 90s played", style="italic", color="white")
#plt.text(x, y, s, kwargs)
plt.ylabel('Recoveries / 90',color='white')
plt.xlabel('Tackles Won / 90',color='white')
plt.hlines(def_tbl["Recovp90"].mean(), def_tbl["TklWp90"].min(), def_tbl["TklWp90"].max(), color='#c2c1c0')
plt.vlines(def_tbl["TklWp90"].mean(), def_tbl["Recovp90"].min(), def_tbl["Recovp90"].max(), color='#c2c1c0')
	
ax.scatter(1.53846,5.76923, color="red", s =200)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8') 
ax.spines['bottom'].set_color('#ccc8c8')


fig.savefig('/Users/damianesene/Desktop/statsbomb/goe_gomez.jpg', dpi=300)


