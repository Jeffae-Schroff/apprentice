import numpy as np
nparams = 2
pnames = ['a', 'b']

#domain/range for observable funcs
x_min = [-1 ,-1]
x_max = [3  ,3]
y_min = [0  ,0]
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

p_min = [0    ,0.5]
p_max = [2    ,1.5]
targets = [1  ,1]

#total area of histogram in params' folder
def num_events(params):
    a, b = params[0], params[1]
    return 20-5*(a+b)


def observation_error(x, params, error_type):
    a, b = params[0], params[1]
    #goes from 0.93-1.8%
    if error_type == "low_linear":
        return x*0.3*(3 + a + b)/100
    #goes from 9.3-18%
    elif error_type == "linear":
        return x*3*(3 + a + b)/100
    else:
        print("error in observation error in set_value")
    

if not nparams == len(pnames) == len(targets) == len(x_min) == len(x_max) == len(y_min) == len(y_max) == len(funcs) == len(p_min) == len(p_max):
    print("\n\n\nerror in set_experiment_values.py: vals not same length\n\n\n")
