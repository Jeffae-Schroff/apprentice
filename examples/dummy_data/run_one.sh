#!/bin/bash 
experiment_name="2_exp"
error="linear"
npoints=100000
python3 data_scripts/new_many_tunes.py
python3 data_scripts/mk_data.py "${experiment_name}" "${error}" "${npoints}"
app-yoda2h5 MC --pname used_params -o inputdata.h5
python3 data_scripts/add_err.py "${experiment_name}" "${error}"
app-datadirtojson Data -o data.json
app-build inputdata.h5  --order 3,0 --sample 30 -s 1 -o val_30.json --computecov True
app-build inputdata.h5  --order 2,0 --sample 30 -s 1 -o err_20.json --errs
app-ls val_30.json -w > myweights.txt
app-yodaenvelope val_30.json -o mytune/envelope
app-tune2 myweights.txt data.json val_30.json -o tune_no_errs
app-tune2 myweights.txt data.json val_30.json -e err_20.json -o tune_w_errs
app-tune2 myweights.txt data.json val_30.json --computecov True -o tune_w_cov

