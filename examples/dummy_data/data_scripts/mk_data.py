# %%
import numpy as np
import yoda
import os
import shutil
import set_experiment_values as vals
"""
Exponential Distribution
"""


#Write generation data to file

def main():
    if(os.path.isdir('MC')):
        shutil.rmtree('MC') 
    os.mkdir('MC/')
    if(os.path.isdir('Data')):
        shutil.rmtree('Data') 
    os.mkdir('Data/')

    np.random.seed(42) #Change this to pick different param value samples
    run_params = np.ndarray([len(vals.funcs), vals.num_folders])
    for i in range(len(vals.funcs)):
        run_params[i,:] = vals.p_min[i] + (vals.p_max[i] - vals.p_min[i])*np.random.rand(vals.num_folders)
    for j in range(vals.num_folders):
        make_histos(run_params[:,j], j)

    # funcs = [vals.func1, vals.func2]
    # a = vals.a_min
    # b = vals.b_min
    # runNum = 0
    # while a <= vals.a_max + 0.00001: #fix floating point errors
    #     while b <= vals.b_max + 0.00001:
    #         make_histos(funcs, [a, b], runNum)
    #         b += vals.b_incr
    #         runNum += 1
    #     b = vals.b_min
    #     a += vals.a_incr

    #make Data folder
    make_target_scatter(vals.funcs)


#writes Histo1D of funcs with given params to .yoda file one subfolder
def make_histos(params, run_num):
    folder = str(run_num).zfill(6)
    os.mkdir('MC/' + folder)
    file = open('MC/' + folder + '/used_params', 'w')
    for i in range(len(vals.pnames)):
        file.write(vals.pnames[i]+' '+str(params[i])+'\n')
    file.close()

    #histogram from exponential
    h = []
    event_weight = vals.num_events(params)/vals.NPOINTS
    for i in range(len(vals.funcs)):
        h.append(yoda.Histo1D(vals.n_bins, vals.y_min[i], vals.y_max[i], "func" + str(i)))
        #fill each histogram with data from NPOINTS # of xs
        x = vals.x_min[i] + (vals.x_max[i] - vals.x_min[i]) * np.random.random_sample(vals.NPOINTS)
        y = vals.funcs[i](x, params)
        for j in range(vals.NPOINTS):
            h[i].fill(y[j], event_weight)
        
    yoda.write(h, 'MC/' + folder + '/combined.yoda')

#makes Scatter2D plots for each function with the target parameters
def make_target_scatter(funcs):
    s = []
    event_weight = vals.num_events(vals.targets)/vals.NTARGETPOINTS
    for i in range(len(funcs)):
        h = yoda.Histo1D(vals.n_bins, vals.y_min[i], vals.y_max[i], "func" + str(i))
        x = vals.x_min[i] + (vals.x_max[i] - vals.x_min[i]) * np.random.random_sample(vals.NTARGETPOINTS)
        y = funcs[i](x, vals.targets)
        for j in range(vals.NTARGETPOINTS):
            h.fill(y[j], event_weight)
        s.append(h.mkScatter())
    
    yoda.write(s, 'Data/' + '/ATLAS_2021_dummy.yoda')




if __name__ == '__main__':
    main()
# %%
