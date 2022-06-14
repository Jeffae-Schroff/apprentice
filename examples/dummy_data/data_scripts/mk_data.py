# %makes Monte Carlo and target data, in folders MC and Data%
import math
import numpy as np
import yoda
import os, sys
import argparse
from math import ceil
import matplotlib.pyplot as plt
import importlib

"""
Exponential Distribution
"""


parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("experimentName", help="Ex: 2_exp or 2_gauss, determines which set_values to use and name of save folder", type=str)
parser.add_argument("errorType", help="linear, low_linear", type=str)

# Parse arguments
args = parser.parse_args()
print("Running mk_data.py: " + args.experimentName + " observables, " + args.errorType + " error")
vals = importlib.import_module('set_values_' + args.experimentName)

# #saves observable graphs here for transferring to results folder later
# observable_folder = 'many_tunes/observables'

def main():
    os.mkdir('MC/')
    os.mkdir('Data/')

    run_params = np.ndarray([len(vals.funcs), vals.num_folders])
    for i in range(len(vals.funcs)):
        run_params[i,:] = vals.p_min[i] + (vals.p_max[i] - vals.p_min[i])*np.random.rand(vals.num_folders)
    
    
    make_target_scatter(vals.funcs)

    np.random.seed(42) #does this mean param value samples are deterministic?

    every_histo_point = []
    for j in range(vals.num_folders):
        print("mk_data" + str(j+1) + "/" + str(vals.num_folders))
        every_histo_point.append(make_histos(run_params[:,j], j))    
    

#writes Histo1D of funcs with given params to a .yoda file in the subfolder run_num
def make_histos(params, run_num):
    folder = str(run_num).zfill(6)
    os.mkdir('MC/' + folder)
    file = open('MC/' + folder + '/used_params', 'w')
    for i in range(len(vals.pnames)):
        file.write(vals.pnames[i]+' '+str(params[i])+'\n')
    file.close()

    h = []
    all_histo_points = []
    event_weight = vals.num_events(params)/vals.NPOINTS
    #i determines which observable func we are processing
    for i in range(len(vals.funcs)):
        h.append(yoda.Histo1D(vals.nbins[i], vals.x_min[i], vals.x_max[i], "func" + str(i)))
        def sample_func(x):
            return vals.funcs[i](x, params)
        histo_points = function_sample(sample_func, vals.x_min[i],vals.x_max[i],vals.y_min[i], vals.y_max[i],vals.NPOINTS)
        all_histo_points.append(histo_points)

        #since this multiplies the fill, std is the percent obs error
        errors = np.random.normal(1, vals.observation_error(1, params, args.errorType), vals.nbins[i])
        new_weights = []
        for xval in histo_points:
            new_weights.append(event_weight*fill_error(errors, xval, vals.x_min[i], vals.x_max[i]))
            h[i].fill(xval, new_weights[-1])
            
    yoda.write(h, 'MC/' + folder + '/combined.yoda')
    return all_histo_points

#Takes array and number of bins, returns the value in array corresponding to bin's point on range
def fill_error(errors, value, xmin, xmax):
    if value < xmin or value > xmax:
        print("error in fill_error")
    #between 0 and 1
    normal_value = (value-xmin)/(xmax-xmin)
    return errors[math.floor(normal_value*len(errors))]

#Return points from a uniformly distribution bounded by ([xmin, xmax], [ymin, ymax]) beneath the given function.
def function_sample(func, xmin, xmax, ymin, ymax, num_points):
    sample = []
    batchsize = ceil(num_points)
    # generates batches of points at a time and checks if y is under func(x)
    while len(sample) < num_points:
        x = np.random.rand(batchsize)
        y = np.random.rand(batchsize)
        x = xmin + (xmax - xmin)*x
        y = ymin + (ymax - ymin)*y
        new_sample = [xval for (xval,yval) in  zip(x,y) if func(xval) > yval]

        if len(new_sample) < 0.01 * batchsize:
            print("low yield of points under func in mk_data:function_sample")
        sample = sample + new_sample

    return sample[:num_points]


#makes Scatter2D plots for each function with the target parameters
def make_target_scatter(funcs):
    s = []
    event_weight = vals.num_events(vals.targets)/vals.NTARGETPOINTS
    for i in range(len(funcs)):
        h = yoda.Histo1D(vals.nbins[i], vals.x_min[i], vals.x_max[i], "func" + str(i))
        def sample_func(x):
            return vals.funcs[i](x, vals.targets)
        histo_points = function_sample(sample_func, vals.x_min[i],vals.x_max[i],vals.y_min[i],vals.y_max[i],vals.NTARGETPOINTS)
        for xval in histo_points:
            h.fill(xval, event_weight)
        s.append(h.mkScatter())
    yoda.write(s, 'Data/ATLAS_dummy.yoda')

if __name__ == '__main__':
    main()

