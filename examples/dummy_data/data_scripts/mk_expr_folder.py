import argparse
import os
import shutil
import sys

parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("exprFolder", help="a new folder to do the experiment in", type=str)

# Parse arguments
args = parser.parse_args()

if not os.path.isdir('experiments'):
    os.mkdir('experiments')

print("Experiment running in " + args.exprFolder)

if(os.path.isdir(args.exprFolder)):
    print("Error: folder " + args.exprFolder + " already exists")
    sys.exit(1)
os.mkdir('experiments/' + args.exprFolder)
os.mkdir('experiments/' + args.exprFolder + '/setup')
os.mkdir('experiments/' + args.exprFolder + '/tunes')
os.mkdir('experiments/' + args.exprFolder + '/results')
os.mkdir('experiments/' + args.exprFolder + '/results/important_graphs')
os.mkdir('experiments/' + args.exprFolder + '/results/many_tunes')
os.mkdir('experiments/' + args.exprFolder + '/results/many_tunes_histos')
os.mkdir('experiments/' + args.exprFolder + '/results/eigen_tunes')
os.mkdir('experiments/' + args.exprFolder + '/results/panda_graphs')
os.mkdir('experiments/' + args.exprFolder + '/results/stats')
