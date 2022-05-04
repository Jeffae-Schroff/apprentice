#!/bin/bash 
python3 data_scripts/mk_data.py
app-yoda2h5 MC --pname used_params -o inputdata.h5
python3 data_scripts/add_err.py
app-datadirtojson Data -o data.json
python3 data_scripts/new_many_tunes.py