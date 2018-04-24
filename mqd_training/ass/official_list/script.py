import pandas as pd
import numpy as np
import six

## filter PDF->Excel file; select Equi from listed securities
def filter(filename):
    bdt_df = pd.read_excel(filename, 1, header=None, index_col=None)
    bdt_df_mat = bdt_df.as_matrix()
    bdt_equi_list = []
    bdt_gdrs_list = []
    for d in bdt_df_mat:
        equi_flag = False
        gdrs_flag = False
        for s in d:
            if isinstance(s, six.string_types):
                if "equi." in s.lower():
                    equi_flag = True
                if ("gdr" in s.lower()) or ("gds" in s.lower()) :
                    gdrs_flag = True

        if equi_flag:
            if gdrs_flag:
                bdt_gdrs_list.append(d)
            else:
                bdt_equi_list.append(d)
    return pd.DataFrame(bdt_equi_list), pd.DataFrame(bdt_gdrs_list)

bdt_equi_list, bdt_gdrs_list = filter('Bdt.xlsx')
mf_equi_list, mf_gdrs_list = filter('EuroMF.xlsx')
# bdt_equi_list.to_csv('bdt_equi_list.csv')
# bdt_gdrs_list.to_csv('bdt_gdrs_list.csv')
# mf_equi_list.to_csv('mf_equi_list.csv')
# mf_gdrs_list.to_csv('mf_gdrs_list.csv')

## reformat: merge multiple name columns into one
def reformat(raw_mat):
    raw_mat = raw_mat.as_matrix()
    ref_mat = np.empty((raw_mat.shape[0],7),dtype=np.object)
    for i,r in enumerate(raw_mat):
        ref_mat[i,0] = r[0]
        name_str = ''
        for j,c in enumerate(r[1:]):
            if isinstance(c, six.string_types):
                if "equi." in c.lower():
                    break
                else:
                    name_str += " " + c
                    ref_mat[i,1] = name_str

        counter = 0
        for s in r[j+1:]:
            if isinstance(s, datetime.datetime):
                s = s.strftime('%d/%m/%Y')
            if isinstance(s, six.string_types):
                ref_mat[i,2+counter] = s
                counter+=1

    return pd.DataFrame(ref_mat)

mat_list = [bdt_equi_list, bdt_gdrs_list, mf_equi_list, mf_gdrs_list]
reformated_list =[reformat(i) for i in mat_list]
filename_str = ['Bdt_equi_list.csv', 'Bdt_gdrs_list.csv', 'EuroMF_equi_list.csv','EuroMF_gdrs_list.csv']

[i.to_csv("equity_filtered_list/"+j) for i,j in zip(reformated_list, filename_str)]

## compare trth & filtered result
trth_list = pd.read_csv('trth_equity_speedguide.csv', header=None, index_col=None).as_matrix()[1:,:]
isin_list = trth_list[:,1].tolist()
official_list = reformated_list[0].as_matrix()[:,0].tolist() + reformated_list[2].as_matrix()[:,0].tolist()

isin_list = [i.split("->")[-1] if "->" in i else i for i in isin_list]

wrong_isin=list()

not_in_official = set(isin_list) - set(official_list)
not_in_trth = set(official_list) - set(isin_list)

# write not in trth but in official into csv
bdt_mat = reformated_list[0].as_matrix()
mf_mat = reformated_list[2].as_matrix()
bdt_not_list = list()
mf_not_list = list()
for i in not_in_trth:
    for j in bdt_mat:
        if i==j[0]:
            bdt_not_list.append(j)
    for j in mf_mat:
        if i==j[0]:
            mf_not_list.append(j)
pd.DataFrame(bdt_not_list).to_csv("./equity_filtered_list/bdt_not_in_trth.csv")
pd.DataFrame(mf_not_list).to_csv("./equity_filtered_list/mf_not_in_trth.csv")

# write not in official but in trth to csv
trth_not_list=list()
for i in not_in_official:
    for j in trth_list:
        if i==j[1]:
            trth_not_list.append(j)
pd.DataFrame(trth_not_list).to_csv("./equity_filtered_list/trth_not_in_official.csv")


