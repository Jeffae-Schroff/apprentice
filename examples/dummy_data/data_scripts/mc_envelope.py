# %makes envelope plot of Monte Carlo runs%
import yoda
import numpy as np
import os
import argparse
from math import ceil
import matplotlib.pyplot as plt
import importlib

# python3 ../../data_scripts/mc_envelope.py 2_exp

parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("experimentName", help="Ex: 2_exp, determines which values to use and name of save folder", type=str)

# Parse arguments
args = parser.parse_args()
vals = importlib.import_module(args.experimentName)

num_obs = 2

n_bins = 0
n_obs = 0
bin_min = []
bin_mid = []
bin_vals = []
obs_names = []

directory = os.getcwd() + "/MC"

for filename in os.listdir(directory):
    folder = os.path.join(directory, filename)
    if not os.path.isfile(folder):
        data = yoda.read(folder + "/combined.yoda", asdict=False)
        for h in data:
            n_obs += 1
            bin_vals.append([])
            obs_names.append(h.path()[1:])

        h = data[0]
        
        for b in h.bins():
            bin_min.append(b.xMin())
            bin_mid.append(b.xMid())
            n_bins += 1
        break


for filename in os.listdir(directory):
    folder = os.path.join(directory, filename)
    if not os.path.isfile(folder):
        data = yoda.read(folder + "/combined.yoda", asdict=False)
        for i in range(len(data)):
            h = data[i]
            for b in h.bins():
                bin_vals[i].append(b.height())

for i in range(len(data)):
    np_bin_vals = np.array(bin_vals[i]).reshape(42,20)
    plt.figure()
    plt.hist(bin_mid, bin_min, weights = np_bin_vals.max(axis=0), histtype='step')
    plt.hist(bin_mid, bin_min, weights = np_bin_vals.min(axis=0), histtype='step')
    plt.title(obs_names[i] + ' MC envelope')
    plt.xlabel('x')
    plt.ylabel('Number of Events')
    plt.savefig('results/important_graphs/observable_envelopes/' + obs_names[i] +'.pdf')