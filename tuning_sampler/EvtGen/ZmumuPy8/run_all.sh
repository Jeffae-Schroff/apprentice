#!/bin/bash

for INDIR in 4alphaS_submit/*
do
	if [ -d $INDIR ];then
		echo $INDIR
		pythia8-main93 -c $INDIR/runPythia.cmnd -n 100000 -o $INDIR/combined
	fi
done
