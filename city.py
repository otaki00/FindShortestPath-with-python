# create class city 
import math
import pyproj
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


class City : 
    def __init__(self, name, lat, lng) : 
        self.name = name
        self.lat = lat
        self.lng = lng
        self.x = 0
        self.y = 0
        self.set_x_y()
    
    def set_x_y(self) : 
        # convert to pixel offset depending on width and height
        width = 950
        height = 700
        self.x = (self.lng + 167.0) * (width / 360)
        self.y = (115 - self.lat ) * (height / 180)
        # use pyproj to convert lat and lng to x and y
        # src_proj = pyproj.Proj(proj='latlong', datum='WGS84')
        
        # tgt_proj = pyproj.Proj(proj='merc', lat_ts=0, lat_0=0, lon_0=0, x_0=0, y_0=0, datum='WGS84')
        
        # self.x , self.y = pyproj.transform(src_proj, tgt_proj, self.lng, self.lat)
        # self.x = (self.lng * 3.6666) + 950
        # self.y = (self.lat * 3.6666) + 700
        # lat_min = -90  # Replace MIN_LAT with the minimum latitude value
        # lat_max = 90  # Replace MAX_LAT with the maximum latitude value
        # lng_min = -180  # Replace MIN_LNG with the minimum longitude value
        # lng_max = 180 # Replace MAX_LNG with the maximum longitude value
        # width = 950
        # height = 700
        # lat_scale = height / (lat_max - lat_min)
        # lng_scale = width / (lng_max - lng_min)

        # self.y = (self.lat - lat_min) * lat_scale
        # self.x = (self.lng - lng_min) * lng_scale
        
        # set x and y for map
        # self.x = (self.lng * 3.6666) + 950
        # self.y = (self.lat * 3.6666) + 700
    
    def __str__(self) : 
        return f"{self.name} -  {self.x} - {self.y}"