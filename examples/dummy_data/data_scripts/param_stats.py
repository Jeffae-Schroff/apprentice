import sys
import os
import numpy as np
import statistics
import matplotlib.pyplot as plt
import examples.dummy_data.data_scripts.set_experiment_values_gauss as const
#prints stats of given file in many_tunes
#assumes first row is names of parameters, rest are values in columns
#Also generates histograms

#filter out boundary values or not
filter = True

if len(sys.argv) != 2 :
    print('invalid arguments to gather_data.py')

filepath = sys.argv[1]
if(not os.path.exists(filepath)):
    print('file given to param_stats.py does not exist')

filename = filepath.split('/')[-1]
file_lines = open(filepath, 'r').readlines()
# Using np array, not list to pull columns easier
file_output = np.array([f.split() for f in file_lines])

params = file_output[0]
vals = file_output[1:,:]
filtered_vals = []
boundary = []

for i in range(len(params)):
    boundary_num = 0
    filtered_val = []
    for j in range(len(vals[:,i])):
        val = float(vals[j][i])
        if filter and (val == const.p_min[i] or val == const.p_max[i]):
            boundary_num += 1
        else:
            filtered_val.append(val)
    filtered_vals.append(filtered_val)
    boundary.append(boundary_num)


print('\nStats for ', filename)
print('Parameter'.ljust(20),'Mean'.ljust(20),'Standard Deviation'.ljust(20), 'Proportion boundary'.ljust(20))
for i in range(len(params)):
    mean = statistics.mean(filtered_vals[i])
    stdev = statistics.stdev(filtered_vals[i])
    if filter:
        boundary_proportion = str(boundary[i]/len(vals[i])).ljust(20)
    else:
        boundary_proportion = "Did not filter"
    print(params[i].ljust(20), str(mean).ljust(20), str(stdev).ljust(20), boundary_proportion)

# zoom into the graph by this factor
zoom = 1
for i in range(len(params)):
    plt.figure()
    title = filename
    if zoom != 1:
        title += " x" + str(zoom)
    if filter and boundary[i] != 0:
        title += " (" + str(boundary[i]) + " boundary values excluded)"

    target = const.targets[i]
    span = (const.p_max[i] - const.p_min[i]) / zoom
    plot_range = [target - span/2, target + span/2]

    plt.hist(filtered_vals[i], bins=100, range = plot_range)
    plt.title(title)
    plt.xlabel(params[i] + " value")
    plt.ylabel("Frequency")
    plt.savefig(filename+"_"+params[i]+".pdf")


