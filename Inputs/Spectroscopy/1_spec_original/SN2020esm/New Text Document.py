import os
from astropy.time import Time

a = os.listdir('./')
print(a)
for name in a:
    if(name.endswith(".txt")):
        times = name[:-4]
        print("////SN2020esm//" + name + " SN2020esm " + times + " 0.036")
