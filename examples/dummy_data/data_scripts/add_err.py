# %%
import h5py
import numpy as np
import argparse
# %%
parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("experimentName", help="2_exp and 2_gauss valid, also name of folder in results to save to", type=str)
parser.add_argument("errorType", help="linear, low_linear", type=str)

# Parse arguments
args = parser.parse_args()
if args.experimentName == '2_exp':
    import set_values_2_exp as vals
elif args.experimentName == '2_gauss':
    import set_values_2_gauss as vals
elif args.experimentName == '2_exp_new_events':
    import set_values_2_exp_new_events as vals
elif args.experimentName == '2_gauss_new_range':
    import set_values_2_gauss_new_range as vals
else:
    print("error with experiment name in mk_data")


f = h5py.File("inputdata.h5", "r+")
# %%
num_runs = np.shape(f['params'])[0]
#this is number of bins in a histogram*number of observables
num_bins = np.shape(f['values'])[0]
for i in range(num_runs):
    params = []
    for j in range(vals.nparams):
        params.append(f['params'][i,j])
    #values of params are constant within each run
    for j in range(num_bins):
        f['errors'][j ,i] = vals.observation_error(f['values'][j,i], params, args.errorType)
# %%
f.close()
# %%
