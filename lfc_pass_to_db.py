#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 21:21:03 2024

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
from sqlalchemy import create_engine
driver = webdriver.Chrome()

url = "https://www.whoscored.com/Matches/1805535/Live/Europe-Europa-League-2023-2024-Sparta-Prague-Liverpool"

ch_driver=driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.select_one('script:-soup-contains("matchCentreData")')

matchdict = json.loads(element.text.split("matchCentreData: ")[1].split(",\n")[0])
away_team = matchdict['away']
lfc_players = away_team['players']
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

df=df[(df['team_id']==26)]
conditions = [
    (df['player_id'] == 322176),
    (df['player_id'] == 136451),
    (df['player_id'] == 345957),
    (df['player_id'] == 430019),
    (df['player_id'] == 115726),
    (df['player_id'] == 345319),
    (df['player_id'] == 86829),
    (df['player_id'] == 363982),
    (df['player_id'] == 352825),
    (df['player_id'] == 400828),
    (df['player_id'] == 377168),
    (df['player_id'] == 108226),
    (df['player_id'] == 369875),
    (df['player_id'] == 95408),
    (df['player_id'] == 450021),
    (df['player_id'] == 424945)

]

player_names = ["Caoimhín Kelleher","Joe Gomez","Ibrahima Konate","Jarell Quansah","Andy Robertson", "Alexis Mac Allister", "Wataru Endo","Harvey Elliott","Cody Gakpo","Darwin Nunex","Luis Diaz","Mohammed Salah","Dominik Szoboszlai","Virgil van Dijk","Bobby Clark","Conor Bradley"]

df['player_name'] = np.select(conditions, player_names, default='')

lfc_pass = df[(df['type_display_name']=='Pass')]

#connect to database
#db_connection_str = 'mysql://root:my_root_pwd@127.0.0.1:3306/soccer-stuff-db'

# Create a SQLAlchemy engine
#engine = create_engine(db_connection_str)

#lfc_pass.to_sql('LFC_PASS', con=engine, if_exists='replace', index=False)

file_name = '/Users/damianesene/Desktop/statsbomb/lfc_match.xlsx'

lfc_pass.to_excel(file_name)