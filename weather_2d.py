# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as mplimg
from secrets import api_key
import requests
import time
import json
import pickle

def retrieve_weather_data(offline=True, pickle_response=False):
    '''
    Retrieve data from Open Weather Map API
    '''
    if offline:
        with open(file="temps.p", mode="rb") as fh:
            temps = pickle.load(fh)
        return temps
    else:
        step_length = 10
        lat_min = -90
        lat_max = 90
        lon_min = -180
        lon_max = 180
        ind = 0
        ind_max = int( (lon_max-lon_min)*(lat_max-lat_min) / step_length**2 )
        temps = []
        for lat in range(-90, 90, step_length):
            lon_row = []
            for lon in range(-180, 180, step_length):
                print( "Processing ", ind, "of", ind_max, "..." )
                parameters = {
                    "APPID": api_key,
                    "lon": lon,
                    "lat": lat,
                    "units": "metric"
                }
                response = requests.request(method="POST", url="https://api.openweathermap.org/data/2.5/weather", params=parameters)
                lon_row.append( json.loads(response.text)["main"]["temp"] )
                time.sleep(1.0)
                ind += 1
            temps.append( lon_row )
        
        if pickle_response:
            with open(file="temps.p", mode="wb") as fh:
                pickle.dump(temps, fh)

        return temps

temps = retrieve_weather_data(offline=True, pickle_response=False)

print( "Creating heatmap ..." )

ext = np.min([-180, 180]), np.max([-180, 180]), np.min([-90, 90]), np.max([-90, 90])
fig = plt.figure(frameon=False)


map_img = mplimg.imread("/home/tobias/Pictures/whole_range_dark.png")
im1 = plt.imshow(map_img, interpolation='bilinear',  aspect="equal", extent=ext)

temps = np.array(temps)
im2 = plt.imshow(temps, cmap=plt.cm.magma, alpha=.5, interpolation='bilinear',  origin="lower", extent=ext)
ax = plt.axis([-180, 180, -90, 90])
print("Displaying heatmap ...")
plt.show()
print("Shutting down ...")
