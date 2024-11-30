import numpy as np
import pandas as pd
import os
import math
import csv
import random

supply_xlsx = pd.read_csv('站供給.csv')
print(supply_xlsx)

village_xlsx= pd.read_excel('點座標.xlsx')
goStation_xlsx = pd.read_excel('GoStationPosition.xlsx')
print(goStation_xlsx)

v_demand_xlsx = pd.read_csv('點需求.csv')
print(supply_xlsx)

goStations = dict()
for i in range(len(goStation_xlsx)):
    name = goStation_xlsx['站點名稱'][i]
    x = goStation_xlsx['x'][i]
    y = goStation_xlsx['y'][i]
    goStations[name] = [x, y]
    
def nearest_station(dot, goStations, restrict = []):
    x = dot[0]
    y = dot[1]
    nearest = float('inf')
    best_station = None
    for station_name, coordinates in goStations.items():
        if station_name in restrict:
            continue
        distance = math.sqrt((coordinates[0] - x) ** 2 + (coordinates[1] - y) ** 2)
        if distance < nearest:
            best_station = station_name
            nearest = distance
    # print(best_station)
    return best_station

village = dict()
for i in range(len(village_xlsx)):
    dot = [village_xlsx['x(TM2)'][i], village_xlsx['y(TM2)'][i], v_demand_xlsx['AVGdemand'][i]]
    station_name = nearest_station(dot, goStations)
    if station_name not in village:
        village[station_name] = list()
    village[station_name].append(dot)    
print(village)

maxBat_xlsx = pd.read_excel('新竹市站點.xlsx')
maxBat = dict()
for i in range(len(goStation_xlsx)):
    name = maxBat_xlsx['站點名稱'][i]
    bat = maxBat_xlsx['maxBat'][i]
    maxBat[name] = bat
print(maxBat)

supply = dict()
demand = dict()
for i in range(len(supply_xlsx)):
    supply[supply_xlsx['站名'][i]] = supply_xlsx['AVGSupply'][i]
    demand[supply_xlsx['站名'][i]] = maxBat[supply_xlsx['站名'][i]] - supply_xlsx['AVGSupply'][i]
    
stationNames = list(goStations.keys())

def get_value(name):
    return -supply[name] / maxBat[name]

sorted_station = sorted(stationNames, key=get_value)

for name in sorted_station:
    print(name, demand[name], maxBat[name])

def pop_element (station_name):
    if station_name in village.keys():
        village.pop(station_name)
    maxBat.pop(station_name)
    demand.pop(station_name)
    goStations.pop(station_name)
    
def plan (abandoned, station_name):
    restrict = abandoned + [station_name]
    if station_name not in village.keys():
        pop_element(station_name)
        return True
    floating_village = village[station_name]
    newValue_next_station = dict()
    new_Home = dict()
    for dot in floating_village:
        next_station = nearest_station(dot, goStations, restrict = restrict)
        if next_station not in newValue_next_station.keys():
            newValue_next_station[next_station] = 0
        if next_station not in new_Home.keys():
            new_Home[next_station] = list()
        newValue_next_station[next_station] += dot[2]
        new_Home[next_station].append(dot)
    
    for name in list(newValue_next_station.keys()):
        if demand[name] + newValue_next_station[name] > maxBat[name]:
            return False
        
    for name in list(newValue_next_station.keys()):
        demand[name] += newValue_next_station[name] 
        if name not in village.keys():
            village[name] = list()
        village[name] += new_Home[name]
    pop_element(station_name)
    return True

abandoned = []
for station in sorted_station:
    if (plan(abandoned, station)):
        abandoned += [station]
        print(station)
        
left_stations = list(goStations.keys())
for name in left_stations:
    print(name, demand[name], maxBat[name])

filename = "剩餘的站.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["剩餘的站"])
    for station in left_stations:
        writer.writerow([station])

filename = "被拔的站.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["被拔的站"])
    for station in abandoned:
        writer.writerow([station])

print(len(abandoned))
print(len(village))