#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 18:40:34 2023

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

driver = webdriver.Chrome()

whoscored_url="https://www.whoscored.com/Matches/1729516/Live/England-Premier-League-2023-2024-Burnley-Liverpool"
ch_driver=driver.get(whoscored_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.select_one('script:-soup-contains("matchCentreData")')

matchdict = json.loads(element.text.split("matchCentreData: ")[1].split(",\n")[0])

match_events = matchdict['events']
player_ids = matchdict['playerIdNameDictionary']

df= pd.DataFrame(match_events)
player_df=pd.DataFrame.from_dict(player_ids, orient='index', columns=['Values'])
player_df=player_df.reset_index()

#Data cleaning
#drop nan values
df.dropna(subset='playerId', inplace=True)

#make NaN to None. This makes it easy to insert into a DB
df = df.where(pd.notnull(df), None)

#rename columns
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
    'isGoal': 'is_goal'
},
axis=1
)


df =df.rename({
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

#Get subs
subs = df[(df["type_display_name"]=='SubstitutionOff')]
subs=   subs['minute']
firstsub= subs.min()


for column in df.columns:
    if df[column].dtype == np.float64 or df[column].dtype == np.float32:
        df[column]=np.where(
        np.isnan(df[column]),
        None,
        df[column]
        )


goal_df=df[(df["type_display_name"]=="Goal")]
pass_df=df[(df["type_display_name"]=="Pass")]

lfc_pass=pass_df[(pass_df["team_id"]==26)]

lfc_pass["passer"]=lfc_pass["player_id"]
lfc_pass["receiver"]=lfc_pass["player_id"].shift(-1)

succ_pass = lfc_pass[(lfc_pass["outcome_display_name"]=="Successful")]
#Get successful passes before the first sub
succ_pass = succ_pass[succ_pass['minute']<firstsub]

#Get avg locations
avg_loc = succ_pass.groupby('passer').agg({'x':['mean'],'y':['mean','count']})
avg_loc.columns = ['x','y','count']
#avg_loc = avg_loc.reset_index()

#Get passes betwen players, reset index uses default index
pass_btwn = succ_pass.groupby(['passer','receiver']).id.count().reset_index()
pass_btwn.rename({'id':'pass_count'}, axis='columns',inplace=True)

pass_btwn = pass_btwn.merge(avg_loc, left_on='passer', right_index= True)
pass_btwn = pass_btwn.merge(avg_loc, left_on='receiver', right_index= True, suffixes=['','_end'])
pass_btwn = pass_btwn[pass_btwn['pass_count']>2]

pass_btwn['x']= pd.to_numeric(pass_btwn['x'])
pass_btwn['y']= pd.to_numeric(pass_btwn['y'])
pass_btwn['x_end']= pd.to_numeric(pass_btwn['x_end'])
pass_btwn['y_end']= pd.to_numeric(pass_btwn['y_end'])

avg_loc['x']= pd.to_numeric(avg_loc['x'])
avg_loc['y']= pd.to_numeric(avg_loc['y'])

pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b')
fig, ax = pitch.draw()


#Allow your x,y,x_end,y_end to be in accordance to the length of the pitch

for i, row in pass_btwn.iterrows():
    num_passes = row["pass_count"]
    line_width = (num_passes / pass_btwn['pass_count'].max())
    arrows = pitch.arrows(1.2*pass_btwn.x, 80-(0.8*pass_btwn.y), 1.2*pass_btwn.x_end, 80-(0.8*pass_btwn.y_end), alpha=1,ax=ax, headwidth=1,width=2, color='#646F66')

lfc_num = ["3","4","11","1","2","66","18","38","19","9","78"]
avg_loc['player_num'] = lfc_num

MAX_MARKER_SIZE = 1000
avg_loc['marker_size'] = (avg_loc['count']/ avg_loc['count'].max() * MAX_MARKER_SIZE)
nodes = pitch.scatter(1.2*avg_loc.x,80-(0.8*avg_loc.y), s =avg_loc.marker_size, ax=ax, color='#BAF5C5')

for i, row in avg_loc.iterrows():
    pitch.annotate(row.player_num, xy=((1.2*row.x)-2,80-(0.8*row.y)), c='black',ax=ax,weight = "bold", size=10)
#pitch.annotate(avg_loc.player_num, xy=(avg_loc.x+3,80-avg_loc.y), c='white',ax=ax,weight = "bold", size=5)
#108226

#114147 136451 318871 352825 363884 363982 400828 430019
plt.title("LFC Passing Network v Burnley | 26th Dec, 2023 | Turf Moor \n Minute 1-60")

fig.savefig('/Users/damianesene/Desktop/statsbomb/lfc_pass_net_v_burnley.jpg', dpi=300)


