#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 20:25:24 2023

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
    print(comps)
    
    matche_s = sb.matches(x, y)
    
    return matche_s