import numpy as np
#number of MC runs
num_folders = 42

#number of points used to generate observable histograms
NPOINTS = 100000
NTARGETPOINTS = 100000

#parameters to go into observables
nparams = 2
pnames = ['a', 'b']

#domain/range for observable funcs: obs1 has domain/range [x_min[0],x_max[0]] --> [y_min[0],y_max[0]], etc.
x_min = [0,0]
x_max = [3,3]
y_min = [0,0]
y_max = [4,4]
# Number of bins to sort observable data into
nbins =  [20, 20]

#observable functions (exponential in this case)
def func1(x, params):
    a, b = params[0], params[1]
    return np.exp(a*x+b*x**2)
def func2(x, params):
    a, b = params[0], params[1]
    return np.exp(a*x+b*x**3)

funcs = [func1, func2]
func_strs = ['e^(ax+bx^2)', 'e^(ax+bx^3)']
obs_names = ['obs1', 'obs2']

# The range over which params will vary when making the MC runs. 
# Every one of the num_folder MC runs has params randomly sampled from this range.
p_min =  [1,  -1.2]
p_max =  [2,  -0.8]
# The parameter values used to make the mock data/target,
# may lead to worse results if they are close to the edge of param range. 
targets =[1.5,-1  ]

#used for normalization--total area under curve for MC run
def num_events(params):
    a, b = params[0], params[1]
    return 20-5*(a-b)

# This will be added per bin to the MC runs.
def observation_error(x, params, error_type):
    a, b = params[0], params[1]
    #error goes from 0.9 to 1.6 %
    if error_type == "low_linear":
        return x*0.5*(a - b)/100
    #error goes from 9 to 16 %
    elif error_type == "linear":
        return x*5*(a - b)/100
    #error goes from 0 to ~30%
    elif error_type == "log":
        return -0.2*a*b*np.log(x)
    else:
        print("error in observation error in set_value")
        
if not (nparams == len(pnames) == len(targets) == len(p_min) == len(p_max)  and \
    len(x_min) == len(x_max)  == len(y_min)  == len(y_max)  == len(funcs) == len(nbins)):
    print("\n\n\nerror in set_experiment_values.py: vals not same length\n\n\n")
