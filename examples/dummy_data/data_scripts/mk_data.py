# %%
import numpy as np
import yoda
import os
import shutil
"""
Exponential Distribution
"""
#pnames only implemented for inputdata_gen_params
pnames = ['a', 'b']
NPOINTS = 100000
NTARGETPOINTS = 100000
a_target = 1.5
b_target = -1
n_bins = 20
#print("Target: a = "+str(a_target)+", b = "+str(b_target))


#domain/range for
#observable funcs
x_min = [0,0]
x_max = [3,3]
y_min = [0,0]
y_max = [4,4]

# # Parameter values for MC
a_min = 1
a_max = 2
a_incr = 0.2
b_min = -1.2
b_max = -0.8
b_incr = 0.4/6

np.random.seed()

#exponential functions used
def func1(x, a, b):
    return np.exp(a*x+b*x**2)

def func2(x, a, b):
    return np.exp(a*x+b*x**3)

def num_events(a, b):
    return 20-5*a

#a-b goes from 1.8 to 3.4
def observation_error(x, a, b):
    return x*10*(a - b)/100

#Write generation data to file

def main():
    #make MC folder
    if(os.path.isdir('MC')):
        shutil.rmtree('MC') 
    os.mkdir('MC/')

    funcs = [func1, func2]
    a = a_min
    b = b_min
    runNum = 0
    while a <= a_max + 0.00001: #fix floating point errors
        while b <= b_max + 0.00001:
            make_histos(funcs, a, b, runNum)
            b += b_incr
            runNum += 1
        b = b_min
        a += a_incr

    #make Data folder
    make_target_scatter(funcs)


#writes Histo1D of funcs with given params to .yoda file one subfolder
def make_histos(funcs, a, b, run_num):
    folder = str(run_num).zfill(6)
    os.mkdir('MC/' + folder)
    file = open('MC/' + folder + '/used_params', 'w')
    file.write('a ' + str(a) + '\n')
    file.write('b ' + str(b))
    file.close()

    #histogram from exponential
    h = []
    event_weight = num_events(a, b)/NPOINTS
    for i in range(len(funcs)):
        h.append(yoda.Histo1D(n_bins, y_min[i], y_max[i], "func" + str(i)))
        #fill each histogram with data from NPOINTS # of xs
        x = x_min[i] + (x_max[i] - x_min[i]) * np.random.random_sample(NPOINTS)
        y = funcs[i](x, a, b)
        for j in range(NPOINTS):
            h[i].fill(y[j], event_weight)
        
    yoda.write(h, 'MC/' + folder + '/combined.yoda')

#makes Scatter2D plots for each function with the target parameters
def make_target_scatter(funcs):
    s = []
    event_weight = num_events(a_target, b_target)/NTARGETPOINTS
    for i in range(len(funcs)):
        h = yoda.Histo1D(n_bins, y_min[i], y_max[i], "func" + str(i))
        x = x_min[i] + (x_max[i] - x_min[i]) * np.random.random_sample(NTARGETPOINTS)
        y = funcs[i](x, a_target, b_target)
        for j in range(NTARGETPOINTS):
            h.fill(y[j], event_weight)
        s.append(h.mkScatter())
    
    yoda.write(s, 'Data/' + '/ATLAS_2021_dummy.yoda')




if __name__ == '__main__':
    main()
# %%
