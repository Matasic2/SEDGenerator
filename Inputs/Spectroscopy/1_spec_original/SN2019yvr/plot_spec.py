import os
import glob

import dataclasses
import pandas as pd
import matplotlib.pyplot as plt

from astropy.io import ascii
from astropy.table import Table

import numpy as np


for file_path in sorted(glob.glob(".//*")):
    print(file_path)
    if (file_path.endswith(".txt")):
        pdData = pd.read_csv(file_path)
        wavelen = pdData.iloc[:,0]
        fluxs = pdData.iloc[:,1]
        plt.plot(wavelen.to_numpy(),fluxs.to_numpy())
        plt.title(file_path)
        plt.show()
