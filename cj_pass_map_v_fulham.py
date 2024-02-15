#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 22:03:42 2024

@author: damianesene
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:05:32 2024

@author: damianesene
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 23:21:43 2024

@author: damianesene
"""
import json
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Optional
from selenium import webdriver
from supabase import create_client, Client
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter
driver = webdriver.Chrome()

cj_url="https://www.whoscored.com/Matches/1790745/Live/England-League-Cup-2023-2024-Liverpool-Fulham"   


ch_driver=driver.get(cj_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.select_one('script:-soup-contains("matchCentreData")')

matchdict = json.loads(element.text.split("matchCentreData: ")[1].split(",\n")[0])
home_team = matchdict['home']
lfc_players = home_team['players']
lfc_df = pd.DataFrame(lfc_players)
match_events = matchdict['events']
df= pd.DataFrame(match_events)
df.dropna(subset='playerId', inplace=True)

df = df.where(pd.notnull(df), None)

df = df.rename(
{
    'eventId': 'event_id',
    'expandedMinute': 'expanded_minute',
    'outcomeType': 'outcome_type',
    'isTouch': 'is_touch',
    'playerId': 'player_id',
    'endX': 'end_x',
    'endY': 'end_y',
    'blockedX': 'blocked_x',
    'blockedY': 'blocked_y',
    'goalMouthZ': 'goal_mouth_z',
    'goalMouthY': 'goal_mouth_y',
    'isShot': 'is_shot',
    'cardType': 'card_type',
    'isGoal': 'is_goal',
    'teamId': 'team_id'
},
axis=1
)

#Get the period name and type from period column
df['period_display_name'] = df['period'].apply(lambda x: x['displayName'])
df['type_display_name'] = df['type'].apply(lambda x: x['displayName'])
df['outcome_display_name'] = df['outcome_type'].apply(lambda x: x['displayName'])


#drop irrelevant columns
df.drop(columns=['period','type', 'outcome_type'], inplace=True)

#specify what columns you want
df = df[[
    'id','event_id', 'minute','second','team_id','player_id','x','y','end_x','end_y',
    'qualifiers', 'is_touch', 'blocked_x', 'blocked_y', 'goal_mouth_z','goal_mouth_y', 'is_shot',
    'card_type', 'is_goal', 'type_display_name', 'outcome_display_name', 'period_display_name'
]]


#convert columns to int data type
df[['id','event_id','minute','team_id','player_id']] = df[['id','event_id','minute','team_id','player_id']].astype(int)
df[['second', 'x', 'y','end_x','end_y' ]] = df[['second', 'x', 'y','end_x','end_y' ]].astype(float)
df[['is_shot','is_goal','card_type']]= df[['is_shot','is_goal','card_type']].astype(bool)

df['is_goal']=df['is_goal'].fillna(False)
df['is_shot']=df['is_shot'].fillna(False)
goal=df[(df["is_goal"]==True)]
cj_events = df[(df["player_id"]==355354)]
cj_pass = cj_events[(cj_events["type_display_name"]=="Pass")]



pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
              pitch_color='#22312b', line_color='#efefef')
# draw
fig, ax = pitch.draw(figsize=(6.6, 4.125))
fig.set_facecolor('#22312b')
arrows = pitch.arrows(1.2*cj_pass.x, 80-(0.8*cj_pass.y), 1.2*cj_pass.end_x, 80-(0.8*cj_pass.end_y), alpha=1,ax=ax, headwidth=1,width=2, color='white')

#plt.scatter(x=cj_goals["x"],y=80-cj_goals["y"],s=0.03*720, marker='o',color='green',edgecolors="black",label='Goals')
