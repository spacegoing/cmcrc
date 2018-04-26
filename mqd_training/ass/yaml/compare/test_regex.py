# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import six
import re

def remove(selected_files, rics_list):
    a = list(selected_files)
    b = set(rics_list) - set(a)
    return list(b)

def save_csv(list_var,name):
    pd.DataFrame(list_var).to_csv(name)

origin_mat = pd.read_excel('11397.xlsx', 0, header=None, index_col=None).as_matrix()[1:,:]
rics_vec = origin_mat[:,0]
rics_list = rics_vec.tolist()

# remove warrents
regex = re.compile('\_t.LU$')
warr_list = filter(regex.search, rics_list)

selected_files = remove(warr_list, rics_list)
selected_files_vec = np.array(selected_files, dtype=np.object)
save_csv(selected_files_vec, 'no_t.csv')

# # remove Debt Instrument
# regex = re.compile('^\d+X.LU$')
# debt_inst_list = filter(regex.search, rics_list)
#
# selected_files = remove(debt_inst_list, selected_files)
# selected_files_vec = np.array(selected_files, dtype=np.object)
# save_csv(selected_files_vec, 'no_t.csv')

# remove noise rics
regex = re.compile('^\d+[A-Za-z]+.LU$')
noise_list = filter(regex.search, rics_list)

selected_files = remove(noise_list, selected_files)
selected_files_vec = np.array(selected_files, dtype=np.object)
save_csv(selected_files_vec, 'no_t.csv')
