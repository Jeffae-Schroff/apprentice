#!/bin/bash 
experiment_name="cov_2_gauss_func"
jobs_folder=$1
num_runs=$2

python3 data_scripts/new_many_tunes.py
for ((i=1; i <= $num_runs; i++))
do 
    python3 data_scripts/gather_tune_data.py tune_no_errs $1 $2
    python3 data_scripts/gather_tune_data.py tune_w_errs $1 $2
    python3 data_scripts/gather_tune_data.py tune_w_cov $1 $2
done
python3 data_scripts/param_stats.py many_tunes/tune_no_errs
python3 data_scripts/param_stats.py many_tunes/tune_w_errs
python3 data_scripts/param_stats.py many_tunes/tune_w_cov
python3 data_scripts/save_results.py "${experiment_name}_${num_runs}_runs"