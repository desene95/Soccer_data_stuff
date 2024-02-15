#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 16:21:02 2023

@author: damianesene
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import numpy as np
import pylab as pl
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch


comps = sb.competitions()

comps

def matches(x,y):
    '''Picks what matches you want to view. x=competition id, y=season id'''
    
    matche_s = sb.matches(x, y)
    
    return matche_s
   
def conv_to_str(x):
    x = x.split()
    x.pop(0)
    my_string = ' '
    for k in x:
        my_string += ' ' + k
    return my_string

my_match = matches(2,27)
leic_home_games = my_match[my_match.home_team =='Leicester City']
leic_away_games = my_match[my_match.away_team =='Leicester City']
leic_h_a_games = pd.concat([leic_home_games, leic_away_games ])
leic_h_a_games=leic_h_a_games.sort_values(by=['match_date'])

picked_game = sb.events(3754237)


vard_events = picked_game[picked_game.player == 'Jamie Vardy']
vard_events=vard_events.dropna(subset=['location'])
vard_events[['loc_x', 'loc_y']] = pd.DataFrame(vard_events.location.tolist(), index=vard_events.index)
#vard_events[['avg_loc_x']] = vard_events['loc_x'].mean()
avg_loc_x = vard_events['loc_x'].mean()
avg_loc_y = vard_events['loc_y'].mean()

pitch = Pitch(pitch_color='green')
fig, ax = pitch.draw()

plots = pitch.scatter(avg_loc_x, avg_loc_y, ax=ax, color='blue')


