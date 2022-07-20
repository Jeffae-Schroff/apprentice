import importlib
import json
import argparse
import pandas as pd
#assumes it is running in an experiment folder with tunes/tune_0 etc.

parser = argparse.ArgumentParser()
add_arg = parser.add_argument
add_arg("experimentName", type=str)
add_arg("tuneType", help="tune_no_errs, tune_w_errs, tune_w_cov")

args = parser.parse_args()

vals = importlib.import_module(args.experimentName)

json_data = {'chain-0':{}}
D = json_data['chain-0']
D['pnames_inner'] = vals.pnames
D['pnames_outer'] = vals.obs_names

df = pd.read_csv('results/many_tunes/'+args.tuneType+'.csv')

D['X_inner'] = df[vals.pnames].values.tolist()
D['X_outer'] = [[1.0,1.0]]
D['Y_outer'] = [0]

binids = []
for i in range(len(vals.obs_names)):
    obs = vals.obs_names[i]
    for bin_num in range(vals.nbins[i]):
        binids.append(obs+"_#" + str(bin_num))
D['binids'] = binids

with open('results/eigen_tunes/'+args.tuneType+'_eigen_input.json', 'w') as f:
    json.dump(json_data, f, indent=4, sort_keys=True)
