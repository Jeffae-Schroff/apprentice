#!/usr/bin/env python
import codecs
import importlib
from itertools import cycle
from math import atan2
from matplotlib import colors
import math
import os
import json
import numpy as np
import matplotlib.patches
import matplotlib.pyplot as plt
import pandas as pd

from apprentice.appset import TuningObjective2
from apprentice.appset import TuningObjective3
from scipy.stats import chi2 as chi2pdf


def readReport(fname):
    """
    Read a pyoo report and extract data for plotting
    """
    with open(fname) as f:
        D=json.load(f)


    # First, find the chain with the best objective
    c_win =""
    y_win = np.inf
    for chain, rep in D.items():
        _y = np.min(rep["Y_outer"])
        if _y is None:
            c_win = chain
            y_win = _y
        elif _y < y_win:
            c_win=chain
            y_win = _y

    i_win = np.argmin(D[c_win]["Y_outer"])
    print(len(D[c_win]["X_outer"]), i_win)
    wmin = D[c_win]["X_outer"][i_win]
    if type(wmin[0]) is list:
        wmin = wmin[0]

    if type(D[c_win]["binids"][0]) is list:
        binids = D[c_win]["binids"][0]
    else:
        binids = D[c_win]["binids"]
    pmin = D[c_win]["X_inner"][i_win]
    pnames = D[c_win]["pnames_inner"]
    hnames = D[c_win]["pnames_outer"]

    # print(c_win)
    # print(len(D[c_win]['Y_outer']))
    # print(len(D[c_win]["X_inner"]))
    print("# of generator parameters:", len(pnames))
    print("# of observables:", len(hnames))
    print("# of bins:", len(binids))
    print("# of weights:", len(wmin))
    # print(binids)

    return {"x":pmin, "binids":binids, "pnames":pnames, "hnames":hnames,'weights':wmin}

def mk_json(tune_type, offbound_num):
    

    json_data = {'chain-0':{}}
    D = json_data['chain-0']
    D['pnames_inner'] = vals.pnames
    D['pnames_outer'] = vals.obs_names

    df = pd.read_csv('results/many_tunes/'+tune_type+'.csv')

    D['X_inner'] = df[vals.pnames].values.tolist()
    D['X_outer'] = []
    for i in range(1,1000):
        D['X_outer'].append([1.0,1.0]) #does not work, --use-wfile True to fix
    D['Y_outer'] = [0]*1000
    D['Y_outer'][offbound_num] = -1

    binids = []
    for i in range(len(vals.obs_names)):
        obs = vals.obs_names[i]
        for bin_num in range(vals.nbins[i]):
            binids.append(obs+"_#" + str(bin_num))
    D['binids'] = binids

    with open('results/eigen_tunes/'+tune_type+'_eigen_input.json', 'w') as f:
        json.dump(json_data, f, indent=4, sort_keys=True)

def build_weight_dict(weights, hnames, binids, normalize=True, **kwargs):

    if len(weights) == (len(hnames) - 1):
        print("adding complimenary value to weights")
        weights.append( 1-sum(weights))

    if normalize:
        tot_sum = sum(weights)
        weights = [x/tot_sum for x in weights]

    assert len(weights) == len(hnames),\
        "size of weights {} has to be equal to the size of observables {}".format(
            len(weights), len(hnames)
        )
    return dict([(x,y) for x,y in zip(hnames, weights)])
    # hname_dict = dict([(hname, idx) for idx,hname in enumerate(hnames)])
    # all_weights = dict([
    #     weights[hname_dict[ibin.split('#')[0]]] for ibin in binids
    # ])
    # return np.array(all_weights)

def build_model(tune_type, args):
    approxfile = args.tunes_folder+'/tune_'+str(offbound_num)+approx_path
    expdatafile = args.expdata
    weightfile = args.tunes_folder+'/tune_'+str(offbound_num)+weights_path
    err_approx = args.tunes_folder+'/tune_'+str(offbound_num)+errapprox_path
    wchi2 = args.weighted_chi2
    if tune_type == 'tune_no_errs':
        IO = TuningObjective3(weightfile, expdatafile, approxfile,
                          filter_hypothesis=False, filter_envelope=False)
    elif tune_type == 'tune_w_errs':
        IO = TuningObjective3(weightfile, expdatafile, approxfile, f_errors=err_approx,
                          filter_hypothesis=False, filter_envelope=False)
    elif tune_type == 'tune_w_cov':
        IO = TuningObjective3(weightfile, expdatafile, approxfile, f_errors=None, computecov=True,
                          filter_hypothesis=False, filter_envelope=False)
    else:
        print(tune_type + ' invalid tune type in build_model')

    mk_json(tune_type, offbound_num)

    # filename = 'Xiangyang/A14_30/meanscore_all_0.json'
    filename = 'results/eigen_tunes/'+tune_type+'_eigen_input.json'
    res = readReport(filename)
    center = np.array(res['x'])
    wdict = build_weight_dict(normalize=args.normalize_weights, **res)
    # wdict = np.array(res['weights'])
    # print(wdict)
    print("------------"+tune_type+"-------------")
    print("length of weights:", len(wdict))
    print("length of hnames", len(IO._hnames))
    print("length of binids", len(IO._binids))
    print("best parameters", center)

    if not args.use_wfile:
        # use weights from the report json file
        # otherwise use the weights in the weight file
        IO.setWeights(wdict)
    else:
        if args.normalize_weights:
            # Read the weight files again
            # then normalize the weights
            with open(weightfile, 'r') as f:
                wdict = dict([(line[:-1].split()[0].split('#')[0], float(line[:-1].split()[1]))
                        for line in f])

            tot_weights = sum(list(wdict.values()))
            norm_val = 1 #len(IO._binids)
            wdict = dict([(key, value*norm_val/tot_weights) for key,value in wdict.items() ])
            print(len(list(wdict.keys())), sum(list(wdict.values())))
            IO.setWeights(wdict)

    weights = np.sqrt(IO._W2)
    print("weighted number of bins: {}".format(np.sum(weights)))
    # print("{:,} bins".format(IO._Y.shape))
    # print(IO._Y.shape)
    weight_sum = np.sum(weights)
    sum_w2 = np.sum(IO._W2)
    if wchi2:
        num_dof = weight_sum * weight_sum / sum_w2 - len(center)
    else:
        num_dof = len(weights) - len(center)

    # unbiased --> using weights in chi2 calcuation
    unbiased = not wchi2
    center_chi2 = IO.objective(center, unbiased=unbiased)

    # num_dof = IO._Y.shape[0] - len(center)
    print("{:.1f} degrees of freedom, calculated with {} weights".format(num_dof, weights.shape[0]))
    print("(sum of weights)^2 = {0:.2f}, sum of weight^2 = {1:.2f}, {0:.2f}/{1:.2f} - {2:.2f} = {3:.2f}".format(
        weight_sum * weight_sum, sum_w2, len(center), num_dof
    ))
    print("center chi2 over number of degrees of freedom: {:.4f}/{:.4f} = {:.4f}; Further divided by sum of weight^2: {:.4f}".format(
        center_chi2, num_dof, center_chi2/num_dof, center_chi2/num_dof/sum_w2))
    # return None

    outdir = os.path.dirname(os.path.abspath(args.outname))
    hessian = IO.hessian(center)
    cov = np.linalg.inv(hessian)
    np.savez(os.path.join(outdir, "cov.npz"), cov=cov)
    t_fwd, evalues, t_back = np.linalg.svd(cov)
    sorted_idx = np.argsort(evalues)

    #max_idx, min_idx = sorted_idx[-1], sorted_idx[0]
    max_idx, min_idx = sorted_idx[-1], sorted_idx[0]

    print("all eigenvalues:", evalues)
    print("eigenvalues chosen: {:.4e} {:.4e}".format(evalues[max_idx], evalues[min_idx]))
    h_fwd, h_eigen, h_back = np.linalg.svd(hessian)

    print("max and min eigen value of HESSIAN matrix: {:.4e} {:.4e}".format(max(h_eigen), min(h_eigen)))
    max_col = t_fwd[max_idx, :]
    min_col = t_fwd[min_idx, :]
    print("scaling targeting number of degrees of freedom by {:.2f}".format(args.dof_scale))

    # going through maximum direction
    cl = args.cl
    edof = num_dof * args.dof_scale
    target_dev = chi2pdf.ppf(cl, edof)
    print(f"target deviations {target_dev:.4f}, with cl {cl:.4f}, {edof:.4f}")

    def find_boundary(direction, dx=0.0001):
        dchi2 = 0
        current_x = new_x = center
        step = 0
        while dchi2 < target_dev:
            if step > 1000:
                break
            step += 1
            current_x = new_x
            new_chi2 = IO.objective(current_x, unbiased=unbiased)
            dchi2 = abs(new_chi2 - center_chi2)
            new_x = current_x + dx*direction
        return current_x

    dx = 0.001
    # loop over all eigenvalues and print the boundary
    ellipse_center = [center[0], center[1]]
    axis1, axis2 = [],[]
    axes = [axis1, axis2]
    for idx in range(2):
        col = t_fwd[idx, :]
        up_val = find_boundary(col, dx=dx)
        down_val = find_boundary(col, dx=-dx)
        print("--------", idx)
        for idx2 in range(center.shape[0]):
            print("{:.3f} {:.3f} {:.3f}".format(center[idx2], up_val[idx2], down_val[idx2]))
        axes[idx].append([up_val[0], up_val[1]])
        axes[idx].append([down_val[0], down_val[1]])

    
    d1 = math.dist(axis1[0], axis1[1])
    d2 = math.dist(axis2[0], axis2[1])
    angle = 180 - math.degrees(atan2(axis1[0][0] - axis1[1][0], axis1[0][1] - axis1[1][1]))
    color = next(tune_colors)

    ell = matplotlib.patches.Ellipse(ellipse_center, d2, d1, color = color, angle = angle, fill = False, label = tune_type)
    ax.add_patch(ell)
    plt.plot(ellipse_center[0], ellipse_center[1], 'o', color=color,markersize=1.5) 

    x_max_up = find_boundary(max_col, dx=dx)
    x_max_down = find_boundary(max_col, dx=-dx)
    x_min_up = find_boundary(min_col, dx=dx)
    x_min_down = find_boundary(min_col, dx=-dx)


    with open(args.outname, 'w') as f:
        out = ""
        for idx in range(center.shape[0]):
            all_vars = [x_max_up[idx], x_max_down[idx], x_min_up[idx], x_min_down[idx]]
            out += "{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}\n".format(
                    center[idx], min(all_vars), max(all_vars), x_max_up[idx],
                    x_max_down[idx], x_min_up[idx], x_min_down[idx])
        f.write(out)
    return target_dev, center

def graph_contour(tune_type, levels, center, tune_colors):
    approxfile = args.tunes_folder+'/tune_'+str(offbound_num)+approx_path
    expdatafile = args.expdata
    weightfile = args.tunes_folder+'/tune_'+str(offbound_num)+weights_path
    err_approx = args.tunes_folder+'/tune_'+str(offbound_num)+errapprox_path
    wchi2 = args.weighted_chi2
    if tune_type == 'tune_no_errs':
        IO = TuningObjective3(weightfile, expdatafile, approxfile,
                          filter_hypothesis=False, filter_envelope=False)
    elif tune_type == 'tune_w_errs':
        IO = TuningObjective3(weightfile, expdatafile, approxfile, f_errors=err_approx,
                          filter_hypothesis=False, filter_envelope=False)
    elif tune_type == 'tune_w_cov':
        IO = TuningObjective3(weightfile, expdatafile, approxfile, f_errors=None, computecov=True,
                          filter_hypothesis=False, filter_envelope=False)
    else:
        print(tune_type + ' invalid tune type in build_model')

    s1 = 50
    s2 = 50

    p1 = np.linspace(vals.p_min[0], vals.p_max[0], s1)
    p2 = np.linspace(vals.p_min[1], vals.p_max[1], s2)
    x, y = np.meshgrid(p1, p2)

    unbiased = not wchi2
    z = np.empty((s2,s1))
    center_objective = IO.objective(center, unbiased=unbiased)
    for i in range(s1):
        for j in range(s2):
            z[j][i] = IO.objective([p1[i],p2[j]], unbiased=unbiased) -center_objective

    # with open('results/eigen_tunes/'+tune_type+'_z.txt', 'wb') as outfile:
    #     json.dump(z.tolist(), indent=4, sort_keys=True)
    
    colors = None
    if tune_colors != None:
        colors = next(tune_colors)
    if levels == None:
        return ax.contour(x,y,z, colors = colors)
    return ax.contour(x,y,z,levels, colors = colors)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Eigen Tune studies")
    add_arg = parser.add_argument
    # add_arg("--filename", help="input filename", default='results/eigen_tunes/tune_no_errs_eigen_input.json')
    add_arg("--outname", help="output filename", default='results/eigen_tunes/result.txt')
    add_arg("--experiment_name", help="2_exp, 2_gauss for example")

    # add_arg("--approx", help="Approximation json file", default="tunes/tune_0/val_30.json")
    add_arg("--expdata", help='experimental data json file', default="data.json")
    # add_arg("--weights", help='weight file', default='tunes/tune_0/myweights.txt')
    # add_arg("--errapprox", help='error approximation', default="tunes/tune_0/err_20.json")
    add_arg("--tunes_folder", help='folder with many recorded tunes, tune_0, tune_1 etc.', default="tunes")
    add_arg("--use-wfile", help='use weight files', action='store_true')
    add_arg("--normalize-weights", help='normalize weights', action='store_true')
    add_arg("--dof-scale", help='scaling the targeting nDoF', type=float, default=1.0)
    add_arg("--cl", help='confidence level', type=float, default=0.68268949)
    add_arg("--weighted-chi2", help='use weighted chi2', action='store_true')

    args = parser.parse_args()
    vals = importlib.import_module('set_values_' + args.experiment_name)
    tune_types = ['tune_no_errs','tune_w_errs','tune_w_cov']
    
    approx_path = '/val_30.json'
    errapprox_path = '/err_20.json'
    weights_path = '/myweights.txt'
    # find tune with all offbound, we just assume many_tunes exists
    dfs = {}
    for tune_file in tune_types:
        dfs[tune_file] = pd.read_csv('results/many_tunes/'+tune_file+'.csv')
    offbound_num = 0
    while True:
        # print("Trying tune_" + str(offbound_num))
        for tune_file in tune_types:
            onbound = dfs[tune_file].at[offbound_num, 'ONBOUND']
            # print(tune_file + ' ONBOUND: ' + str(onbound))
            if onbound:
                offbound_num += 1
                break
        if not onbound:
           break
    print('Using tune_' + str(offbound_num))

    tune_colors = cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    target_dev={}
    center={}

    fig, ax = plt.subplots()
    plt.plot(vals.targets[0], vals.targets[1],'ro',markersize=1.5,label = 'target params')
    for tune_type in tune_types:
        target_dev[tune_type], center[tune_type]  = build_model(tune_type, args)

    plt.title("chi2 boundary region from eigenvectors (ellipse) for " + args.experiment_name)
    plt.xlabel('a')
    plt.ylabel('b')
    # ax.set_aspect('equal')
    ax.set_xlim(vals.p_min[0],vals.p_max[0])
    ax.set_ylim(vals.p_min[1],vals.p_max[1])
    plt.legend()
    plt.savefig('results/eigen_tunes/boundary_ellipse.pdf')

    plt.figure()
    fig, ax = plt.subplots()
    tune_colors = cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    objects = []
    for tune_type in tune_types:
        legend_temp,_ = graph_contour(tune_type, [target_dev[tune_type]], center[tune_type], tune_colors).legend_elements()
        objects.append(legend_temp[0])
    #wrong if target_dev changes between tunes
    plt.title("boundary region for " + args.experiment_name.format(val = target_dev['tune_w_cov']))
    plt.xlabel('a')
    plt.ylabel('b')
    # ax.set_aspect('equal')
    ax.set_xlim(vals.p_min[0],vals.p_max[0])
    ax.set_ylim(vals.p_min[1],vals.p_max[1])
    ax.legend(objects, tune_types)
    plt.savefig('results/eigen_tunes/boundary_contour.pdf')


    plt.title("chi2 boundary region from eigenvectors (ellipse) for " + args.experiment_name)
    plt.xlabel('a')
    plt.ylabel('b')
    # ax.set_aspect('equal')
    ax.set_xlim(vals.p_min[0],vals.p_max[0])
    ax.set_ylim(vals.p_min[1],vals.p_max[1])
    plt.legend()
    plt.savefig('results/eigen_tunes/boundary_ellipse.pdf')

    tune_colors = cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])

    # gen_levels = [10,20,50,100,200,500]
    # graph_ellipse = [True, True, True]
    # for tune_type in tune_types:
    #     plt.figure()
    #     fig, ax = plt.subplots()
    #     objects = []
    #     cs = graph_contour(tune_type, gen_levels, None)
    #     plt.clabel(cs)
    #     legend_temp,_ = cs.legend_elements()
    #     objects.append(legend_temp[0])
    #     plt.title("boundary region from chi2 (contour) for " + args.experiment_name)
    #     plt.xlabel('a')
    #     plt.ylabel('b')
    #     ax.set_aspect('equal')
    #     ax.set_xlim(vals.p_min[0],vals.p_max[0])
    #     ax.set_ylim(vals.p_min[1],vals.p_max[1])
    #     ax.legend(objects, [tune_type])
    #     plt.savefig('results/eigen_tunes/'+tune_type+'_contour.pdf')


