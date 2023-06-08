import pandas as pd
import numpy as np
import waterfall_chart
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300


a = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
b = [1000,-300,400,-100,100,-700,400,-300,500,-700,100,50]
waterfall_chart.plot(a, b, rotation_value=0);