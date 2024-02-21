#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:00:47 2024

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
import re
driver = webdriver.Chrome()

url = "https://www.whoscored.com/Teams/26/Fixtures/England-Liverpool"

ch_driver=driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

element = soup.select_one('script:-soup-contains("fixtureMatches")')

matches = element.text.split("fixtureMatches: [")[1]

#grab all match ids from the string matches
match_ids = [int(match.group(0)) for match in re.finditer(r'\b17\d+\b', matches)]

#fixture_dict = json.loads(element.text.split("fixtureMatches:[26, [")[1].split(',\n')[0])

#matchdict = json.loads(element.text.split("matchCentreData: ")[1].split(",\n")[0])


#element = soup.find_all('tables')