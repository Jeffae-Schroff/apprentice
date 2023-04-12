#!/bin/bash
#SBATCH --image=hepstore/rivet-pythia
#SBATCH --qos=shared
#SBATCH --constraint=haswell

for INDIR in 4alphaS_500runs_submit/*
do
	if [ -d $INDIR ];then
		echo $INDIR
		shifter pythia8-main93 -c $INDIR/runPythia.cmnd -n 100000 -o $INDIR/combined
	fi
done
