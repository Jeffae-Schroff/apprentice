# %makes MC and target data, saves observable histograms to many_tunes%
import numpy as np
import yoda
import os
import argparse
import shutil

"""
Exponential Distribution
"""

from math import ceil
import matplotlib.pyplot as plt
import set_run_vals as run_vals

parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("experimentName", help="2_exp and 2_gauss valid, also name of folder in results to save to", type=str)
parser.add_argument("errorType", help="linear, low_linear", type=str)
parser.add_argument("npoints", help="number of points used in observable graphs", type=float)

# Parse arguments
args = parser.parse_args()
print("Running " + args.experimentName + " with " + args.errorType)
if args.experimentName == '2_exp':
    import set_values_2_exp as vals
elif args.experimentName == '2_gauss':
    import set_values_2_gauss as vals
elif args.experimentName == '2_exp_new_events':
    import set_values_2_exp_new_events as vals
elif args.experimentName == '2_gauss_new_range':
    import set_values_2_gauss_new_range as vals
else:
    print("error with experiment name in mk_data")
NPOINTS = int(args.npoints)
NTARGETPOINTS = int(args.npoints)

#saves observable graphs here for transferring to results folder later
observable_folder = 'many_tunes/observables'

def main():
    if(os.path.isdir('MC')):
        shutil.rmtree('MC') 
    os.mkdir('MC/')
    if(os.path.isdir('Data')):
        shutil.rmtree('Data') 
    os.mkdir('Data/')
    if(os.path.isdir(observable_folder)):
        shutil.rmtree(observable_folder) 
    os.mkdir(observable_folder)
    os.mkdir(observable_folder+"/MC")
    os.mkdir(observable_folder+"/target")


    run_params = np.ndarray([len(vals.funcs), run_vals.num_folders])
    for i in range(len(vals.funcs)):
        run_params[i,:] = vals.p_min[i] + (vals.p_max[i] - vals.p_min[i])*np.random.rand(run_vals.num_folders)
    
    plot_envelope(run_params)
    make_target_scatter(vals.funcs)

    np.random.seed(42) #does this mean param value samples are deterministic?

    for j in range(run_vals.num_folders):
        print("mk_data" + str(j) + "/" + str(run_vals.num_folders))
        make_histos(run_params[:,j], j)

    
    

#writes Histo1D of funcs with given params to a .yoda file in the subfolder run_num
def make_histos(params, run_num):
    folder = str(run_num).zfill(6)
    os.mkdir('MC/' + folder)
    file = open('MC/' + folder + '/used_params', 'w')
    for i in range(len(vals.pnames)):
        file.write(vals.pnames[i]+' '+str(params[i])+'\n')
    file.close()

    h = []
    event_weight = vals.num_events(params)/NPOINTS
    #i determines which observable func we are processing
    for i in range(len(vals.funcs)):
        h.append(yoda.Histo1D(run_vals.nbins, vals.x_min[i], vals.x_max[i], "func" + str(i)))
        def sample_func(x):
            return vals.funcs[i](x, params)
        histo_points = function_sample(sample_func, vals.x_min[i],vals.x_max[i],vals.y_min[i], vals.y_max[i],NPOINTS)
        for xval in histo_points:
            h[i].fill(xval, event_weight)

        #plot observable histogram to observable folder in many_tunes where it will be saved to results by another script
        plt.hist(histo_points, bins=run_vals.nbins, range=[vals.x_min[i], vals.x_max[i]], weights = [event_weight]*len(histo_points))
        plt.title(args.experimentName + ' observable function: ' + vals.func_strs[i])
        plt.xlabel("x")
        plt.ylabel("Number of Events")
        for j in range(len(vals.pnames)):
            plt.annotate(vals.pnames[j] + '=' + str(round(params[j],3)), xy=(0.85, 1-0.05*(1+j)), xycoords='axes fraction')
        figStr = '_'.join([vals.pnames[j] + '=' + str(round(params[j],2)) for j in range(len(vals.pnames))])
        plt.savefig(observable_folder + '/MC/obs' + str(i) + '--' + figStr + ".pdf")
        plt.close()
            
    yoda.write(h, 'MC/' + folder + '/combined.yoda')

#Return points from a uniformly distribution beneath the given function bounded by ([xmin, xmax], [ymin, ymax]).
def function_sample(func, xmin, xmax, ymin, ymax, num_points):
    sample = []
    batchsize = ceil(num_points)
    # generates batches of points at a time and checks if y is under func(x)
    while len(sample) < num_points:
        x = np.random.rand(batchsize)
        y = np.random.rand(batchsize)
        x = xmin + (xmax - xmin)*x
        y = ymin + (ymax - ymin)*y
        new_sample = [xval for (xval,yval) in  zip(x,y) if func(xval) > yval]

        if len(new_sample) < 0.01 * batchsize:
            print("low yield of points under func in mk_data:function_sample")
        sample = sample + new_sample

    return sample[:num_points]


#makes Scatter2D plots for each function with the target parameters
def make_target_scatter(funcs):
    s = []
    event_weight = vals.num_events(vals.targets)/NTARGETPOINTS
    for i in range(len(funcs)):
        h = yoda.Histo1D(run_vals.nbins, vals.x_min[i], vals.x_max[i], "func" + str(i))
        def sample_func(x):
            return vals.funcs[i](x, vals.targets)
        histo_points = function_sample(sample_func, vals.x_min[i],vals.x_max[i],vals.y_min[i],vals.y_max[i],NTARGETPOINTS)
        for xval in histo_points:
            h.fill(xval, event_weight)

        plt.hist(histo_points, bins=run_vals.nbins, range=[vals.x_min[i], vals.x_max[i]], weights = [event_weight]*len(histo_points))
        plt.title(args.experimentName + ' observable function: ' + vals.func_strs[i])
        plt.xlabel("x")
        plt.ylabel("Number of Events")
        for j in range(len(vals.pnames)):              #below changed from MC graph code
            plt.annotate(vals.pnames[j] + '=' + str(round(vals.targets[j],3)), xy=(0.85, 1-0.05*(1+j)), xycoords='axes fraction')
        figStr = '_'.join([vals.pnames[j] + '=' + str(round(vals.targets[j],2)) for j in range(len(vals.pnames))])
        plt.savefig(observable_folder + '/target/obs' + str(i) + '--' + figStr + ".pdf")
        plt.close()

        s.append(h.mkScatter())
    yoda.write(s, 'Data/' + '/ATLAS_2021_dummy.yoda')

def plot_envelope(run_params):
    for i in range(len(vals.funcs)):
        num_x = 100
        x = [j/num_x for j in range(num_x*vals.x_min[i], num_x*vals.x_max[i])]
        for j in range(run_vals.num_folders):
            def obs_with_param(x):
                return vals.funcs[i](x, run_params[:,j])
            
            y = [obs_with_param(k) for k in x]
            #color based on first two params
            norm_param_1 = (run_params[0,j]-vals.p_min[0])/(vals.p_max[0]-vals.p_min[0])
            norm_param_2 = (run_params[1,j]-vals.p_min[1])/(vals.p_max[1]-vals.p_min[1])
            param_color = (0.25 + 0.75*norm_param_1, 0.25, 1 - 0.75*norm_param_1, 1 - 0.75*norm_param_2)
            plt.plot(x, y, linestyle="-", color = param_color)
        
        plt.xlim(vals.x_min[i], vals.x_max[i])
        plt.ylim(vals.y_min[i], vals.y_max[i]) 
        plt.title(args.experimentName + ' observable function: ' + vals.func_strs[i])
        plt.annotate(vals.pnames[0] + ': red to blue', xy=(0.68, 0.95), xycoords='axes fraction')
        plt.annotate(vals.pnames[1] +': opacity (low to high)', xy=(0.68, 0.9), xycoords='axes fraction')
        plt.savefig(observable_folder + '/obs' + str(i) + ".pdf")
        plt.close()
    

if __name__ == '__main__':
    main()

