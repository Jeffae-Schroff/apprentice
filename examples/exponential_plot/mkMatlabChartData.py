import numpy as np

"""
Exponential Distribution
"""


def Ex(Z, L = 3):
    return L*np.exp(-L*Z)


np.random.seed(100)


NPOINTS=10000
L = 2 + np.random.random_sample((NPOINTS,))
Z = 2 * np.random.random_sample((NPOINTS,))

# 1D test plot
T = Ex(Z)
import matplotlib.pyplot as plt
# plt.scatter(Z, T)
# plt.savefig("exponential.pdf")


X = np.zeros((NPOINTS, 2))
D = np.zeros((NPOINTS, 3))

X[:,0]=Z
X[:,1]=L

import apprentice
S=apprentice.Scaler(X)

X_scaled = S.scale(X) # scaled with 1, -1 max, min
Y = np.array([Ex(*x) for x in X])
# plt.figure()
# plt.scatter(X_scaled[:,0], Y)

D[:,[0,1]]=X_scaled
D[:,2] = Y

# Store as CSV
np.savetxt("exponential.csv", [(l,z, Ex(l,z)) for l,z in zip(L,Z)], delimiter=',')

# Store as CSV, write out scaled parameter points
np.savetxt("exponential_scaled.csv", D, delimiter=',')

n_bins = 20
noise = 20/100

plt.figure()
plt.hist(Y, bins=n_bins, weights=np.zeros(NPOINTS) + 1. / Y.size)
plt.savefig("exponential_histogram.pdf")

noisy_bin_heights = np.zeros(n_bins)
bin_widths = np.zeros(n_bins + 1)
bin_widths[0] = 0
p = plt.gca().patches
for i in range(n_bins):
    noisy_bin_heights[i] = p[i].get_height()*(1 + noise*np.random.randn(1))
    bin_widths[i+1] = bin_widths[i] + p[i].get_width()
plt.figure()
plt.stairs(noisy_bin_heights, bin_widths, fill=True, color='r')

plt.show()
