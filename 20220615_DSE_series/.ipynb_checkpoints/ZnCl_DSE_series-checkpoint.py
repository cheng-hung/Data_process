import os
import glob
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


wd = '/Users/chenghunglin/Documents/20220615_XPD_DSE/CsPbBr3_ZnCl2'
subfolders = glob.glob(wd + '/' + '**_min')
subfolders.sort()
subfolders_r = subfolders[::-1]
name_list = [os.path.basename(i) for i in subfolders_r]


##### Check scale factor for bkg data #####

d0 = subfolders_r[0] + '/64uL_min_mean.xy'
d1 = d1 = subfolders_r[0] + '/64uL_min_mean_sub_bkg.xy'
d_bkg = '/Users/chenghunglin/Documents/20220615_XPD_DSE/CsPbBr3_ZnCl2/Kapton_empty_bkg/Kapton_empty_bkg_mean.xy'

df0 = pd.read_csv(d0, header=None, sep=' ')
df1 = pd.read_csv(d1, header=None, sep=' ', on_bad_lines='skip')
df_bkg = pd.read_csv(d_bkg, sep=' ', header=None)

scale_64 = round(((df0[1]-df1[1])/df_bkg[1]).mean(), 3)  ## 1.15
scale_32 = 1.25
scale_16 = 1.25
scale_08 = 1.2
scale_00 = 1.5
scale_list = [scale_64, scale_32, scale_16, scale_08, scale_00]

# df_bkg = pd.read_csv(d_bkg, header=None, sep=' ')
# for i in range(1, len(name_list)):
#     fn = subfolders_r[i] + '/' + name_list[i] + '_mean.xy'
#     df = pd.read_csv(fn, sep=' ', header=None)
#     df_scale = pd.DataFrame()
#     df_scale['q'] = df[0]
#     df_scale['i_sub'] = df[1]-df_bkg[1]*scale_list[i]
#     fn_out = fn[:-3] + '_sub_bkg.xy'
#     df_scale.to_csv(fn_out, sep=' ', index=False, header=False, float_format='{:.8e}'.format)

#############################################

source_par = ['CsPbBr3_Pnma_topas01_Best.par', 'CsPbCl3_Pnma_topas02_Best.par']
des_par = ['CsPbBr3.par', 'CsPbCl3.par']
DFA = 'DFA_s01/'

for k in range(1, len(name_list)):
    cwd = subfolders_r[k] + '/' + DFA
    os.chdir(cwd)
    dwa = glob.glob(subfolders_r[k] + '/' + DFA + '**.dwa') 
    debussy = f'/opt/anaconda3/envs/debussy_unix/bin/Debussy {dwa[0]}'
    subprocess.call([debussy], shell=True)

    try:
        for i, j in zip(source_par, des_par):
            source_folder = subfolders_r[k] + '/' + DFA
            des_folder = subfolders_r[k+1] + '/' + DFA
            cc = f'cp {source_folder+i} {des_folder+j}'
            subprocess.call(cc, shell=True)
    except IndexError:
        print(subfolders_r[k])

