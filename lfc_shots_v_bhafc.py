#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:36:39 2023

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


def football_pitch(x_min=0, x_max=105,
               y_min=0, y_max=68,
               pitch_color="#f0f0f0",
               line_color='black',
               line_thickness=1.5,
               point_size=20,
               orientation="horizontal",
               aspect="full",
               axis='off',
               ax=None
               ):

    if not ax:
        raise TypeError("This function is intended to be used with an existing fig and ax in order to allow flexibility in plotting of various sizes and in subplots.")


    if orientation.lower().startswith("h"):
        first = 0
        second = 1
        arc_angle = 0

        if aspect == "half":
            ax.set_xlim(x_max / 2, x_max + 5)

    elif orientation.lower().startswith("v"):
        first = 1
        second = 0
        arc_angle = 90

        if aspect == "half":
            ax.set_ylim(x_max / 2, x_max + 5)

    
    else:
        raise NameError("You must choose one of horizontal or vertical")
    
    ax.axis(axis)

    rect = plt.Rectangle((x_min, y_min),
                         x_max, y_max,
                         facecolor=pitch_color,
                         edgecolor="none",
                         zorder=-2)

    ax.add_artist(rect)

    x_conversion = x_max / 100
    y_conversion = y_max / 100

    pitch_x = [0,5.8,11.5,17,50,83,88.5,94.2,100] # x dimension markings
    pitch_x = [x * x_conversion for x in pitch_x]

    pitch_y = [0, 21.1, 36.6, 50, 63.2, 78.9, 100] # y dimension markings
    pitch_y = [x * y_conversion for x in pitch_y]

    goal_y = [45.2, 54.8] # goal posts
    goal_y = [x * y_conversion for x in goal_y]

    # side and goal lines
    lx1 = [x_min, x_max, x_max, x_min, x_min]
    ly1 = [y_min, y_min, y_max, y_max, y_min]

    # outer box
    lx2 = [x_max, pitch_x[5], pitch_x[5], x_max]
    ly2 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    lx3 = [0, pitch_x[3], pitch_x[3], 0]
    ly3 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    # goals
    lx4 = [x_max, x_max+2, x_max+2, x_max]
    ly4 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    lx5 = [0, -2, -2, 0]
    ly5 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    # 6 yard box
    lx6 = [x_max, pitch_x[7], pitch_x[7], x_max]
    ly6 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]

    lx7 = [0, pitch_x[1], pitch_x[1], 0]
    ly7 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]


    # Halfline, penalty spots, and kickoff spot
    lx8 = [pitch_x[4], pitch_x[4]]
    ly8 = [0, y_max]

    lines = [
        [lx1, ly1],
        [lx2, ly2],
        [lx3, ly3],
        [lx4, ly4],
        [lx5, ly5],
        [lx6, ly6],
        [lx7, ly7],
        [lx8, ly8],
        ]

    points = [
        [pitch_x[6], pitch_y[3]],
        [pitch_x[2], pitch_y[3]],
        [pitch_x[4], pitch_y[3]]
        ]

    circle_points = [pitch_x[4], pitch_y[3]]
    arc_points1 = [pitch_x[6], pitch_y[3]]
    arc_points2 = [pitch_x[2], pitch_y[3]]


    for line in lines:
        ax.plot(line[first], line[second],
                color=line_color,
                lw=line_thickness,
                zorder=-1)

    for point in points:
        ax.scatter(point[first], point[second],
                   color=line_color,
                   s=point_size,
                   zorder=-1)

    circle = plt.Circle((circle_points[first], circle_points[second]),
                        x_max * 0.088,
                        lw=line_thickness,
                        color=line_color,
                        fill=False,
                        zorder=-1)

    ax.add_artist(circle)

    arc1 = Arc((arc_points1[first], arc_points1[second]),
               height=x_max * 0.088 * 2,
               width=x_max * 0.088 * 2,
               angle=arc_angle,
               theta1=128.75,
               theta2=231.25,
               color=line_color,
               lw=line_thickness,
               zorder=-1)

    ax.add_artist(arc1)

    arc2 = Arc((arc_points2[first], arc_points2[second]),
               height=x_max * 0.088 * 2,
               width=x_max * 0.088 * 2,
               angle=arc_angle,
               theta1=308.75,
               theta2=51.25,
               color=line_color,
               lw=line_thickness,
               zorder=-1)

    ax.add_artist(arc2)

    ax.set_aspect("equal")

    return ax

base_url = "https://understat.com/match/"

match_id = "21966"

url = base_url+match_id

#Get Data
res =requests.get(url)
soup=BeautifulSoup(res.content)
scripts=soup.find_all("script")

#shots data
strings = scripts[1].string


#Decode data
str_start = strings.index("('")+2
str_end = strings.index("')")
json_data = strings[str_start:str_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

data=json.loads(json_data)

data_home = json_normalize(data['h'])
data_away = json_normalize(data['a'])



data_away['X']=pd.to_numeric(data_away['X'])
data_away['Y']=pd.to_numeric(data_away['Y'])
data_away['xG']=pd.to_numeric(data_away['xG'])

data_away['X_1'] = (data_away['X']/100)*105*100
data_away['Y_1'] = (data_away['Y']/100)*68*100

away_goals= data_away[data_away.result=='Goal']
away_missed = data_away[data_away.result=='MissedShots']
away_saved = data_away[data_away.result=='SavedShot']
away_blocked = data_away[data_away.result=='BlockedShot']

fig, ax = plt.subplots(figsize=(20, 10))
football_pitch(orientation="horizontal",aspect="full",line_color="black",ax=ax,axis="off")



plt.scatter(x=away_goals["X_1"],y=away_goals["Y_1"],s=away_goals['xG']*720, marker='o',color='green',edgecolors="black",label='Goals')
plt.scatter(x=away_missed["X_1"],y=away_missed["Y_1"],s=away_missed['xG']*720, marker='o',color='purple',edgecolors="black",label='Missed Shots')
plt.scatter(x=away_saved["X_1"],y=away_saved["Y_1"],s=away_saved['xG']*720, marker='o',color='red',edgecolors="black",label='Saved Shots')
plt.scatter(x=away_blocked["X_1"],y=away_blocked["Y_1"],s=away_blocked['xG']*720, marker='o',color='orange',edgecolors="black",label='Blocked Shots')

legend = ax.legend(loc="upper center",bbox_to_anchor= (0.14, 0.88),labelspacing=1.3,prop={'weight':'bold','size':11})
legend.legendHandles[0]._sizes = [500]
legend.legendHandles[1]._sizes = [500]
legend.legendHandles[2]._sizes = [500]
legend.legendHandles[3]._sizes = [500]
#legend.legendHandles[4]._sizes = [500]

from highlight_text import fig_text
fig_text(0.38,0.91, s="LFC Shots v Brighton  \n", fontsize = 25, fontweight = "bold",c='black')
fig_text(0.7,0.91, s="@DAME_WORLD \n", fontsize = 10, fontweight = "bold",c='black')

fig.savefig('/Users/damianesene/Downloads/lfc_shots_v_bhafc.jpg', dpi=300)