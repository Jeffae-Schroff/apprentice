import sys
import os
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
parser.add_argument("filepath", help="folder with stats", type=str)
parser.add_argument("experimentName", help="2_exp and 2_gauss valid, also name of folder in results to save to", type=str)
# parser.add_argument("errorType", help="linear, low_linear", type=str)

# Parse arguments
args = parser.parse_args()

#filter out boundary values or not
filter = True

if(not os.path.exists(args.filepath)):
    print('file given to param_stats.py does not exist')
filename = args.filepath.split('/')[-1]
file_lines = open(args.filepath, 'r').readlines()
# Using np array, not list to pull columns easier
file_output = np.array([f.split() for f in file_lines])

if args.experimentName == "2_exp":
    import set_values_2_exp as const
elif args.experimentName == "2_gauss":
    import set_values_2_gauss as const
else:
    print("error with experiment name in mk_data")

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


