import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
import pandas as pd

def plotSpec(dir, roll = False):
    spec_curve = pd.read_csv(dir, delim_whitespace=True)
    #spec_curve.rename(columns = [1])
    if (roll):
        spec_curve.iloc[:,1] = spec_curve.iloc[:,1].rolling(5).mean()
    wavelen = spec_curve.iloc[:,0]
    fluxs = spec_curve.iloc[:,1]
    wavelen.to_numpy()
    fluxs.to_numpy()
    plt.plot(wavelen,fluxs)
    plt.show()

plotSpec("SN2020tlf_NIRES_59245.txt",True)
