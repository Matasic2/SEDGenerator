import os
from astropy.time import Time

a = os.listdir('./')
print(a)
for name in a:
    if(name == "New Text Document.py" or name.endswith(".flm")):
        continue
    #print(name[:-4])
    #print(name[-14:-4])
    times = name[-14:-4]
    t = Time(times, format='isot', scale='utc')
    #print(t.mjd)
    print("////SN2020oi//" + name + " SN2020oi " + str(t.mjd) + " 0.00524")
