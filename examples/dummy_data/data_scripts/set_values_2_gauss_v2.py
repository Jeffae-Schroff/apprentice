import numpy as np
#number of random MC runs
num_folders = 42

#number of points used to generate observable histograms
NPOINTS = 100000
NTARGETPOINTS = 100000

nparams = 2
pnames = ['a', 'b']
obs_names = ['obs1', 'obs2']

#domain/range for observable funcs
x_min = [-1, -1 ]
x_max = [3,  3  ]
y_min = [0,  0  ]
y_max = [1.5,1.5]

#Gaussian functions used
def func1(x, params):
    a, b = params[0], params[1]
    return np.exp(-((x-a)**2/(2*b)**2))

def func2(x, params):
    a, b = params[0], params[1]
    return np.exp(-((x-a)**4/(2*b)**2))
funcs = [func1, func2]
func_strs = ['e^(-(x-a)^2/(2b^2))', 'e^(-(x-a)^4/(2b^2))']

p_min =   [1,    1]
p_max =   [1.1,  5]
nbins =   [10,   5]
targets = [1.05, 3]

#total area of histogram in params' folder
def num_events(params):
    a, b = params[0], params[1]
    #goes from 6 to 18.3
    return 3*(a+b)


def observation_error(x, params, error_type):
    a, b = params[0], params[1]
    #goes from 10-20.4%
    if error_type == "linear":
        return x*2.5*(2 + a + b)/100
    else:
        print("error in observation error in set_value")
    

if not nparams == len(pnames) == len(targets) == len(x_min) == len(x_max)\
               == len(y_min)  == len(y_max)   == len(funcs) == len(p_min) == len(p_max) == len(nbins):
    print("\n\n\nerror in set_experiment_values.py: vals not same length\n\n\n")
