#!/bin/bash 
# File Structure:
# experiments
#     experiment_folder
#         Data
#         MC
#         inputdata.h5
#         data.json
#         tunes
#             tune_0
#                 val_30.json
#                 err_20.json
#                 my_weights.txt
#                 mytune
#                 tune_no_errs
#                 tune_w_errs
#                 tune_w_cov
#             tune_1
#             ...
#         results
#             many_tunes
#                 tune_no_errs.csv
#                 tune_w_errs.csv
#                 tune_w_cov.csv
#             TBD

experiment_name="2_exp" 
error="linear"
experiment_folder="${experiment_name}_${error}_$(date +%m-%d-%Y_%T)"
python3 data_scripts/mk_expr_folder.py "${experiment_folder}"
pushd experiments/"${experiment_folder}"
python3 ../../data_scripts/mk_data.py "${experiment_name}" "${error}"
app-yoda2h5 MC --pname used_params -o inputdata.h5
python3 ../../data_scripts/add_err.py "${experiment_name}" "${error}" inputdata.h5
app-datadirtojson Data -o data.json
popd

num_runs=10
start=$(date +%s)

for ((i=0; i < $num_runs; i++))
do
    mkdir experiments/"${experiment_folder}"/tunes/tune_"${i}"
    pushd experiments/"${experiment_folder}"/tunes/tune_"${i}"
    app-build ../../inputdata.h5  --order 3,0 --sample 30 -s $i -o val_30.json --computecov True
    app-build ../../inputdata.h5  --order 2,0 --sample 30 -s $i -o err_20.json --errs
    app-ls val_30.json -w > myweights.txt
    app-yodaenvelope val_30.json -o mytune/envelope
    app-tune2 myweights.txt ../../data.json val_30.json -o tune_no_errs
    app-tune2 myweights.txt ../../data.json val_30.json -e err_20.json -o tune_w_errs
    app-tune2 myweights.txt ../../data.json val_30.json --computecov True -o tune_w_cov
    python3 ../../../../data_scripts/gather_tune_data.py tune_no_errs
    python3 ../../../../data_scripts/gather_tune_data.py tune_w_errs
    python3 ../../../../data_scripts/gather_tune_data.py tune_w_cov
    popd
    current=$(date +%s)
    printf "\n\n------------Run $((i+1)) of $num_runs finished     Elapsed time: $(($current-$start)) s--------------\n\n"
done
pushd experiments/"${experiment_folder}"
python3 ../../data_scripts/save_setup.py ../../run_many.sh ../../data_scripts/"${experiment_name}".py
python3 ../../data_scripts/eigen_analysis.py --experiment_name "${experiment_name}".py --use-wfile
python3 ../../data_scripts/param_stats.py results/many_tunes/tune_no_errs.csv "${experiment_name}" 1
python3 ../../data_scripts/param_stats.py results/many_tunes/tune_w_errs.csv "${experiment_name}" 1
python3 ../../data_scripts/param_stats.py results/many_tunes/tune_w_cov.csv "${experiment_name}" 1
python3 ../../data_scripts/graph_pandas.py results/many_tunes "${experiment_name}"
pushd tunes/tune_0
python3 ../../../../data_scripts/graph_surrogates_and_target.py myweights.txt ../../data.json val_30.json err_20.json \
 ../../results/surrogate_target_graphs "${experiment_name}"
popd 
