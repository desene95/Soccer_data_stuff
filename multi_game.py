#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 16:34:45 2024

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

whoscored_url = "https://www.whoscored.com/Teams/26/Show/England-Liverpool"

#ch_driver=driver.get(whoscored_url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.select_one('script:-soup-contains("fixtureMatches")')

cols = []
for x in range(1,33):
    x=str(x)
    
    col_name="id"+x
    cols.append(col_name)
    #print(cols)
print(cols)
#columns = ["Game-Id","rand_num","Date","Time","Team ID","Home Team","ran_num2","ran_num3","Away Team","ran_num4","Final Score","1H Score","ran_num5","ran_num6","Full Time","Season","Competition","ran_num7","ran_num6","ran_num6","ran_num6","ran_num6","ran_num6"]
#matchdict = json.loads(element.text.split("fixtureMatches: ")[1].split(",\n")[0])
matches = element.text.split("fixtureMatches:")[1].split(",\n")[0]
matches=matches[6:]
#matches=matches.split(']')
#matches = matches
#matches=matches[0]
#matchdict = json.loads(element.text.split("fixtureMatches: "))