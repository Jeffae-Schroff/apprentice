import argparse
import os
import importlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# python3 ../../data_scripts/graph_pandas.py 2_gauss_v2 results/many_tunes/tune_w_cov.csv
parser = argparse.ArgumentParser()
parser.add_argument("experimentName", help="Ex: 2_exp or 2_gauss, determines which target params to give to surrogate", type=str)
parser.add_argument("tunesFile", help="csv file with data from many tunes", type=str)
args = parser.parse_args()
vals = importlib.import_module('set_values_' + args.experimentName)

df = pd.read_csv(args.tunesFile)
if(not os.path.isdir('results/panda_tunes_graphs')):
    os.mkdir('results/panda_tunes_graphs/')

onbound = df.loc[df['ONBOUND'] == True]
offbound = df.loc[df['ONBOUND'] == False]

tunes_type = args.tunesFile.split('/')[-1].split('.')[0]
save_location = "results/panda_tunes_graphs/"+ args.experimentName.split('/')[-1]+tunes_type
plt.scatter(onbound[vals.pnames[0]], onbound[vals.pnames[1]], alpha = 0.5, label = 'ONBOUND')
plt.scatter(offbound[vals.pnames[0]], offbound[vals.pnames[1]], alpha = 0.5, label = 'not ONBOUND')
plt.title(args.experimentName + '_' + tunes_type+' many_tunes')
plt.xlabel(vals.pnames[0])
plt.ylabel(vals.pnames[1])
plt.savefig(save_location +".pdf")
plt.close() 

bins = np.linspace(15,50,100)
# plt.hist(onbound['chi2'], bins, alpha = 0.5, label = 'ONBOUND')
# plt.hist(offbound['chi2'], bins, alpha = 0.5, label = 'not ONBOUND')
plt.hist(offbound['chi2'], bins = 100, alpha = 0.5, label = 'not ONBOUND')
plt.title(args.experimentName + '_' + tunes_type+' chi2/ndf')
plt.xlabel('chi2/ndf')
plt.ylabel('frequency')
plt.legend()
plt.savefig(save_location + "_chi2.pdf")