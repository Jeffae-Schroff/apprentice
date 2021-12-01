#!/bin/bash 
python3 data_scripts/mk_data.py
app-yoda2h5 MC --pname used_params -o inputdata.h5
python3 data_scripts/add_err.py
app-datadirtojson Data -o data.json
app-build inputdata.h5  --order 3,0 -o val_30.json
app-build inputdata.h5  --order 2,0 -o err_20.json --errs
app-yodaenvelope val_30.json -o mytune/envelope
app-ls val_30.json -w > myweights.txt
app-tune2 myweights.txt data.json val_30.json -o tune_no_errs
app-tune2 myweights.txt data.json val_30.json -e err_20.json -o tune_w_errs

# python3 mk_data.py
# app-yoda2h5 MC --pname used_params -o inputdata.h5
# app-datadirtojson Data -o data.json
# app-build inputdata.h5  --order 3,0 -o val_30.json
# app-yodaenvelope val_30.json -o mytune/envelope
# app-ls val_30.json -w > myweights.txt
# app-tune2 myweights.txt data.json val_30.json -o tune_no_errs

# python3 add_err.py
# app-datadirtojson Data -o data.json
# app-build inputdata.h5  --order 3,0 -o val_30.json
# app-yodaenvelope val_30.json -o mytune/envelope
# app-ls val_30.json -w > myweights.txt
# app-tune2 myweights.txt data.json val_30.json -o tune_no_errs