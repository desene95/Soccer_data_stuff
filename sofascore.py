#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 13:12:05 2023

@author: damianesene
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import json_normalize
url =  'https://www.sofascore.com/west-ham-united-tottenham-hotspur/IM#id:11777279'

#response = requests.get(url, headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})
#soup = BeautifulSoup(response.text, 'html.parser')
#soup.select('g[cursor="pointer"]')

#get access to SFscore api for shot map
import requests

headers = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"9815214080"',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

#response = requests.get('https://api.sofascore.com/api/v1/event/11777279/shotmap', headers=headers)

#add this key and value to the headers
headers['If-Modified-Since']='Sun, 10 Dec 2023 00:00:00 EST'
response = requests.get('https://api.sofascore.com/api/v1/event/11777279/shotmap', headers=headers)
print(response.status_code)

shots = response.json()

shots_df = pd.DataFrame.from_dict(shots['shotmap'])

shots_df['player_name'] = shots_df['player'].apply(lambda x: x.get('name'))
    
    
    
    