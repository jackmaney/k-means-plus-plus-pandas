from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import sys
import os

sys.path = [os.path.abspath("..")] + sys.path

from k_means_plus_plus import *

np.random.seed(1234)  # For reproducibility

# We create a data set with three sets of 500 points each chosen from a normal distrubution with a standard deviation of 10.
# The means for the distributions from which we sample are:
# (25,45), (-30,5), and (5,-20)
data = DataFrame({'x': 10 * np.random.randn(500) + 25, 'y':
                 10 * np.random.randn(500) + 45}, columns=list('xy'))
data = data.append(DataFrame(
    {'x': 10 * np.random.randn(500) - 30, 'y': 10 * np.random.randn(500) + 5}, columns=list('xy')))
data = data.append(DataFrame(
    {'x': 10 * np.random.randn(500) + 5, 'y': 10 * np.random.randn(500) - 20}, columns=list('xy')))

# Grab a scatterplot
import matplotlib.pyplot as plt
plt.scatter(data['x'], data['y'], s=5)
plt.savefig("three_clusters_scatterplot.png")

# Cluster
kmpp = KMeansPlusPlus(data, 3)
kmpp.cluster()

# Get a scatterplot that's color-coded by cluster
colors = [
    "red" if x == 0 else "blue" if x == 1 else "green" for x in kmpp.clusters]
plt.scatter(data['x'], data['y'], s=5, c=colors)
plt.savefig("three_clusters_clusters.png")
