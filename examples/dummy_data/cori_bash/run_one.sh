
app-build inputdata.h5  --order 3,0 --sample 30 -s $1 -o val_30.json --computecov True
app-build inputdata.h5  --order 2,0 --sample 30 -s $1 -o err_20.json --errs
app-ls val_30.json -w > myweights.txt
app-tune2 myweights.txt data.json val_30.json -o tune_no_errs
app-tune2 myweights.txt data.json val_30.json -e err_20.json -o tune_w_errs
app-tune2 myweights.txt data.json val_30.json --computecov True -o tune_w_cov
python3 data_scripts/gather_tune_data.py tune_no_errs
python3 data_scripts/gather_tune_data.py tune_w_errs
python3 data_scripts/gather_tune_data.py tune_w_cov