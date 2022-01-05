import sys
import os
import numpy as np
import statistics
import matplotlib.pyplot as plt
#prints stats of given file in many_tunes
#assumes first row is names of parameters, rest are values in columns
#Also generates histograms
#Urgh, range has to be hardcoded, maybe fix later
#filter out boundary values
filter = False

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

param_range = [(1,2), (-1.2, -0.8)] #TODO: read from file instead of hardcode uggh probably means changing format too
vals = []
filtered_vals = []
boundary= []
for i in range(len(params)):
    vals.append(file_output[1:,i].astype(np.float))
    boundary_num = 0
    filtered_val = []
    for j in range(len(vals[i])):
        if filter and (vals[i][j] == param_range[i][0] or vals[i][j] == param_range[i][0]):
            boundary_num += 1
        else:
            filtered_val.append(vals[i][j])
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



for i in range(len(params)):
    plt.figure()
    title = filename
    if filter:
        title += " (" + str(boundary[i]) + " boundary values excluded)"
    
    plt.hist(filtered_vals[i], bins=30, range = param_range[i])
    plt.title(title)
    plt.xlabel(params[i] + " value")
    plt.ylabel("Frequency")
    plt.savefig(filename+"_"+params[i]+".pdf")


