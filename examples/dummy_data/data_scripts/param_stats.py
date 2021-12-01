import sys
import os
import numpy as np
import statistics
#prints stats of given file in many_tunes

if len(sys.argv) != 2 :
    print('invalid arguments to gather_data.py')

filename = sys.argv[1]
if(not os.path.exists("many_tunes/"+filename)):
    print('file given to oaram_stats.py does not exist')

file_output = open("many_tunes/"+filename, 'r').readlines()
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


