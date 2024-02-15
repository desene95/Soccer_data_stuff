#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 12:54:41 2023

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


def lfc_recov():
    '''displays ball recoveries'''
    comp_id = input('pick your competition id: ')
    seas_id = input('Pick your season id: ')
    
    my_match = matches(comp_id, seas_id)
    
    lfc_home_games = my_match[my_match.home_team =='Liverpool']
    lfc_away_games = my_match[my_match.away_team =='Liverpool']
    lfc_h_a_games = pd.concat([lfc_home_games, lfc_away_games ])
    
    for i in lfc_h_a_games.match_id:
        print(i)
       
    
    lfc_game = input('What match ID do you want? ')
    picked_game = sb.events(lfc_game)
    
    tackles = picked_game[picked_game.type == 'Ball Recovery']
    
    lfc_recovery = tackles[tackles.team == 'Liverpool']
    game_row = lfc_h_a_games.loc[(lfc_h_a_games.match_id == int(lfc_game))]
    
    lfc_recovery[['loc_x', 'loc_y']] = pd.DataFrame(lfc_recovery.location.tolist(), index=lfc_recovery.index)
    
    pitch = Pitch(pitch_color='green')
    fig, ax = pitch.draw()
    home_team = game_row.home_team[game_row.index].to_string()
    home_team = conv_to_str(home_team)
    
    away_team = game_row.away_team[game_row.index].to_string()
    away_team = conv_to_str(away_team)
    
    home_score = game_row.home_score[game_row.index].to_string()
    home_score = conv_to_str(home_score)
    
    away_score = game_row.away_score[game_row.index].to_string()
    away_score = conv_to_str(away_score)
    
    
    print('Opening Game ID : ', home_team, "vs" , away_team, "\n Final score: ",home_score , "-",away_score )
    
    plots = pitch.scatter(lfc_recovery.loc_x, lfc_recovery.loc_y, ax=ax, color='red')
    return plots

lfc_recov()
    

