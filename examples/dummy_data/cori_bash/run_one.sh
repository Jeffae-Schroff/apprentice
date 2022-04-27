#!/bin/bash
WORKDIR=/global/cscratch1/sd/jeffae/apprentice/examples/dummy_data
app-build $WORKDIR/inputdata.h5  --order 3,0 --sample 30 -s $1 -o val_30.json --computecov True
app-build $WORKDIR/inputdata.h5  --order 2,0 --sample 30 -s $1 -o err_20.json --errs
app-ls val_30.json -w > myweights.txt
app-tune2 myweights.txt $WORKDIR/data.json val_30.json -o tune_no_errs
app-tune2 myweights.txt $WORKDIR/data.json val_30.json -e err_20.json -o tune_w_errs
app-tune2 myweights.txt $WORKDIR/data.json val_30.json --computecov True -o tune_w_cov
