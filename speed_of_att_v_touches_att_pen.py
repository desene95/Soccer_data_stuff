#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 22:41:00 2024

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

import requests

touches_url="https://fbref.com/en/comps/9/possession/Premier-League-Stats"

data=requests.get(touches_url)

soup = BeautifulSoup(data.text)

touches = pd.read_html(data.text, match="Squad Possession")

touches = touches[0]

touches.columns = touches.columns.droplevel(0)

touches = touches.drop(columns=['Def Pen','Def 3rd','Mid 3rd','Att 3rd','Live', 'Att', 'Succ', 'Succ%', 'Tkld',
'Tkld%', 'Carries', 'TotDist', 'PrgDist', 'PrgC', '1/3', 'CPA', 'Mis',
'Dis', 'Rec', 'PrgR' ])

touches['Att Pen p90'] = touches["Att Pen"] / touches["90s"]



opta_url="https://theanalyst.com/eu/2023/08/premier-league-stats-2023-24/"


driver = webdriver.Chrome()

ch_driver=driver.get(opta_url)

opta_soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.find_all('tables')
#opta_data = requests.get(opta_url)

#opta_soup = BeautifulSoup(opta_data.text, 'html.parser')

#opta_table = pd.read_html(opta_data.text, match="data-table")
#opta_table = opta_soup.find_all('table')
#touches = touches.reset_index(drop=True)

#touches = touches.rename({
#    ('Unnamed: 0_level_0 ' ,'Squad'): 'Squad'
#    
#    },
#    axis=1
#    )
