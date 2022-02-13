#!/bin/bash 
python3 data_scripts/mk_data.py
app-yoda2h5 MC --pname used_params -o inputdata.h5
python3 data_scripts/add_err.py
app-datadirtojson Data -o data.json

start=$(date +%s)
num_runs=1000
python3 data_scripts/new_many_tunes.py
for ((i=1; i <= $num_runs; i++))
do 
    app-build inputdata.h5  --order 3,0 --sample 30 -s $i -o val_30.json --computecov True
    # app-build inputdata.h5  --order 2,0 --sample 30 -s $i -o err_20.json --errs
    app-ls val_30.json -w > myweights.txt
    # app-tune2 myweights.txt data.json val_30.json -e err_20.json -o tune_w_errs
    app-tune2 myweights.txt data.json val_30.json --computecov True -o tune_w_cov
    # python3 data_scripts/gather_tune_data.py tune_w_errs
    python3 data_scripts/gather_tune_data.py tune_w_cov
    current=$(date +%s)
    printf "\n\n------------Run $i of $num_runs      Elapsed time: $(($current-$start)) s--------------\n\n"
done
# python3 data_scripts/param_stats.py many_tunes/tune_w_errs
python3 data_scripts/param_stats.py many_tunes/tune_w_cov