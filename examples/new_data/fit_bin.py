import h5py
import numpy as np
import jax.numpy as jnp
from jax.config import config
config.update("jax_enable_x64", True)
config.update('jax_platform_name', 'cpu')
import matplotlib.pyplot as plt
import argparse
import pickle

# Fits a polynomial curve of order order to the nominal values for one bin of one observable. 
# We have: Y (num_runs * 1), which are the nominal values in the bin for different parameters 
# and X (num_runs * num_params), which are the parameters
# (given to unkwown observable function we try to estimate) that generated these nominal values.

#example arguments:
# filename = '../dummy_data/jax_test/inputdata.h5'
# order = 3
# bin_name = '/func0#0'

# filename = 'inputdata.h5'
# order = 3
# bin_name = '/ATLAS_2019_I1736531/d01-x01-y01[AUX_isr:murfac=0.5]#0'

parser = argparse.ArgumentParser(description="Eigen Tune studies")
add_arg = parser.add_argument
add_arg("-filename", help="input filename", default='../dummy_data/jax_test/inputdata.h5')
add_arg("-order", help='order of polynomial', default=3)
add_arg("-bin_id", help='bin to tune', default='/func0#0')

args = parser.parse_args()


def surrogate(x):
    term = dim*[0]
    powers = []
    for i in range(numCoeffsPoly(dim, order)):
        powers.append(list(term))
        term = mono_next_grlex(dim, term)
    fit = []
    for xi in x:
        fit.append(sum(pcoeff*np.product(xi**powers, axis=1)))
    return fit
def numCoeffsPoly(dim, order):
    """
    Number of coefficients a dim-dimensional polynomial of order order has (C(dim+order, dim)).
    """
    ntok = 1
    r = min(order, dim)
    for i in range(r):
        ntok = ntok * (dim + order - i) / (i + 1)
    return int(ntok)
def mono_next_grlex(m, x):
    #  Author:
    #
    #    John Burkardt
    #
    #     TODO --- figure out the licensing thing https://people.sc.fsu.edu/~jburkardt/py_src/monomial/monomial.html

    #  Find I, the index of the rightmost nonzero entry of X.
    i = 0
    for j in range(m, 0, -1):
        if 0 < x[j-1]:
            i = j
            break

    #  set T = X(I)
    #  set X(I) to zero,
    #  increase X(I-1) by 1,
    #  increment X(M) by T-1.
    if i == 0:
        x[m-1] = 1
        return x
    elif i == 1:
        t = x[0] + 1
        im1 = m
    elif 1 < i:
        t = x[i-1]
        im1 = i - 1

    x[i-1] = 0
    x[im1-1] = x[im1-1] + 1
    x[m-1] = x[m-1] + t - 1

    return x

def vandermonde_jax(params, order):
    """
    Construct the Vandermonde matrix.
    """
    try:
        dim = len(params[0])
    except:
        dim = 1

    #We will take params to the power of s element-wise
    if dim == 1:
        s = jnp.array(range(order+1))
    else:
        term_list = [[0]*dim]
        for i in range(1, numCoeffsPoly(dim, order)):
            term_list.append(mono_next_grlex(dim, term_list[-1][:]))
        s = jnp.array(term_list)
    
    if len(params[0]) == 1:
        V = jnp.zeros((len(params), numCoeffsPoly(dim, order)), dtype=jnp.float64)
        for a, p in enumerate(params): 
            V = V.at[a].set(p**s)
        return V
    else:
        V = jnp.power(params, s[:, jnp.newaxis])
        return jnp.prod(V, axis=2).T


if __name__ == "__main__":
    filename = args.filename
    order = args.order
    bin_id = args.bin_id
    f = h5py.File(filename, "r")

    pnames = [str(p) for p in f.get('params').attrs["names"]]
    print("parameter names: ", pnames)

    observables = np.unique([x.decode().split("#")[0] for x in f.get("index")[:]])
    print(len(observables), "observables")
    # print(observables[0:10])
    # print(f.get("index")[0:10])

    # key bin names to the array indexes(of values) with binids(in index) matching their bin
    index = {}
    II = [x.decode() for x in f.get("index")[:]]
    [index.setdefault(bin.split('#')[0], []).append(i) for i,bin in enumerate(II)]
    index = {k : np.array(index[k]) for k in index.keys()}

    dim = len(f['params'][0])

    bin_name, bin_number = bin_id.split('#')[0], int(bin_id.split('#')[1])
    X = np.array(f['params'][:], dtype=np.float64)
    Y = np.array(f['values'][index[bin_name][int(bin_number)]])
    VM = vandermonde_jax(X, order)

    #coeffsolve2 code
    pcoeff, res, rank, s  = np.linalg.lstsq(VM, Y, rcond=None)

    #coeffsolve code (very small difference so far)
    # U, S, V = np.linalg.svd(VM)
    # # SM dixit: manipulations to solve for the coefficients
    # # Given A = U Sigma VT, for A x = b, x = V Sigma^-1 UT b
    # temp = np.dot(U.T, Y.T)[0:S.size]
    # pcoeff = np.dot(V.T, 1./S * temp)
    # epsilon = Y - np.dot(VM, pcoeff)
    # resids = np.dot(epsilon.T, epsilon)


    # print('polynomial ceofficients compare: ', pcoeff2-pcoeff)
    print('polynomial coefficients: ', pcoeff)

    # #Scaler for testing
    # b = 1
    # a = -1
    # print('binnies', bin_name, bin_number)
    # print(f['xmax'])
    # Xmax = f['xmax'][index[bin_name][bin_number]]
    # Xmin = f['xmin'][index[bin_name][bin_number]]
    # scaleTerm = (b - a)/(Xmax - Xmin)
    # def scale(x):
    #     """
    #     Scale the point x from the observed range _Xmin, _Xmax to the interval _interval
    #     (newmax-newmin)/(oldmax-oldmin)*(x-oldmin)+newmin
    #     """
    #     return scaleTerm*(x - Xmin) + a
    # print(Xmax, Xmin)
    # print('scaled polynomial coefficients', scale(pcoeff))

    if dim == 1:
        p = np.linspace(X.min(), X.max(), 100)
        plt.plot(p, surrogate(p))
        plt.scatter(X.flatten(), Y)
    elif dim == 2:
        fig, ax = plt.subplots()
        plt.scatter(surrogate(X), Y)
        plt.title('Nominal vs surrogate for the given parameter values(X)')
        plt.xlabel('surrogate')
        plt.ylabel('nominal')
        ax.autoscale(tight=True)
        xlim = ax.get_xlim()
        plt.plot(xlim, xlim, 'k--')
    plt.savefig('fit_bin_testing.pdf')
    

    #Pickle time
    dbfile = open('pickle_test', 'ab')
    dict = {index[bin_name][bin_number]:surrogate}
    print('pickling: ', dict)
    pickle.dump(dict, dbfile)                     
    dbfile.close()








