experiment_name="cov_2_gauss_func"
python3 data_scripts/param_stats.py many_tunes/tune_no_errs
python3 data_scripts/param_stats.py many_tunes/tune_w_errs
python3 data_scripts/param_stats.py many_tunes/tune_w_cov
python3 data_scripts/save_results.py "${experiment_name}_${num_runs}_runs"