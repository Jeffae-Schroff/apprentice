import numpy as np

pnames = ['a', 'b']
NPOINTS = 100000
NTARGETPOINTS = 100000
targets = [1.5, -1]
n_bins = 20

#domain/range for observable funcs
x_min = [0,0]
x_max = [3,3]
y_min = [0,0]
y_max = [4,4]

#exponential functions used
def func1(x, params):
    a, b = params[0], params[1]
    return np.exp(a*x+b*x**2)

def func2(x, params):
    a, b = params[0], params[1]
    return np.exp(a*x+b*x**3)

num_folders = 42
funcs = [func1, func2]
p_min = [1,-1.2]
p_max = [2,-0.8]

#total area of histogram in params' folder
def num_events(params):
    return 20-5*params[0]

#goes from 18-34%
def observation_error(x, a, b):
    return x*10*(a - b)/100

if not len(pnames) == len(targets) == len(x_min) == len(x_max) == len(y_min) == len(y_max) == len(funcs) == len(p_min) == len(p_max):
    print("error in set_experiment_values.py: vals not same length")
