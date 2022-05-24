import os
from astropy.time import Time

a = os.listdir('./')
print(a)
for name in a:
    if(name.endswith(".txt")):
        times = name[:-4]
        print("////SN2020oi//" + name + " SN2020oi " + times + " 0.00524")
