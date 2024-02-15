#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 21:20:18 2023

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

driver = webdriver.Chrome()

whoscored_url="https://www.whoscored.com/Matches/1729226/Live/England-Premier-League-2023-2024-Manchester-United-Manchester-City"
ch_driver=driver.get(whoscored_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.select_one('script:-soup-contains("matchCentreData")')

matchdict = json.loads(element.text.split("matchCentreData: ")[1].split(",\n")[0])

match_events = matchdict['events']

df= pd.DataFrame(match_events)

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



for column in df.columns:
    if df[column].dtype == np.float64 or df[column].dtype == np.float32:
        df[column]=np.where(
        np.isnan(df[column]),
        None,
        df[column]
        )

pitch = Pitch(pitch_color='green')
fig, ax = pitch.draw()
pass_df=df[(df["type_display_name"]=="Pass")]
#plots = pitch.scatter(df., avg_loc_y, ax=ax, color= y, s=200)










