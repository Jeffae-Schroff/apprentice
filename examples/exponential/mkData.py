
import numpy as np
import yoda, random
import os
import apprentice as app

"""
Exponential Distribution
"""

NPOINTS = 100000
n_bins = 20
noise = 20/100 #not implemented
x_min = 0
x_max = 3

a_min = 1
a_max = 2
a_incr = 0.2
b_min = -1.2
b_max = -0.8
b_incr = 0.1

NTARGETPOINTS = 100000
a_target = 1.4
b_target = -1.1

np.random.seed(100)




#exponential functions used
def func1(x, a, b):
    return np.exp(a*x+b*x**2)

def func2(x, a, b):
    return np.exp(a*x+b*x**3)

#writes Histo1D of funcs with given params to .yoda file one subfolder
def make_histos(funcs, a, b, run_num):
    #make subfolder if needed, add usedparams
    folder = str(run_num).zfill(6)
    if not os.path.isdir('MC/' + folder):
        os.mkdir('MC/' + folder)
    file = open('MC/' + folder + '/used_params', 'w')
    file.write('a ' + str(a) + '\n')
    file.write('b ' + str(b))
    file.close()

    #fill each histogram with data from NPOINTS # of xs
    x = x_min + (x_max - x_min) * np.random.random_sample(NPOINTS)
    h = []
    for i in range(len(funcs)):
        h.append(yoda.Histo1D(n_bins, 0.0, 1.0, "func" + str(i)))
        for j in range(NPOINTS):
            h[i].fill(funcs[i](a, b, x[j]))
    yoda.write(h, 'MC/' + folder + '/combined.yoda')

    #add error
    for b in h[0].bins():
        print(help(b))
        print(b.height())
        #b.height = b.height()*(1 + noise*np.random.randn(1))
        print(b.height())
    # for i in range(h.numBins):
    #     b.bin(i).height = b.bin(i).height (1 + noise*np.random.randn(1))

    # for d in h.heights:
    #     d += (1 + noise*np.random.randn(1))

#makes Scatter2D plots for each function with the target parameters
def make_target_scatter(funcs):
    x = x_min + (x_max - x_min) * np.random.random_sample(NTARGETPOINTS)
    s = []
    for i in range(len(funcs)):
        h = yoda.Histo1D(n_bins, 0.0, 1.0, "func" + str(i))
        for j in range(NTARGETPOINTS):
            h.fill(funcs[i](a_target, b_target, x[j]))
        s.append(h.mkScatter())
    
    yoda.write(s, 'Data/' + '/ATLAS_2021_dummy.yoda')




#make MC folder
funcs = [func1, func2]
a = a_min
b = b_min
runNum = 0
while a <= a_max:
    while b <= b_max:
        make_histos(funcs, a, b, runNum)
        b += b_incr
        runNum += 1
    b = b_min
    a += a_incr

#make Data folder
make_target_scatter(funcs)



# app.io.readInputDataYODA("ND", "pnames", None, "input_data.h5")




