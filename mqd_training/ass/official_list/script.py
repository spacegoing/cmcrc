import pandas as pd
import six

## filter PDF->Excel file; select Equi from listed securities
def filter(filename):
    bdt_df = pd.read_excel(filename, 1, header=None, index_col=None)
    bdt_df_mat = bdt_df.as_matrix()
    bdt_equi_list = []
    for d in bdt_df_mat:
        skip = False
        for s in d:
            if isinstance(s, six.string_types):
                # if "GDR" in s:
                #     break
                if "Equi." in s and skip == False:
                    bdt_equi_list.append(d)

    return bdt_equi_list

bdt_equi_list = filter('Bdt.xlsx')
mf_equi_list = filter('EuroMF.xlsx')
total = bdt_equi_list + mf_equi_list

df_total = pd.DataFrame(total)
df_total.to_csv('filtered_list.csv')

##

filename = 'raw_rics.csv'
bdt_df = pd.read_excel(filename, 1, header=None, index_col=None)
bdt_df_mat = bdt_df.as_matrix()




