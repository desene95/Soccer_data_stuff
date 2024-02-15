#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:33:40 2024

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

cj_url="https://www.whoscored.com/Matches/1729532/Live/England-Premier-League-2023-2024-Bournemouth-Liverpool"   


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

maca_events = df[(df["player_id"]==345319)]

maca_def_act = maca_events[(maca_events["type_display_name"]=="BlockedPass") | (maca_events["type_display_name"]=="BallRecovery") | (maca_events["type_display_name"]=="Tackle") | (maca_events["type_display_name"]=="Interception") |(maca_events["type_display_name"]=="Challenge")]

pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
              pitch_color='black', line_color='#efefef')
# draw
fig, ax = pitch.draw(figsize=(6.6, 4.125))
fig.set_facecolor('black')
maca_def_act = maca_def_act[maca_def_act['y'] <=80]
maca_def_act= maca_def_act.reset_index(drop=True)

    
plt.gca().invert_yaxis()
#for x in range(len(maca_def_act['x'])):
for i,shot in maca_def_act.iterrows():
    x=shot['x']
    y=shot['y']
    if shot['type_display_name']=="BlockedPass" and shot["outcome_display_name"]=="Successful":
        #arrows = pitch.arrows(1.2*maca_pass['x'][x], (0.8*maca_pass['y'][x]), 1.2*maca_pass['end_x'][x], (0.8*maca_pass['end_y'][x]), alpha=1,ax=ax, headwidth=3,width=2, color='red')
        #plt.plot(maca_def_act['x'][x], maca_def_act['y'][x], color='white')
        def_circle=plt.Circle((x,y),2,color="red")
        ax.add_patch(def_circle)
    elif shot['type_display_name']=="BallRecovery" and shot["outcome_display_name"]=="Successful":
        def_circle=plt.Circle((x,y),2,color="grey")
        ax.add_patch(def_circle)
    elif shot['type_display_name']=="Tackle" and shot["outcome_display_name"]=="Successful":
        def_circle=plt.Circle((x,y),2,color="blue")
        ax.add_patch(def_circle)
    elif shot['type_display_name']=="Interception" and shot["outcome_display_name"]=="Successful":
        def_circle=plt.Circle((x,y),2,color="yellow")
        ax.add_patch(def_circle)
    elif shot['type_display_name']=="Challenge" and shot["outcome_display_name"]=="Successful":
        def_circle=plt.Circle((x,y),2,color="purple")
        ax.add_patch(def_circle)
        
fig.savefig('/Users/damianesene/Desktop/statsbomb/maca_def_actions.jpg', dpi=300)
        
