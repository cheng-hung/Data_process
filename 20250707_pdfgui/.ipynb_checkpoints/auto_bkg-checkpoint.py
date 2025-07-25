import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy
from scipy import integrate
from scipy.optimize import minimize, NonlinearConstraint


class auto_bkg():
    
    def __init__(self, data_fn, bkg_fn):       
        self.data_fn = data_fn
        self.bkg_fn = bkg_fn
        self.bkg_scale = 1.0
        self.data_df = None
        self.bkg_df = None
        self.bkg_opt = None
        self.min_res = None

    
    def pdload_data(self, **kwargs):
        data_df = pd.read_csv(self.data_fn, **kwargs)
        self.data_df = data_df
        return data_df


    def pdload_bkg(self, **kwargs):
        bkg_df = pd.read_csv(self.bkg_fn, **kwargs)
        self.bkg_df = bkg_df
        return bkg_df
        

    def data_sub(self, scale):
        return self.data_df.iloc[:,1] - scale*self.bkg_df.iloc[:,1]


    def guess_01(self, update_scale=True):
        bkg_max_val = self.bkg_df.iloc[:,1].max()
        bkg_max_idx = self.bkg_df.iloc[:,1].idxmax()

        data_cor_val = self.data_df.iloc[bkg_max_idx, 1]
        scale_01 = data_cor_val/bkg_max_val

        if update_scale:
            self.bkg_scale = scale_01
        
        return scale_01


    def integral_sub(self, scale):
        return integrate.simpson(self.data_sub(scale))


    def min_integral(self):
        # Define a constraint where 0 <= x[0] + x[1] <= 1
        # nlc = NonlinearConstraint(self.data_sub, 0, 50)
        nlc = [{'type': 'ineq', 'fun': self.data_sub} # 1 - x0^2 - x1 >= 0
              ]
        
        a0 = self.guess_01()
        
        result = minimize(self.integral_sub, 
                          [a0], 
                          method='COBYLA', 
                          constraints=nlc, 
                          tol=1e-7, 
                          # options={'verbose': 3, 
                          #          'barrier_tol':1e-5, 
                          #          'maxiter': 1000, }
                         )
            
        self.min_res = result

        if result.success:
            print('Found the bkg scale to minimize the integral')
            self.bkg_opt = result.x[0]

        else:
            print('Unable to find the bkg scale by minimizing integral')

        return result


    def plot_sub(self):

        fig, ax = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)

        ax[0].plot(self.data_df.iloc[:,0], self.data_df.iloc[:,1], label='data')
        
        try:
            ax[0].plot(self.bkg_df.iloc[:,0], self.bkg_df.iloc[:,1]*self.bkg_opt, 'g.', label='scaled_bkg', )
            ax[1].plot(self.data_df.iloc[:,0], self.data_sub(self.bkg_opt), label=f'data_sub, scale={self.bkg_opt: .3f}')
        
        except TypeError:
            ax[0].plot(self.bkg_df.iloc[:,0], self.bkg_df.iloc[:,1]*self.guess_01(), 'r.', label='scaled_bkg', )
            ax[1].plot(self.data_df.iloc[:,0], self.data_sub(self.guess_01()), label=f'data_sub, scale={self.guess_01(): .3f}')

        ax[0].legend()
        ax[1].legend()
        
        

        


    