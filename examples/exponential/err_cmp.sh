#!/bin/bash 
echo "This is a shell script"
python3 mk_data.py
app-yoda2h5 MC --pname used_params -o inputdata.h5
app-datadirtojson Data -o data.json
app-build inputdata.h5  --order 3,0 -o val_30.json
app-yodaenvelope val_30.json -o mytune/envelope
app-ls val_30.json -w > myweights.txt
app-tune2 myweights.txt data.json val_30.json -o tune_no_errs

python3 add_err.py
app-datadirtojson Data -o data.json
app-build inputdata.h5  --order 3,0 -o val_30.json
app-yodaenvelope val_30.json -o mytune/envelope
app-ls val_30.json -w > myweights.txt
app-tune2 myweights.txt data.json val_30.json -o tune_no_errs



echo "shell script is finished"