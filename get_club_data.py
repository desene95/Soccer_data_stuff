#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:03:22 2023

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


def get_team_data(team):
    base_url = "https://understat.com/team/"
    full_url= base_url +team
    res =requests.get(full_url)
    soup=BeautifulSoup(res.content)
    scripts=soup.find_all("script")
    strings = scripts[1].string

    str_start = strings.index("('")+2
    str_end = strings.index("')")
    json_data = strings[str_start:str_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')

    data=json.loads(json_data)

    
    return data

club_data = json_normalize(get_team_data("Liverpool"))

club_data = club_data[club_data.isResult==True]
match_ids = []
for x in club_data.id:
    match_url = "https://understat.com/match/" + x
    match_ids.append(x)
    

def get_shots_per_match(match_id):
    base_url = "https://understat.com/match/"
    url = base_url + match_id
    res =requests.get(url)
    soup=BeautifulSoup(res.content)
    scripts=soup.find_all("script")

    #shots data
    strings = scripts[1].string

    str_start = strings.index("('")+2
    str_end = strings.index("')")
    json_data = strings[str_start:str_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    
    return json_data


def get_home_data(match_index):
    
    game_data= json.loads(get_shots_per_match(match_index))

    data_home = json_normalize(game_data['h'])
    #data_away = json_normalize(game_data['a'])
    return data_home

def get_away_data(match_index):
    
    game_data= json.loads(get_shots_per_match(match_index))

    #data_home = json_normalize(game_data['h'])
    data_away = json_normalize(game_data['a'])
    return data_away




    
home_data = get_home_data(match_ids[0])
away_data = get_away_data(match_ids[0])

home_data1 = get_home_data(match_ids[1])
away_data1 = get_away_data(match_ids[1])

home_data2 = get_home_data(match_ids[2])
away_data2 = get_away_data(match_ids[2])

home_data3 = get_home_data(match_ids[3])
away_data3 = get_away_data(match_ids[3])

home_data4 = get_home_data(match_ids[4])
away_data4 = get_away_data(match_ids[4])

home_data5 = get_home_data(match_ids[5])
away_data5 = get_away_data(match_ids[5])

home_data6 = get_home_data(match_ids[6])
away_data6 = get_away_data(match_ids[6])

home_data7 = get_home_data(match_ids[7])
away_data7 = get_away_data(match_ids[7])

home_data8 = get_home_data(match_ids[8])
away_data8 = get_away_data(match_ids[8])

home_data9 = get_home_data(match_ids[9])
away_data9 = get_away_data(match_ids[9])



game_1 = pd.merge(home_data,away_data,how="outer")
game_2 = pd.merge(home_data1,away_data1,how="outer")
game_3 = pd.merge(home_data2,away_data2,how="outer")
game_4 = pd.merge(home_data3,away_data3,how="outer")
game_5 = pd.merge(home_data4,away_data4,how="outer")
game_6 = pd.merge(home_data5,away_data5,how="outer")
game_7 = pd.merge(home_data6,away_data6,how="outer")
game_8 = pd.merge(home_data7,away_data7,how="outer")
game_9 = pd.merge(home_data8,away_data8,how="outer")
game_10 = pd.merge(home_data9,away_data9,how="outer")



#game_2 = pd.merge(data_home, data_away,how="outer")
#games = pd.merge(game_1, game_2, how="outer")
lfc_games = pd.merge(game_1,game_2, how="outer")
lfc_games = pd.merge(lfc_games,game_3, how="outer")
    


#Get Data


#shots data
