# adds error to the inputdata.h5 file using the observation_error function
# (which is stored in the set_values file corresponding with the experimentName it is given)

import importlib
import h5py
import numpy as np
import argparse
parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("experimentName", help="2_exp and 2_gauss valid, also name of folder in results to save to", type=str)
parser.add_argument("errorType", help="linear, low_linear", type=str)
parser.add_argument("h5File", help="where Data and MC are written to", type=str)

# Parse arguments
args = parser.parse_args()
print("Running " + args.experimentName + " with " + args.errorType)
vals = importlib.import_module('set_values_' + args.experimentName)

f = h5py.File(args.h5File, "r+")

num_runs = np.shape(f['params'])[0]
#num_bins is number of bins in a histogram * number of observables
num_bins = np.shape(f['values'])[0]
for i in range(num_runs):
    params = []
    for j in range(vals.nparams):
        params.append(f['params'][i,j])
    #values of params are constant within each run
    for j in range(num_bins):
        f['errors'][j ,i] = vals.observation_error(f['values'][j,i], params, args.errorType)
f.close()
