# -*- coding: utf-8 -*-

# https://openweathermap.org

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from secrets import api_key
import requests
import time
import json
import pickle
import matplotlib
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

def farenheit_to_celcius(temp):
    return (temp - 32)*5/9

np.random.seed(125)

lats = np.random.randint(-90, 90, size=500)
longs = np.random.randint(-180, 180, size=500)

coords = pd.DataFrame({
    "latitude": lats,
    "longitude": longs
})

'''
Retrieve data from Open Weather Map API
'''
# responses = []
# for i, coord in coords.iterrows():
#     print("processing: ", i, " ...")
#     parameters = {
#         "APPID": api_key,
#         "lon": coord["longitude"],
#         "lat": coord["latitude"],
#         "units": "metric"
#     }
#     response = requests.request(method="GET", url="http://api.openweathermap.org/data/2.5/weather", params=parameters)
#     responses.append( response )
#     time.sleep(1.0)

# with open(file="responses.p", mode="wb") as f:
#     pickle.dump(obj=responses, file=f)
# exit()


with open(file="responses.p", mode="rb") as f:
    responses = pickle.load(f)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d" )

xs = []
ys = []
zs = []
for response in responses:
    datum = json.loads(response.text)
    xs.append( datum["coord"]["lon"] )
    ys.append( datum["coord"]["lat"] )
    zs.append( datum["main"]["temp"] )

minima = min(zs)
maxima = max(zs)
nor = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)

ax.scatter(xs, ys, zs, c=zs, cmap="RdYlBu_r", norm=nor )
ax.set_xlabel('longitude')
ax.set_ylabel('latitude')
ax.set_zlabel('temperature (degrees C)')
ax.axis([-180, 180, -90, 90])

plt.show()
