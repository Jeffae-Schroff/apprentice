# %%
import h5py
import numpy as np
from mk_data import observation_error
# %%
#make this a parameter? perhaps not important
f = h5py.File("inputdata.h5", "r+")
# %%
num_runs = np.shape(f['params'])[0]
#this is number of bins in a histogram*number of observables
num_bins = np.shape(f['values'])[0]
for i in range(num_runs):
    this_a = f['params'][i,0]
    this_b = f['params'][i,1]
    #values of params are constant within each run
    for j in range(num_bins):
        f['errors'][j ,i] = observation_error(f['values'][j,i], this_a, this_b)
# %%
f.close()
# %%
