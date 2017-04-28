import numpy as np


d = np.load("data.npz")
d2 = np.load("data2.npz")


img = list(d['image'])+list(d2['image'])
spd = list(d['speed'])+list(d2['speed'])
ang = list(d['angle'])+list(d2['angle'])

print(len(img))
print(len(spd))
print(len(ang))


np.savez("new_data.npz",image= img, speed = spd, angle=ang )
