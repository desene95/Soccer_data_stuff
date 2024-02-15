#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 20:28:59 2023

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
from pick_matches import matches
#from itertools import zip
import matplotlib.patheffects as path_effects


view_comps=sb.competitions()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#print(view_comps)




my_comp = matches(43, 106)

Moroc_home_games = my_comp[my_comp.home_team =='Morocco']
Moroc_away_games = my_comp[my_comp.away_team =='Morocco']
Moroc_h_a_games = pd.concat([Moroc_home_games, Moroc_away_games ])
Moroc_h_a_games=Moroc_h_a_games.sort_values(by=['match_date'])

moroc_cro = sb.events(3857277)

moroc_poss = moroc_cro[moroc_cro.possession_team == 'Morocco']

moroc_poss = moroc_poss.dropna(subset=['location'])
moroc_poss[['loc_x', 'loc_y']] = pd.DataFrame(moroc_poss.location.tolist(), index=moroc_poss.index)

# setup pitch
pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
              pitch_color='#22312b', line_color='#efefef')
# draw
# =============================================================================
fig, ax = pitch.draw(figsize=(6.6, 4.125))
fig.set_facecolor('#22312b')
bin_statistic = pitch.bin_statistic(moroc_poss.loc_x, moroc_poss.loc_y, statistic='count', bins=(25, 25))
pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', edgecolors='#22312b')
 
cbar = fig.colorbar(pcm, ax=ax, shrink=0.6)
cbar.outline.set_edgecolor('#efefef')
cbar.ax.yaxis.set_tick_params(color='#efefef')
ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#efefef')
# =============================================================================

csfont = {'fontname':'Tahoma'}


plt.title("Morocco Possession Heat Map v Croatia",**csfont, size=20, color='white')
plt.text(20,85,"Direction of attack")
plt.arrow(60, 83, 40, 0, width=0.7,color="black")
# =============================================================================
# pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f4edf0')
# path_eff = [path_effects.Stroke(linewidth=1.5, foreground='black'),
#             path_effects.Normal()]
# fig, ax = pitch.draw(figsize=(4.125, 6))
# fig.set_facecolor('#f4edf0')
# bin_statistic = pitch.bin_statistic(moroc_poss.loc_x, moroc_poss.loc_y, statistic='count', bins=(6, 5), normalize=True)
# pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', edgecolor='#f9f9f9')
# labels = pitch.label_heatmap(bin_statistic, color='#f4edf0', fontsize=18,
#                              ax=ax, ha='center', va='center',
#                              str_format='{:.0%}', path_effects=path_eff)
# =============================================================================

fig.savefig('/Users/damianesene/Desktop/statsbomb/moroc_poss_map.jpg', dpi=300)






