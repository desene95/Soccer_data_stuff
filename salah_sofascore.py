#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:09:05 2023

@author: damianesene
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import json_normalize
url =  'https://www.sofascore.com/player/mohamed-salah/159665#tab:statistics'

import requests

headers = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"3c39829ed7"',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

headers['If-Modified-Since']='Sun, 10 Dec 2023 00:00:00 EST'

response = requests.get(
    'https://api.sofascore.com/api/v1/player/159665/unique-tournament/17/season/52186/statistics/overall',
    headers=headers,
)

print(response.status_code)

mo_salah = response.json()


salah_df = pd.DataFrame.from_dict(mo_salah['statistics'], orient='index', columns=['Values'])
