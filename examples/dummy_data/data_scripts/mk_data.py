# %%
import numpy as np
import yoda
import os
import shutil
import set_experiment_values as vals
"""
Exponential Distribution
"""


#Write generation data to file

def main():
    if(os.path.isdir('MC')):
        shutil.rmtree('MC') 
    os.mkdir('MC/')
    if(os.path.isdir('Data')):
        shutil.rmtree('Data') 
    os.mkdir('Data/')

    np.random.seed(42) #Change this to pick different param value samples
    run_params = np.ndarray([len(vals.funcs), vals.num_folders])
    for i in range(len(vals.funcs)):
        run_params[i,:] = vals.p_min[i] + (vals.p_max[i] - vals.p_min[i])*np.random.rand(vals.num_folders)
    for j in range(vals.num_folders):
        print("mk_data" + str(j) + "/" + str(vals.num_folders))
        make_histos(run_params[:,j], j)
    make_target_scatter(vals.funcs)

#writes Histo1D of funcs with given params to a .yoda file in the subfolder run_num
def make_histos(params, run_num):
    folder = str(run_num).zfill(6)
    os.mkdir('MC/' + folder)
    file = open('MC/' + folder + '/used_params', 'w')
    for i in range(len(vals.pnames)):
        file.write(vals.pnames[i]+' '+str(params[i])+'\n')
    file.close()

    h = []
    event_weight = vals.num_events(params)/vals.NPOINTS
    for i in range(len(vals.funcs)):
        h.append(yoda.Histo1D(vals.nbins, vals.x_min[i], vals.x_max[i], "func" + str(i)))
        def sample_func(x):
            return vals.funcs[i](x, params)
        histo_points = function_sample(sample_func, vals.x_min[i],vals.x_max[i],vals.y_min[i], vals.y_max[i],vals.NPOINTS)
        for xval in histo_points:
            h[i].fill(xval, event_weight)
        
    yoda.write(h, 'MC/' + folder + '/combined.yoda')

from itertools import compress
from math import ceil
import matplotlib.pyplot as plt
import time

#Return points from a uniformly distribution beneath the given function bounded by ([xmin, xmax], [ymin, ymax]).
def function_sample(func, xmin, xmax, ymin, ymax, npoints):
    sample = []
    batchsize = ceil(npoints)
    # generates batches of points at a time and checks if they are under
    while len(sample) < npoints:
        x = np.random.rand(batchsize)
        y = np.random.rand(batchsize)
        x = xmin + (xmax - xmin)*x
        y = ymin + (ymax - ymin)*y
        new_sample = [xval for (xval,yval) in  zip(x,y) if func(xval) > yval]

        if len(new_sample) < 0.01 * batchsize:
            print("low yield of points under func in mk_data:function_sample")
        sample = sample + new_sample
    # plt.hist(sample, bins=100, range = [xmin,xmax])
    # plt.title(str(params[0]) + " " + str(params[1]))
    # plt.savefig(time.ctime(time.time())+".pdf")
    # plt.close()

    return sample[:npoints]


#makes Scatter2D plots for each function with the target parameters
def make_target_scatter(funcs):
    s = []
    event_weight = vals.num_events(vals.targets)/vals.NTARGETPOINTS
    for i in range(len(funcs)):
        h = yoda.Histo1D(vals.nbins, vals.x_min[i], vals.x_max[i], "func" + str(i))
        def sample_func(x):
            return vals.funcs[i](x, vals.targets)
        histo_points = function_sample(sample_func, vals.x_min[i],vals.x_max[i],vals.y_min[i],vals.y_max[i],vals.NTARGETPOINTS)
        for xval in histo_points:
            h.fill(xval, event_weight)
        s.append(h.mkScatter())
    
    yoda.write(s, 'Data/' + '/ATLAS_2021_dummy.yoda')

if __name__ == '__main__':
    main()
# %%
