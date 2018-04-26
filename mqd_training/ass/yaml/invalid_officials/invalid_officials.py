# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import numpy as np
import six

exported_trth_list = pd.read_csv('trth_exported.csv', header=None, index_col=None).as_matrix()[1:,:]



