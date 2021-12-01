#!/bin/bash 
python3 data_scripts/mk_data.py
app-yoda2h5 MC --pname used_params -o inputdata.h5
python3 data_scripts/add_err.py
app-datadirtojson Data -o data.json

python3 data_scripts/new_many_tunes.py
for i in {1..30}; do 
    app-build inputdata.h5  --order 3,0 --sample 30 -s $i -o val_30.json
    app-build inputdata.h5  --order 2,0 --sample 30 -s $i -o err_20.json --errs
    app-yodaenvelope val_30.json -o mytune/envelope
    app-ls val_30.json -w > myweights.txt
    app-tune2 myweights.txt data.json val_30.json -o tune_no_errs
    app-tune2 myweights.txt data.json val_30.json -e err_20.json -o tune_w_errs
    python3 data_scripts/gather_tune_data.py tune_no_errs
    python3 data_scripts/gather_tune_data.py tune_w_errs
done
python3 data_scripts/param_stats.py tune_no_errs
python3 data_scripts/param_stats.py tune_w_errs