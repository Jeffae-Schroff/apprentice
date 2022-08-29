#!/bin/bash 
# compare a basic case without handling error w/ and w/out using jax

pushd jax_test
app-datadirtojson ../Data -o data.json
app-yoda2h5 ../MC --pname used_params -o inputdata.h5
app-build inputdata.h5  --order 3,0  -o val_30.json --computecov
app-build inputdata.h5  --order 2,0  -o err_20.json --errs
# app-ls val_30.json -w > myweights.txt
# app-yodaenvelope val_30.json -o mytune/envelope
# app-tune2 myweights.txt data.json val_30.json -a trust -o tune_no_errs
# app-tune2 myweights.txt data.json val_30.json -a trust -e err_20.json -o tune_w_errs
# app-tune2 myweights.txt data.json val_30.json -a trust -o tune_w_cov --computecov
# popd

