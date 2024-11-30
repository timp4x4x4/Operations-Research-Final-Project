import numpy as np
import pandas as pd
import os
import math
import csv

class GoStation:
    def __init__(self, station_id, name, position, demand, supply):
        self.station_id = station_id
        self.name = name
        self.position = position
        self.distant_order = list()
        self.demand = demand
        self.supply = supply
        self.left_battery = 0

    def get_distant_order(self, goStations):
        distant_order = [i for i in range(len(goStations))]
        
        my_position = self.position
        
        def calculate_distance(pos1, pos2):
            return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        
        def get_value(index):
            return calculate_distance(my_position, goStations[index].position)
        
        # Sort the station names based on their distance from the reference station
        sorted_order = sorted(distant_order, key=get_value)
        
        self.distant_order = sorted_order
        
    def find_some_help (self, ttl_help, goStations):
        total_helper = list()
        total_left_battery = self.left_battery
        one_to_one = False
        p = 0
        for helper in self.distant_order:
            lb = goStations[helper].left_battery
            p += lb  
            if helper == self.station_id:
                continue
            
            if lb > 0:
                if lb + self.left_battery >= 0: # one to one
                    goStations[helper].left_battery -= abs(self.left_battery)
                    self.left_battery = 0
                    one_to_one = True
                    break
                elif total_left_battery != 0: # many to one
                    if abs(total_left_battery) > lb:
                        total_left_battery += lb
                        total_helper.append([helper, lb])
                    else:
                        total_helper.append([helper, abs(total_left_battery)])
                        total_left_battery = 0
            else:
                continue
        
        if not one_to_one:
            if len(total_helper) == 0:
                print(f"need outer help {p}")
                ttl_help[0] += abs(self.left_battery)  # Modify the value in the list
            else:
                for elem in total_helper:
                    goStations[elem[0]].left_battery -= elem[1]
        self.left_battery = 0

                
stations_csv = pd.read_csv('剩餘的站.csv')
stations = stations_csv.iloc[:, 0]
print(stations)

goStation_xlsx = pd.read_excel('GoStationPosition.xlsx')
goStations_pos = dict()
for i in range(len(goStation_xlsx)):
    name = goStation_xlsx['站點名稱'][i]
    x = goStation_xlsx['x'][i]
    y = goStation_xlsx['y'][i]
    goStations_pos[name] = [x, y]

goStations = list()   
id = 0
for name in stations:
    file_path = f'new_supply/{name}新供給.csv'
    s_file_path = f'demand_supply/{name}demand_supply.csv'
    _demand = pd.read_csv(file_path)
    _supply = pd.read_csv(s_file_path)
    demand_ALL = list(_demand['新需求'])
    supply_ALL = list(_supply['Supply'])
    
    demand = [d / 7 for d in demand_ALL[:48]]
    supply = [s / 7 for s in supply_ALL[:48]]
    
    for i in range(48, len(demand_ALL)):
        demand[i % 48] += demand_ALL[i] / 7
        supply[i % 48] += supply_ALL[i] / 7
    goStations.append(GoStation(0, name, goStations_pos[name], demand, supply))
    id += 1

for goStation in goStations:
    goStation.get_distant_order(goStations)
    # print(goStation.demand)

ttl_help = [0]  # Encapsulate ttl_help in a list
for time in range(48):
    print(time)
    tmp = 0
    for goStation in goStations:
        goStation.left_battery = goStation.supply[time] - goStation.demand[time]
        print(goStation.left_battery)
        tmp += goStation.left_battery
    if (tmp <= 0):
        print('INFEASIBLE')
    for goStation in goStations:
        if (goStation.left_battery < 0):
            goStation.find_some_help(ttl_help, goStations)
            
print(ttl_help[0])  # Access the value inside the list
