import pandas as pd
import city as City
import random
from networkx.generators.random_graphs import erdos_renyi_graph

CITIES_DATA_SET = []
GRAPH = {}

# function for get the distance between two cities
def get_distance(city1, city2) :
    distance = ((city1.lat - city2.lat)**2 + (city1.lng - city2.lng)**2)**0.5
    distance = float("{:.2f}".format(distance))
    return distance


def create_DataSet():
    df = pd.read_csv("assets/Poistions/worldcities.csv")
    df.columns = ['city', 'city_ascii', 'lat', 'lng', 'country', 'iso2', 'iso3', 'admin_name', 'capital', 'population', 'id']
    df = df.drop(columns=['city','country', 'iso2', 'iso3', 'admin_name',  'population', 'id'])
    # print(df.to_string())

    # store the cities in list of cities
    rangec = 0
    for i in range(len(df)) : 
        if(df['capital'][i] == 'primary' and df['capital'][i] != None ) : 
            CITIES_DATA_SET.append(City.City(df['city_ascii'][i], df['lat'][i], df['lng'][i]))
            rangec +=1
    # print(CITIES_DATA_SET)
    # make graph from cities list 

    for i in range(len(CITIES_DATA_SET)) : 
        GRAPH[CITIES_DATA_SET[i].name] = []
        for j in range(random.randint(4,6)) :
            randomCity = int(random.randint(0, len(CITIES_DATA_SET) - 1) )
            if randomCity != i : 
                GRAPH[CITIES_DATA_SET[i].name].append((CITIES_DATA_SET[randomCity].name, get_distance(CITIES_DATA_SET[i], CITIES_DATA_SET[randomCity])))
            # else :
            #     GRAPH[CITIES_DATA_SET[i].name].append((CITIES_DATA_SET[randomCity +3].name, get_distance(CITIES_DATA_SET[i], CITIES_DATA_SET[randomCity+3])))
            # GRAPH[CITIES_DATA_SET[i].name][CITIES_DATA_SET[j + random.randint(0, )].name] = getDistance(CITIES_DATA_SET[i], CITIES_DATA_SET[j])
    # print(GRAPH)





# def lat_lng_to_pixels(lat, lng, zoom):
#     lat_rad = math.radians(lat)
#     n = 2.0 ** zoom
#     x = int((lng + 180.0) / 360.0 * n)
#     y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
#     return (x, y)

# def lat_lng_to_pixels(lat, lng, width, height):
#     lat_min = MIN_LAT  # Replace MIN_LAT with the minimum latitude value
#     lat_max = MAX_LAT  # Replace MAX_LAT with the maximum latitude value
#     lng_min = MIN_LNG  # Replace MIN_LNG with the minimum longitude value
#     lng_max = MAX_LNG  # Replace MAX_LNG with the maximum longitude value

#     lat_scale = height / (lat_max - lat_min)
#     lng_scale = width / (lng_max - lng_min)

#     lat_offset = (lat - lat_min) * lat_scale
#     lng_offset = (lng - lng_min) * lng_scale

#     return (lng_offset, lat_offset)