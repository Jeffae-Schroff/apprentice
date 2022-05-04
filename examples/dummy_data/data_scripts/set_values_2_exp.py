import numpy as np
nparams = 2
pnames = ['a', 'b']

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
funcs = [func1, func2]
func_strs = ['e^(ax+bx^2)', 'e^(ax+bx^3)']

p_min = [1,-1.2]
p_max = [2,-0.8]
targets = [1.5, -1]

#used for normalization--total area under curve for MC run
def num_events(params):
    a, b = params[0], params[1]
    return 20-5*(a-b)

def observation_error(x, params, error_type):
    a, b = params[0], params[1]
    #error goes from 0.9 to 1.6 %
    if error_type == "low_linear":
        return x*0.5*(a - b)/100
    #error goes from 9 to 16 %
    elif error_type == "linear":
        return x*5*(a - b)/100
    else:
        print("error in observation error in set_value")

if not nparams == len(pnames) == len(targets) == len(x_min) == len(x_max) == len(y_min) == len(y_max) == len(funcs) == len(p_min) == len(p_max):
    print("\n\n\nerror in set_experiment_values.py: vals not same length\n\n\n")
