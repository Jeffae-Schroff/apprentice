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
parser.add_argument("filepath", help="place of file with stats", type=str)
parser.add_argument("experimentName", help="2_exp and 2_gauss valid, also name of folder in results to save to", type=str)
parser.add_argument("zoom", help="zoom of graph", type=int)
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

if args.experimentName == '2_exp':
    import set_values_2_exp as vals
elif args.experimentName == '2_gauss':
    import set_values_2_gauss as vals
elif args.experimentName == '2_exp_new_events':
    import set_values_2_exp_new_events as vals
elif args.experimentName == '2_gauss_new_range':
    import set_values_2_gauss_new_range as vals
else:
    print("error with experiment name in param_stats")

params = file_output[0]
tunes = file_output[1:,:]
filtered_tunes = []
boundary = []

for i in range(len(params)):
    boundary_num = 0
    filtered_tune = []
    for j in range(len(tunes[:,i])):
        val = float(tunes[j][i])
        if filter and (val == vals.p_min[i] or val == vals.p_max[i]):
            boundary_num += 1
        else:
            filtered_tune.append(val)
    filtered_tunes.append(filtered_tune)
    boundary.append(boundary_num)


printstr = '\nStats for ' + filename
printstr += '\nParameter'.ljust(20) +'Mean'.ljust(20) + 'Standard Deviation'.ljust(20) + 'Proportion boundary'.ljust(20)
for i in range(len(params)):
    mean = statistics.mean(filtered_tunes[i])
    stdev = statistics.stdev(filtered_tunes[i])
    if filter:
        boundary_proportion = str(boundary[i]/len(tunes[i])).ljust(20)
    else:
        boundary_proportion = "Did not filter"
    printstr += "\n" + params[i].ljust(20) + str(mean).ljust(20) + str(stdev).ljust(20) + boundary_proportion
print(printstr)

f = open(filename + "_stats.txt", "w")
f.write(printstr)
f.close()


# zoom into the graph by this factor
zoom = 1
for i in range(len(params)):
    plt.figure()
    title = filename
    if zoom != 1:
        title += " x" + str(zoom)
    if filter and boundary[i] != 0:
        title += " (" + str(boundary[i]) + " boundary values excluded)"

    target = vals.targets[i]
    span = (vals.p_max[i] - vals.p_min[i]) / zoom
    plot_range = [target - span/2, target + span/2]

    plt.hist(filtered_tunes[i], bins=100, range = plot_range)
    plt.title(title)
    plt.xlabel(params[i] + " value")
    plt.ylabel("Frequency")
    plt.savefig(filename+"_"+params[i]+".pdf")


