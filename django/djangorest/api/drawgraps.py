
from matplotlib import pylab
from pylab import plt,xlabel,ylabel,grid
from PIL import Image
from io import BytesIO
import base64
from .utils import get_translate_string
import pandas as pd
import numpy as np
from .models import get_dig_metric_data,get_dig_path_data
from math import sqrt

def draw_dig_metric(data, locale):
    """
        get dig metric data and draw dig metric graph.
    """
    title = "Dig_Metric"
    dig_metrics_data = get_dig_metric_data(data)
    title = get_translate_string(title, locale)
    result = __draw_dig_metric(dig_metrics_data, title)

    return result

def draw_dig_path(data, locale):
    """
        get dig path data and draw dig path graph.
    """
    dig_path_data = get_dig_path_data(data)
    result = __draw_dig_path(dig_path_data, locale)

    return result

def __draw_dig_metric(data, label):
    """
        draw dig metric graph with data and set title with locale.
    """
    dig_metrics_data = []
    dig_metrics_data = data
    r=np.array([y for x,y in dig_metrics_data])
    theta = np.array([x for x,y in dig_metrics_data])
    fig = plt.figure()
    ax = plt.subplot(111, polar=True)

    #define the bin spaces
    r_bins     = np.linspace(0., round(max(r)), 12)
    N_theta    = 36
    d_theta    = 2. * np.pi / (N_theta + 1.)
    theta_bins = np.linspace(-d_theta / 2., 2. * np.pi + d_theta / 2., N_theta)

    H, theta_edges, r_edges = np.histogram2d(theta % (2. * np.pi), r, bins = (theta_bins, r_bins))

    #plot data in the middle of the bins
    r_mid     = .5 * (r_edges[:-1] + r_edges[1:])
    theta_mid = .5 * (theta_edges[:-1] + theta_edges[1:])
    xlabel(label)

    cax = ax.contourf(theta_mid, r_mid, H.T, 10, cmap=plt.cm.Spectral)
    ax.scatter(theta, r, color='None')
    ax.set_rmax(round(max(r)))   
    grid(True)
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()

    pil_image = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pylab.close()
    return pil_image

def __draw_dig_path(data, locale):
    """
        draw dig metric graph with data and set title with locale.
    """
    dig_path_data = []
    dig_path_data = data
    result = [(X,Y,Z) for X,Y,Z in dig_path_data if sqrt(X*X +Y*Y)>14 and sqrt(X*X +Y*Y)<28 and Z >-6 and Z <10]

    x = [sqrt(X*X +Y*Y) for X,Y,Z in result]
    y = [Z for X,Y,Z in result]
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)

    fig, ax = plt.subplots(ncols=1, sharey=True, figsize=(7, 4))
    fig.subplots_adjust(hspace=0.5, left=0.27, right=0.93)

    hb = ax.hexbin(x, y, gridsize=150, bins='log', cmap='inferno')
    ax.axis([xmin, xmax, ymin, ymax])
    plt.xlabel(get_translate_string('Cycle_Duration',locale)) 
    plt.ylabel(get_translate_string('Dipper_Load',locale))
    ax.set_title(get_translate_string('Dig_Path',locale))
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('log10(N)')
    grid(True)
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()

    pil_image = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pylab.close()
    return pil_image

