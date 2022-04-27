import numpy as np

nparams = 2
pnames = ['a', 'b']
NPOINTS = 100000
NTARGETPOINTS = 100000
targets = [1, 0.5]
nbins = 20

#domain/range for observable funcs
x_min = [-2 ,-3]
x_max = [4  ,5]
y_min = [0  ,0]
y_max = [1.5,1.5]

#Gaussian functions used
def func1(x, params):
    a, b = params[0], params[1]
    return np.exp(-((x-a)**2/(2*b)**2))

def func2(x, params):
    a, b = params[0], params[1]
    return np.exp(-((x-a)**4/(2*b)**2))

num_folders = 42
funcs = [func1, func2]
p_min = [0    ,0.1]
p_max = [2    ,1]

#total area of histogram in params' folder
def num_events(params):
    a, b = params[0], params[1]
    return 20-5*(a+b)

#goes from 9.3-18%
def observation_error(x, params):
    a, b = params[0], params[1]
    return x*3*(3 + a + b)/100

if not nparams == len(pnames) == len(targets) == len(x_min) == len(x_max) == len(y_min) == len(y_max) == len(funcs) == len(p_min) == len(p_max):
    print("\n\n\nerror in set_experiment_values.py: vals not same length\n\n\n")
