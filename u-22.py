#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 22:27:40 2024

@author: damianesene
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import numpy as np
import pylab as pl
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

t5_url="https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats"

response = requests.get(t5_url)

tables = pd.read_html(response.text, header=1)
t5_tbl = tables[0]

# Get the tables within the Comments
# =============================================================================
# soup = BeautifulSoup(response.text, 'html.parser')
# comments = soup.find_all(string=lambda text: isinstance(text, Comment))
# for each in comments:
#     if 'table' in str(each):
#         try:
#             t5_tbl = pd.read_html(str(each), header=1)[0]
#             t5_tbl = t5_tbl[t5_tbl['Rk'].ne('Rk')].reset_index(drop=True)
#             t5_tbl.append(t5_tbl)
#         except:
#             continue
# =============================================================================
    

#index_to_retrieve = 25  # Replace with the index you want to retrieve

# Access the value(s) at the specified index
#row_values = t5_tbl.iloc[index_to_retrieve]

#print("Values at index", index_to_retrieve, ":", row_values)
for index, row in t5_tbl.iterrows():
    value_to_find="Rk"
    indices_with_value = t5_tbl.index[t5_tbl['Rk'] == value_to_find].tolist()
    t5_tbl = t5_tbl.drop(indices_with_value)
#print(indices_with_value)
    #print("Index:", index)
    #print("Row values:", row.values)
    #print("------------")  
t5_tbl['90s'] = pd.to_numeric(t5_tbl['90s'])
t5_tbl['Born'] = pd.to_numeric(t5_tbl['Born'])
t5_tbl = t5_tbl[t5_tbl["Born"]>2001]
t5_tbl = t5_tbl[t5_tbl["90s"]>8]