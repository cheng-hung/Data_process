import os, glob
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Button


class color_tuner():
    
    def __init__(self, fig, img, aspect=1, q_array=None):
    
        self.fig = fig
        self.ax = fig.gca()
        # self.ax = self.fig.add_axes([0.1, 0.1, 0.7, 0.8])
        self.img = img
        self.vmax = np.nanpercentile(img, 98)
        self.slider_max = self.vmax+500
        self.vmin = np.nanpercentile(img, 10)
        self.slider_min = self.vmin-500

        if q_array is None:
            self.im = self.ax.imshow(img, vmax=self.vmax, vmin=self.vmin)
            self.ax.set_aspect(aspect)
        else:
            x_mesh = np.asarray(q_array)
            # print(f'{x_mesh.shape = }')
            y_mesh = np.arange(img.shape[0])
            # print(f'{y_mesh.shape = }')
            self.im = self.ax.pcolormesh(x_mesh, y_mesh, img, vmax=self.vmax, vmin=self.vmin)
            self.ax.invert_yaxis()
            
        self.cbar = fig.colorbar(self.im, )
          
        
        # Create the RangeSlider
        self.fig.subplots_adjust(bottom=0.1)
        self.slider_ax = plt.axes([0.15, 0.01, 0.65, 0.03])
        self.slider = RangeSlider(self.slider_ax, "color_scale", self.slider_min, self.slider_max)

        #Creat buttons
        self.axplus = self.fig.add_axes([0.9, 0.9, 0.082, 0.05])
        self.axminus = self.fig.add_axes([0.9, 0.8, 0.082, 0.05])
        self.bplus = Button(self.axplus, 'Max +')
        self.bminus = Button(self.axminus, 'Max -')

        self.axplus1 = self.fig.add_axes([0.01, 0.9, 0.082, 0.05])
        self.axminus1 = self.fig.add_axes([0.01, 0.8, 0.082, 0.05])
        self.bplus1 = Button(self.axplus1, 'Min +')
        self.bminus1 = Button(self.axminus1, 'Min -')

    
    
    def update(self, val):
        # The val passed to a callback by the RangeSlider will
        # be a tuple of (min, max)
    
        # Update the image's colormap
        self.im.norm.vmin = val[0]
        self.im.norm.vmax = val[1]
    
        # Redraw the figure to ensure it updates
        self.fig.canvas.draw_idle()


    def vmax_plus(self, event):
        self.slider_max += 100
        self.slider_ax.remove()
        self.slider_ax = plt.axes([0.15, 0.01, 0.65, 0.03])
        self.slider = RangeSlider(self.slider_ax, "color_scale", self.slider_min, self.slider_max)
        self.slider.on_changed(self.update)

    
    def vmax_minus(self, event):
        self.slider_max -= 100
        # self.slider.set_max(self.slider_max)
        self.slider_ax.remove()
        self.slider_ax = plt.axes([0.15, 0.01, 0.65, 0.03])
        self.slider = RangeSlider(self.slider_ax, "color_scale", self.slider_min, self.slider_max)
        self.slider.on_changed(self.update)


    def vmin_plus(self, event):
        self.slider_min += 100
        self.slider_ax.remove()
        self.slider_ax = plt.axes([0.15, 0.01, 0.65, 0.03])
        self.slider = RangeSlider(self.slider_ax, "color_scale", self.slider_min, self.slider_max)
        self.slider.on_changed(self.update)

    
    def vmin_minus(self, event):
        self.slider_min -= 100
        # self.slider.set_max(self.slider_max)
        self.slider_ax.remove()
        self.slider_ax = plt.axes([0.15, 0.01, 0.65, 0.03])
        self.slider = RangeSlider(self.slider_ax, "color_scale", self.slider_min, self.slider_max)
        self.slider.on_changed(self.update)
        

    def __call__(self):
        self.slider.on_changed(self.update)
        self.bplus.on_clicked(self.vmax_plus)
        self.bminus.on_clicked(self.vmax_minus)
        self.bplus1.on_clicked(self.vmin_plus)
        self.bminus1.on_clicked(self.vmin_minus)
        # pass

        