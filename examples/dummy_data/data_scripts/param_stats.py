import sys
import os
import numpy as np
import statistics
import matplotlib.pyplot as plt
#prints stats of given file in many_tunes

if len(sys.argv) != 2 :
    print('invalid arguments to gather_data.py')

filepath = sys.argv[1]
if(not os.path.exists(filepath)):
    print('file given to oaram_stats.py does not exist')

filename = filepath.split('/')[-1]
file_output = open(filepath, 'r').readlines()
file_output = np.array([f.split() for f in file_output])

params = file_output[0]

vals = []
for i in range(len(params)):
    vals.append(file_output[1:,i].astype(np.float))

print('\nStats for ', filename)
print('Parameter'.ljust(20),'Mean'.ljust(20),'Standard Deviation')
for i in range(len(params)):
    mean = statistics.mean(vals[i])
    stdev = statistics.stdev(vals[i])
    print(params[i].ljust(20), str(mean).ljust(20), str(stdev).ljust(20))
print()


for i in range(len(params)):
    
    plt.figure()
    plt.hist(vals[i], bins=30)
    plt.title(filename)
    plt.xlabel(params[i] + " value")
    plt.ylabel("Frequency")
    plt.savefig(filename+"_"+params[i]+".pdf")


