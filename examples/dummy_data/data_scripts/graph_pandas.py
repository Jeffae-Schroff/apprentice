import argparse
import importlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# python3 ../../data_scripts/graph_pandas.py results/many_tunes 2_exp
parser = argparse.ArgumentParser()
parser.add_argument("tunesFolder", help="folder with data in .csv files from many tunes", type=str)
parser.add_argument("experimentName", help="Ex: 2_exp or 2_gauss, determines which target params to give to surrogate", type=str)
parser.add_argument("--chi2outFolder", help="folder to put out chi graph for every method", default="results/important_graphs/", type=str)
parser.add_argument("--otheroutFolder", help="folder for other graphs", default="results/panda_graphs/", type=str)
# add optional output later
args = parser.parse_args()
vals = importlib.import_module(args.experimentName)

filenames = list(os.walk(args.tunesFolder, topdown=False))[0][2]

for tunesFile in filenames:
    df = pd.read_csv(args.tunesFolder+'/'+tunesFile)

    onbound = df.loc[df['ONBOUND'] == True]
    offbound = df.loc[df['ONBOUND'] == False]

    tunes_type = tunesFile.split('/')[-1].split('.')[0]
    save_location = args.otheroutFolder + args.experimentName.split('/')[-1] + '_' + tunes_type
    plt.scatter(onbound[vals.pnames[0]], onbound[vals.pnames[1]], alpha = 0.5, label = 'ONBOUND')
    plt.scatter(offbound[vals.pnames[0]], offbound[vals.pnames[1]], alpha = 0.5, label = 'not ONBOUND')
    plt.title(args.experimentName + '_' + tunes_type +' many_tunes')
    plt.xlim([vals.p_min[0], vals.p_max[0]])
    plt.ylim([vals.p_min[1], vals.p_max[1]])
    plt.xlabel(vals.pnames[0])
    plt.ylabel(vals.pnames[1])
    plt.legend()
    plt.savefig(save_location +"_tunes.pdf")
    plt.close() 

    bins=np.histogram(np.hstack((onbound['chi2'], offbound['chi2'])), bins=50)[1]
    plt.hist(onbound['chi2'], bins = bins, alpha = 0.5, label = 'ONBOUND')
    plt.hist(offbound['chi2'], bins = bins, alpha = 0.5, label = 'not ONBOUND')
    plt.title(args.experimentName + '_' + tunes_type+' chi2/ndf')
    plt.xlabel('chi2/ndf')
    plt.ylabel('frequency')
    plt.legend()
    plt.savefig(save_location + "_chi2.pdf")
    plt.close()

# plot chi2 on same graph
text = ''
for tunesFile in filenames:
    df = pd.read_csv(args.tunesFolder+'/'+tunesFile)

    offbound = df.loc[df['ONBOUND'] == False]

    tunes_type = tunesFile.split('/')[-1].split('.')[0]
    
    if args.experimentName == '2_exp':
            bins = np.logspace(-1.5,2.5,100)
    elif args.experimentName == '2_gauss_v2':
            bins = np.logspace(-1.5,2.5,100)
    else:
        print('bins whoopies, graph_panadas')
    weights = [1/offbound['chi2'].size]*offbound['chi2'].size
    
    tune_stats = tunes_type + ': ' + str(round(offbound['chi2'].mean(), 3)) + ' +/- ' + str(round(offbound['chi2'].std(), 3)) + '\n'
    text += tune_stats
    plt.hist(offbound['chi2'], weights = weights, bins = bins, alpha = 0.5, label = tune_stats)

print(text)
plt.title(args.experimentName +' chi2/ndf')
plt.gca().set_xscale("log")
plt.xlabel('chi2/ndf')
plt.ylabel('Density')
plt.legend()
plt.savefig(args.chi2outFolder +  args.experimentName + "_every_offbound_chi2.pdf")
plt.close()