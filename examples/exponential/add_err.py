# %%
import h5py
import numpy as np
from mk_data import observation_error
# %%
#TODO:make this a parameter
fname = "inputdata.h5"
f = h5py.File(fname, "r+")
# %%
num_runs = np.shape(f['params'])[0]
for i in range(num_runs):
    #counts bins from all observables put together
    #TODO: check that this doesn't break if num_bins < num_runs
    #TODO change observation error to apply a percentage of the value
    num_bins = np.shape(f['params'])[0]
    for j in range(num_bins):
        f['errors'][j,i] = observation_error(f['values'][j,i], f['params'][i,0], f['params'][i,1])
# %%
f.close()
# %%
