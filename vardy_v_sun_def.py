#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:47:07 2023

@author: damianesene
"""

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

picked_game = sb.events(3754237) #leic vs sunderland

home_team_form = picked_game.iloc[0]['tactics']
away_team_form = picked_game.iloc[1]['tactics']

for p in home_team_form['lineup']:
    print('Leicester City Players: ', p['player']['name'])

for q in away_team_form['lineup']:
    print('Sunderland Players: ', q['player']['name'])
    
plot_player = True

#while plot_player:
#def plot_player(x,y,z,a):
 #player_name = input('what player: ')
 
player_name = input('what player: ')
player1_name = input('what player: ')
player2_name = input('what player: ')
player3_name = input('what player: ')
player4_name = input('what player: ')


team_color = input('team color: (red or blue) ')
team1_color = input('team color: (red or blue) ')
team2_color = input('team color: (red or blue) ')
team3_color = input('team color: (red or blue) ')
team4_color = input('team color: (red or blue) ')
 
 
player_events = picked_game[picked_game.player == player_name]
player1_events = picked_game[picked_game.player == player1_name]
player2_events = picked_game[picked_game.player == player2_name]
player3_events = picked_game[picked_game.player == player3_name]
player4_events = picked_game[picked_game.player == player4_name]
 #player1_events = picked_game[picked_game.player == z]
 
player_events=player_events.dropna(subset=['location'])
player1_events = player1_events.dropna(subset=['location'])
player2_events = player2_events.dropna(subset=['location'])
player3_events = player3_events.dropna(subset=['location'])
player4_events = player4_events.dropna(subset=['location'])
 
 
player_events[['loc_x', 'loc_y']] = pd.DataFrame(player_events.location.tolist(), index=player_events.index)
player1_events[['loc_x', 'loc_y']] = pd.DataFrame(player1_events.location.tolist(), index=player1_events.index)
player2_events[['loc_x', 'loc_y']] = pd.DataFrame(player2_events.location.tolist(), index=player2_events.index)
player3_events[['loc_x', 'loc_y']] = pd.DataFrame(player3_events.location.tolist(), index=player3_events.index)
player4_events[['loc_x', 'loc_y']] = pd.DataFrame(player4_events.location.tolist(), index=player4_events.index)
 #vard_events[['avg_loc_x']] = vard_events['loc_x'].mean()
avg_loc_x = player_events['loc_x'].mean()
avg_loc_y = player_events['loc_y'].mean()
 
avg1_loc_x = player1_events['loc_x'].mean()
avg1_loc_y = player1_events['loc_y'].mean()
 
avg2_loc_x = player2_events['loc_x'].mean()
avg2_loc_y = player2_events['loc_y'].mean()
 
avg3_loc_x = player3_events['loc_x'].mean()
avg3_loc_y = player3_events['loc_y'].mean()
 
avg4_loc_x = player4_events['loc_x'].mean()
avg4_loc_y = player4_events['loc_y'].mean()
 
 
 
 
pitch = Pitch(pitch_color='green')
fig, ax = pitch.draw()
  #team_color = input('team color: (red or blue) ')
 
 
 
plots = pitch.scatter(avg_loc_x, avg_loc_y, ax=ax, color= team_color, s=200)
pitch.annotate(text='Vardy', xy=(avg_loc_x-3,avg_loc_y+6), xytext=None, ax=ax, color='white')
 
plots1 = pitch.scatter(120-avg1_loc_x, avg1_loc_y, ax=ax, color= team1_color, s=200)
pitch.annotate(text='Jones', xy=(120- avg1_loc_x-3,avg1_loc_y+6), xytext=None, ax=ax, color='white')
 
plots2 = pitch.scatter(120-avg2_loc_x, avg2_loc_y, ax=ax, color= team2_color, s=200)
pitch.annotate(text='Coates', xy=(120- avg2_loc_x-3,avg2_loc_y+6), xytext=None, ax=ax, color='white')
 
plots3 = pitch.scatter(120-avg3_loc_x, avg3_loc_y, ax=ax, color= team3_color, s=200)
l chromadb
pitch.annotate(text='Kaboul', xy=(120- avg3_loc_x-3,avg3_loc_y+6), xytext=None, ax=ax, color='white')
 
plots4 = pitch.scatter(120-avg4_loc_x, avg4_loc_y, ax=ax, color= team4_color, s=200)
pitch.annotate(text='Van Aanholt', xy=(120- avg4_loc_x-3,avg4_loc_y+6), xytext=None, ax=ax, color='white')
 #return plots, plots1



#player_name = input('what player: ')

#player1_name = input('what player: ')

#player2_name = input('what player: ')

#player3_name = input('what player: ')

#player4_name = input('what player: ')


#team2_color = input('team color: (red or blue) ')
#team3_color = input('team color: (red or blue) ')
#team4_color = input('team color: (red or blue) ')

#print(plot_player(player_name, team_color, player1_name, team1_color))

print(plots,plots1, plots2, plots3, plots4)

fig.savefig('/Users/damianesene/Desktop/statsbomb/vardy_pos_v_def.jpg', dpi=300)

# =============================================================================
#     
#     plot_again = input('plot another player: Y/N')
#     if plot_again == 'N':
#         plot_player = False
# =============================================================================
    

