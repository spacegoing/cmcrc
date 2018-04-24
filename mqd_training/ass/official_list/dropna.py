# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
filename = 'hahu0291@uni.sydney.edu.au--N168554113.csv'
full = pd.read_csv(filename, index_col=False, header=None, low_memory=False)
dropped = full.dropna(axis=0, subset=[5])
nodup = dropped.drop_duplicates(subset=[0])
nodup.to_csv('nodup.csv')
