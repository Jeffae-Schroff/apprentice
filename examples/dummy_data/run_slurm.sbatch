#!/bin/bash

#SBATCH -C haswell
#SBATCH --time=04:00:00

### This script works for any number of nodes, Ray will find and manage all resources
#SBATCH --nodes=1

### Give all resources to a single Ray task, ray can manage the resources internally
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=32

# setup the ray cluster
source start-ray-cluster

# run the job
raytaskfarmer.py -i 16_run_task_list.txt

# exit
exit