# %%
import h5py
import numpy as np
import set_experiment_values as const
# %%
#make this a parameter? perhaps not important
f = h5py.File("inputdata.h5", "r+")
# %%
num_runs = np.shape(f['params'])[0]
#this is number of bins in a histogram*number of observables
num_bins = np.shape(f['values'])[0]
for i in range(num_runs):
    params = []
    for j in range(const.nparams):
        params.append(f['params'][i,j])
    #values of params are constant within each run
    for j in range(num_bins):
        f['errors'][j ,i] = const.observation_error(f['values'][j,i], params)
# %%
f.close()
# %%
