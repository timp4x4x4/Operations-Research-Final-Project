import numpy as np
import pandas as pd
import os
import math
import csv

stations_csv = pd.read_csv('被拔的站.csv')
stations = stations_csv.iloc[:, 0]

supply_xlsx = pd.read_csv('站供給.csv')
print(supply_xlsx)

village_xlsx= pd.read_excel('點座標.xlsx')
goStation_xlsx = pd.read_excel('GoStationPosition.xlsx')
print(goStation_xlsx)

goStations = dict()
for i in range(len(goStation_xlsx)):
    name = goStation_xlsx['站點名稱'][i]
    x = goStation_xlsx['x'][i]
    y = goStation_xlsx['y'][i]
    goStations[name] = [x, y]
  
left_stations = list()
for station in goStations.keys():
    if station not in stations:
        left_stations.append(station)  
        
def nearest_station(dot, goStations, restrict = []):
    x = dot[0]
    y = dot[1]
    nearest = float('inf')
    best_station = None
    for station_name, coordinates in goStations.items():
        if station_name in restrict:
            continue
        distance = math.sqrt((coordinates[0] - x)**2 + (coordinates[1] - y) ** 2)
        if distance < nearest:
            best_station = station_name
            nearest = distance
    return best_station

village = dict()
for i in range(len(village_xlsx)):
    dot = [village_xlsx['x(TM2)'][i], village_xlsx['y(TM2)'][i]]
    station_name = nearest_station(dot, goStations)
    if station_name not in village:
        village[station_name] = list()
    village[station_name].append(dot)    
print(village)
 
demand = dict()
supply = dict()
for name in goStations.keys():
    file_path = f'demand_supply/{name}demand_supply.csv'
    demand_and_supply = pd.read_csv(file_path)
    demand_ALL = list(demand_and_supply['Demand'])  
    supply_ALL = list(demand_and_supply['Supply'])
    demand[name] = demand_ALL
    supply[name] = supply_ALL
     
modify = dict()
for station in stations:
    if station not in village.keys():
        continue
    
    for v in village[station]:
        new_station = nearest_station(v, goStations, restrict=stations)

        for time in range(336):
            supply[new_station][time] -= demand[station][time] / len(village[station])
            print(supply[new_station][time])
             
print(len(left_stations))
for station in left_stations:
    filename = f"new_supply/{station}新供給.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["新供給"])
        print(len(supply[station]))
        for s in supply[station]:
            writer.writerow([s])
            
filename = "剩餘的站.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["剩餘的站"])
    for station in left_stations:
        writer.writerow([station])