#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 20:00:29 2023

@author: damianesene
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
from matplotlib.patches import Arc
from socc_pitch import football_pitch

base_url = "https://understat.com/match/"

match_id = "21979"

url = base_url+match_id

#Get Data
res =requests.get(url)
soup=BeautifulSoup(res.content)
scripts=soup.find_all("script")

#shots data
strings = scripts[1].string

str_start = strings.index("('")+2
str_end = strings.index("')")
json_data = strings[str_start:str_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

data=json.loads(json_data)

data_home = json_normalize(data['h'])
data_away = json_normalize(data['a'])

data_home['X']=pd.to_numeric(data_home['X'])
data_home['Y']=pd.to_numeric(data_home['Y'])
data_home['xG']=pd.to_numeric(data_home['xG'])

data_home['X_1'] = (data_home['X']/100)*105*100
data_home['Y_1'] = (data_home['Y']/100)*68*100

home_goals= data_home[data_home.result=='Goal']
home_missed = data_home[data_home.result=='MissedShots']
home_saved = data_home[data_home.result=='SavedShot']
home_blocked = data_home[data_home.result=='BlockedShot']

fig, ax = plt.subplots(figsize=(10, 10))
football_pitch(orientation="horizontal",aspect="full",line_color="black",ax=ax,axis="off")

plt.scatter(x=home_goals["X_1"],y=home_goals["Y_1"],s=home_goals['xG']*720, marker='o',color='green',edgecolors="black",label='Goals')
plt.scatter(x=home_missed["X_1"],y=home_missed["Y_1"],s=home_missed['xG']*720, marker='o',color='purple',edgecolors="black",label='Missed Shots')
plt.scatter(x=home_saved["X_1"],y=home_saved["Y_1"],s=home_saved['xG']*720, marker='o',color='red',edgecolors="black",label='Saved Shots')
plt.scatter(x=home_blocked["X_1"],y=home_blocked["Y_1"],s=home_blocked['xG']*720, marker='o',color='orange',edgecolors="black",label='Blocked Shots')


legend = ax.legend(loc="upper center",bbox_to_anchor= (0.14, 0.88),labelspacing=1.3,prop={'weight':'bold','size':11})
legend.legendHandles[0]._sizes = [500]
legend.legendHandles[1]._sizes = [500]
legend.legendHandles[2]._sizes = [500]
legend.legendHandles[3]._sizes = [500]

from highlight_text import fig_text
fig_text(0.3,0.76, s="LFC Shots v Everton \n", fontsize = 25, fontweight = "bold",c='black')
fig_text(0.74,0.76, s="@dame_world \n", fontsize = 12, fontweight = "bold",c='black')
fig.savefig('/Users/damianesene/Desktop/statsbomb/lfc_shot_v_eve.jpg', dpi=300)



