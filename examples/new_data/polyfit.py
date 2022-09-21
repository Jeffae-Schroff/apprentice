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

        if len(kwargs.keys()) == 3:
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
            # self.index = {k : np.array(self.index[k]) for k in self.index.keys()}
            self.dim = len(f['params'][0])

            self.fit_index = {}
            for bin_id in bin_ids:
                bin_name, bin_number = bin_id.split('#')[0], int(bin_id.split('#')[1])
                X = np.array(f['params'][:], dtype=np.float64)
                Y = np.array(f['values'][self.index[bin_name][int(bin_number)]])
                VM = self.vandermonde_jax(X, self.order)

                #polynomialapproximation.coeffsolve2 code
                pcoeffs, res, rank, s  = np.linalg.lstsq(VM, Y, rcond=None)

                surrogate_Y = self.surrogate(X, pcoeffs)
                chi2 = np.sum(np.divide(np.power((Y - surrogate_Y), 2), surrogate_Y))

                #polynomialapproximation.fit code
                if kwargs["computecov"]:
                    cov = np.linalg.inv(VM.T@VM)
                fac = res / (VM.shape[0]-VM.shape[1])
                cov = cov*fac

                bin_dict = {}
                bin_dict['pceoffs'] = pcoeffs.tolist()
                bin_dict['res'] = res.tolist()
                bin_dict['chi2/ndf'] = chi2/self.numCoeffsPoly(self.dim, self.order)
                bin_dict['cov'] = cov.tolist()
                self.fit_index[bin_id] = bin_dict
            
            json_dict = {'input_h5': self.input_h5, 'order': self.order, 'dim': self.dim,
             'bin_index': self.index, 'fit_index': self.fit_index}
            with open(fit_json, 'w') as f:
                json.dump(json_dict, f, indent = 4)
        elif len(kwargs) == 0:
            #loads from json file into class variables
            with open(fit_json, "r") as f:
                json_dict = json.load(f)
            self.input_h5 = json_dict['input_h5']
            self.order = json_dict['order']
            self.dim = json_dict['dim']
            self.index = json_dict['bin_index']
            self.fit_index = json_dict['fit_index']
        else:
            print('error in polyfit')

    def get_XY(self, bin_id):
        # probably temp for testing
        f = h5py.File(self.input_h5, "r")
        bin_name, bin_number = bin_id.split('#')[0], int(bin_id.split('#')[1])
        return np.array(f['params'][:], dtype=np.float64),np.array(f['values'][self.index[bin_name][int(bin_number)]])

    def get_surrogate_func(self, bin):
        """
        Returns a surrogate that does not need pceoffs as an input.
        Returns chi2/ndf of fit and residual(s) along with this function.
        """
        if type(bin) is int:
            fit = list(self.fit_index.values())[bin]
        else:
            fit = self.fit_index[bin]
        return partial(self.surrogate, pcoeffs = fit['pceoffs']), fit['res'], fit['chi2/ndf'], fit['cov']

    def surrogate(self, x, pcoeffs):
        """
        Takes a list/array of param sets, and returns the surrogate's estimate for their nominal values.
        The length of the highest dimension of the list/array is the number of params.
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
        If params is a 2-D array, the highest dimension indicates number of parameters.
        """
        try:
            dim = len(params[0])
        except:
            dim = 1
        params = jnp.array(params)

        #We will take params to the power of grlex_pow element-wise
        if dim == 1:
            grlex_pow = jnp.array(range(order+1))
        else:
            term_list = [[0]*dim]
            for i in range(1, self.numCoeffsPoly(dim, order)):
                term_list.append(self.mono_next_grlex(dim, term_list[-1][:]))
            grlex_pow = jnp.array(term_list)
        
        if dim == 1:
            V = jnp.zeros((len(params), self.numCoeffsPoly(dim, order)), dtype=jnp.float64)
            for a, p in enumerate(params): 
                V = V.at[a].set(p**grlex_pow)
            return V
        else:
            V = jnp.power(params, grlex_pow[:, jnp.newaxis])
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


