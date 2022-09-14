import h5py
import numpy as np
import jax.numpy as jnp
from jax.config import config
config.update("jax_enable_x64", True)
config.update('jax_platform_name', 'cpu')
from functools import partial
import json

class Polyfit:
    def __init__(self, fit_json, **kwargs):
        """ Fit polynomials of order order to each bin in input_h5.
        If no kwargs are given, it instead assumes fit_json stores fits from a previous instance

        Keyword arguments:
        fit_json -- filepath for json file which will contain the fitting results
        input_h5 -- the name of an h5 file with MC run results
        order -- the order of polynomial to fit each bin with
        """

        if len(kwargs.keys()) == 2:
            self.input_h5 = kwargs['input_h5']
            self.order = kwargs['order']

            f = h5py.File(self.input_h5, "r")

            # self.pnames = [str(p) for p in f.get('params').attrs["names"]]
            # print("parameter names: ", self.pnames)

            # self.observables = np.unique([x.decode().split("#")[0] for x in f.get("index")[:]])
            # print(len(self.observables), "observables")
            # print(observables[0:10])
            # print(f.get("index")[0:10])

            # key bin names to the array indexes(of values) with binids(in index) matching their bin
            self.index = {}
            bin_ids = [x.decode() for x in f.get("index")[:]]
            [self.index.setdefault(bin.split('#')[0], []).append(i) for i,bin in enumerate(bin_ids)]
            self.index = {k : np.array(self.index[k]) for k in self.index.keys()}
            self.dim = len(f['params'][0])

            self.pcoeff_dict = {}
            for bin_id in bin_ids:
                bin_name, bin_number = bin_id.split('#')[0], int(bin_id.split('#')[1])
                self.X = np.array(f['params'][:], dtype=np.float64)
                self.Y = np.array(f['values'][self.index[bin_name][int(bin_number)]])
                VM = self.vandermonde_jax(self.X, self.order)
                #coeffsolve2 code
                pcoeffs, res, rank, s  = np.linalg.lstsq(VM, self.Y, rcond=None)
                self.pcoeff_dict[bin_id] = pcoeffs.tolist()
            
            json_dict = {'input_h5': self.input_h5, 'order': self.order, 'dim': self.dim, 'pcoeffs': self.pcoeff_dict}
            with open(fit_json, 'w') as f:
                json.dump(json_dict, f, indent = 4)
        elif len(kwargs) == 0:
            with open(fit_json, "r") as f:
                json_dict = json.load(f)
            self.input_h5 = json_dict['input_h5']
            self.order = json_dict['order']
            self.dim = json_dict['dim']
            self.pcoeff_dict = {key: np.array(value) for key, value in json_dict['pcoeffs'].items()}
        else:
            print('error in polyfit')

    def get_XY(self, bin_id):
        # temp for testing
        f = h5py.File(self.input_h5, "r")
        bin_name, bin_number = bin_id.split('#')[0], int(bin_id.split('#')[1])
        self.index = {}
        bin_ids = [x.decode() for x in f.get("index")[:]]
        [self.index.setdefault(bin.split('#')[0], []).append(i) for i,bin in enumerate(bin_ids)]
        self.index = {k : np.array(self.index[k]) for k in self.index.keys()}
        return np.array(f['params'][:], dtype=np.float64),np.array(f['values'][self.index[bin_name][int(bin_number)]])

    def get_surrogate_func(self, bin):
        """
        Returns a surrogate that does not need
        """
        if type(bin) is int:
            return partial(self.surrogate, pcoeffs = list(self.pcoeff_dict.values())[bin])
        return partial(self.surrogate, pcoeffs = self.pcoeff_dict[bin])

    def surrogate(self, x, pcoeffs):
        """
        Takes a list/array of param sets, and returns the surrogate's estimate for their nominal values.
        The length of the highest dimension of the list/array is the number of params.
        TODO: residuals and chi2/ndf
        """
        x = np.array(x)
        dim = x.shape[-1]
        term_powers = dim*[0]
        pvalues = []
        last_axis = None if len(x.shape) == 1 else len(x.shape)-1
        for pcoeff in pcoeffs:
            #appending the value of the term for each param set given
            pvalues.append(pcoeff*np.prod(x**term_powers, axis = last_axis))
            term_powers = self.mono_next_grlex(dim, term_powers)
        #add along first axis to sum the terms for each param set
        return np.sum(pvalues, axis=None if len(x.shape) == 1 else 0)
    def vandermonde_jax(self, params, order):
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
            for i in range(1, self.numCoeffsPoly(dim, order)):
                term_list.append(self.mono_next_grlex(dim, term_list[-1][:]))
            s = jnp.array(term_list)
        
        if len(params[0]) == 1:
            V = jnp.zeros((len(params), self.numCoeffsPoly(dim, order)), dtype=jnp.float64)
            for a, p in enumerate(params): 
                V = V.at[a].set(p**s)
            return V
        else:
            V = jnp.power(params, s[:, jnp.newaxis])
            return jnp.prod(V, axis=2).T
    def numCoeffsPoly(self, dim, order):
        """
        Number of coefficients a dim-dimensional polynomial of order order has (C(dim+order, dim)).
        """
        ntok = 1
        r = min(order, dim)
        for i in range(r):
            ntok = ntok * (dim + order - i) / (i + 1)
        return int(ntok)
    def mono_next_grlex(self, m, x):
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


