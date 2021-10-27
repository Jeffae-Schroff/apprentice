#!/usr/bin/env python
# From https://yoda.hepforge.org/plot_yoda_matplotlib.py
import numpy as np
import matplotlib.pylab as plt

import argparse

parser = argparse.ArgumentParser(description="Example plotting a YODA histo with Matplotlib")
parser.add_argument('--yodaFile', '-y', type=str, default="Rivet.yoda")
parser.add_argument('--plot', '-p', type=str, default="")
parser.add_argument('--logx', action='store_true')
parser.add_argument('--logy', action='store_true')
parser.add_argument('--label', '-l', type=str, default="")
parser.add_argument('--xlabel', type=str, default="x label")
parser.add_argument('--ylabel', type=str, default="y label")

args = parser.parse_args()

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

import yoda

file = yoda.read(args.yodaFile)
print(file)
histo = file[args.plot]
#histo = list(file.items())[0]

f, ax = plt.subplots(1,figsize=(8.5, 7.), facecolor='w')

plt.xticks(fontsize=24)
plt.yticks(fontsize=24)

plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.15)

ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')

if args.logx:
  plt.xscale('log')

if args.logy:
  plt.yscale('log')

#ax.plot(histo.xMids(), histo.yVals(), "ko", label=args.label)
ax.step(histo.xMaxs(), histo.yVals(), "black", label=args.label)

ax.set_xlabel(args.xlabel, fontsize=36)
ax.set_ylabel(args.ylabel, fontsize=36)

ax.yaxis.set_label_coords(-0.12, 0.72)
ax.xaxis.set_label_coords(0.7, -0.095)

ax.legend(loc=1, fontsize=20, frameon=False)

plt.savefig("myplot.pdf")
plt.show()