from socket import IP_DEFAULT_MULTICAST_TTL
import sys
import os
import importlib
import numpy as np
import statistics
import matplotlib.pyplot as plt
#prints stats of given file in many_tunes
#assumes first row is names of parameters, rest are values in columns
#Also generates histograms
import argparse
# %%
parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("filepath", help="place of file with collected tune results", type=str)
parser.add_argument("experimentName", help="2_exp and 2_gauss valid, also name of folder in results to save to", type=str)
parser.add_argument("zoom", help="zoom of graph", type=int)
# parser.add_argument("errorType", help="linear, low_linear", type=str)

# Parse arguments
args = parser.parse_args()

#filter out boundary values or not
filter = True

vals = importlib.import_module('set_values_' + args.experimentName)

if(not os.path.exists(args.filepath)):
    print('file given to param_stats.py does not exist')
filename = args.filepath.split('/')[-1]
file_lines = open(args.filepath, 'r').readlines()
# Using np array, not list to pull columns easier
file_output = np.array([f.split(',') for f in file_lines])



params = file_output[0,:-2]
tunes = file_output[1:,:-2]
is_boundary = file_output[1:,-2]
chi2 = file_output[1:,-1]
filtered_tunes = []
boundary_num = 0

#i is number of runs in file
for i in range(np.shape(tunes)[0]):
    if is_boundary[i] == 'True':
        boundary_num += 1
    else:
        filtered_tunes.append(tunes[i])

printstr = '\nStats for ' + filename
printstr += '\nParameter'.ljust(20) +'Mean'.ljust(20) + 'Standard Deviation'.ljust(20) + 'Proportion boundary'.ljust(20)
for i in range(len(params)):
    mean = statistics.mean([float(row[i]) for row in tunes])
    stdev = statistics.stdev([float(row[i]) for row in tunes])
    printstr += "\n" + params[i].ljust(20) + str(round(mean,10)).ljust(20) + str(round(stdev,10)).ljust(20)  + "Did not filter"
printstr += '\nONBOUND filtered stats for ' + filename
printstr += '\nParameter'.ljust(20) +'Mean'.ljust(20) + 'Standard Deviation'.ljust(20) + 'Proportion boundary'.ljust(20)
for i in range(len(params)):
    mean = statistics.mean([float(row[i]) for row in filtered_tunes])
    stdev = statistics.stdev([float(row[i]) for row in filtered_tunes])
    boundary_proportion = str(boundary_num/np.shape(tunes)[0]).ljust(20)
    printstr += "\n" + params[i].ljust(20) + str(round(mean,10)).ljust(20)  + str(round(stdev,10)).ljust(20)  + boundary_proportion

print(printstr)

f = open("results/stats/" + filename.split('.')[0] + "_stats.txt", "w")
f.write(printstr)
f.close()


# zoom into the graph by this factor
zoom = 1
for i in range(len(params)):
    plt.figure()
    title = filename.split('.')[0]
    if zoom != 1:
        title += " x" + str(zoom)

    target = vals.targets[i]
    span = (vals.p_max[i] - vals.p_min[i]) / zoom
    plot_range = [target - span/2, target + span/2]

    plt.hist([float(row[i]) for row in tunes], bins=100, range = plot_range)
    plt.title(title)
    plt.xlabel(params[i] + " value")
    plt.ylabel("Frequency")
    plt.savefig("results/many_tunes_histos/"+filename.split('.')[0]+"_"+params[i]+".pdf")


