import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plotSpec(spec_curve, roll = False):
    if (roll):
        spec_curve[1] = spec_curve[1].rolling(5, min_periods=0).mean()
    wavelen = spec_curve.iloc[:,0]
    fluxs = spec_curve.iloc[:,1]
    wavelen.to_numpy()
    fluxs.to_numpy()
    plt.plot(wavelen,fluxs)
    
    return spec_curve
    #plt.show()

for file_path in os.listdir('.'):
    if (file_path.endswith(".txt")):
        spec_curve = pd.read_csv(file_path, header=None, delim_whitespace=True)
        plt.title(file_path)
        plotSpec(spec_curve,True)
        spec_curve.to_csv(".//t//" + file_path, sep = ' ',header=False, index=False)

