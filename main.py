# Student ID: 011058934

import csv 
import math
import datetime
from package import Package, DeliveryTimeGroup, TruckPackage
from status import Status   
from chainingHashTable import ChainingHashTable    
from dataImportServices import ImportCsvToArray, CreateDistanceMatrix, LoadPackagesToHashTable
from location import Location, DistanceRow 
from arrayServices import GroupPackagesByDeliveryTime, LoadPackagesInTruck, ListPackages  
from truck import Truck    
from uiService import MainMenu, ViewPackageStatus

# Imports the distances between destinations from a csv and put them in a matrix. 
# The matrix is an array of DistanceRow objects. DistanceRow have a location field 
# (Location object) and distances field (array of distances). The ineex of the 
# distance correspondes to the Location.id - 1
# ---------Requirement B----------------
# The DistanceRow object has a method called GetDistance(locationId) that will return the 
# distance from the current location in the DistanceRow to the requested locationId.
distanceMatrix = CreateDistanceMatrix()

# ---------Requirement A----------------
# Imports packages from csv and store them as Package objects in a hash table. 
# Packages are inserted into buckets using the package id as the key.
packageHashTable = LoadPackagesToHashTable(distanceMatrix)

# -----Disperse packages to trucks------
# Put package ids into a matrix orderd by delivery time. Organizing packages by 
# delivery deadline will ensure that packages are delivered before their deadline.
# But prior to that:
# Packages are moved to an array to simplifiy iteration and comparison of delivery 
# deadlines, delays, and other delivery notes 
arrayOfPackages = packageHashTable.toArray()
# ------Load Truck 1--------------------
# Truck 1 will be the early morning delivery truck. It will prioritize packages 
# that have an early delivery deadline. Remaining space in the truck will go to 
# EOD packages. Included in this truck will be packages 13,14,15,16,19 and 20
# since they have the requirement of being delivered together. This truck will 
# depart at 8 am

# Build an array of packages available for morning delivery (no delays or 
# special requests)
packagesCombined = []
for p in arrayOfPackages:
    note = p.note.split()
    if len(note) > 0:
        if note[0] == 'Combine:':
            packagesCombined.append(p)
    if p.note == '':
        packagesCombined.append(p)
'''        
def PrintTruck(times):
    for time in times:
        print(time.time)
        print(time.packageIds)
'''
# Group the packages with no notes into an array prioritizing delivery deadlines. 
# The method GroupPackagesByDeliveryTime will return an array of DeliveryTimeGroup
# objects. This object contains the required delivery time as the field time and 
# an array of package ids to be delivered by that time in the field packageIds.
# The DeliveryTimeGroup with the earlier delivery time will be at the front of the 
# array while EOD packages will be at the tail of the array. The contents of 
# packageIds are unordered.
packagesByTime = GroupPackagesByDeliveryTime(packagesCombined)
truck_empty = []
truck_1 = LoadPackagesInTruck(truck_empty, packagesByTime, packageHashTable, distanceMatrix)

# ------Load Truck 2--------------------
# Find packages that have to go on truck 2 with note "Truck:" or a delay 
# with 9. Packages 3,18, 36, and 38 are required to be on this truck. This truck 
# leaves at 9:05.
truck2Required = []
for p in arrayOfPackages:
    note = p.note.split()
    if len(note) > 0:
        if note[0] == 'Truck:' or int(note[1][0]) == int(9):
            truck2Required.append(p)

# Make room for packages requiring delivery on truck 2
packagesByTime = GroupPackagesByDeliveryTime(truck2Required, packagesByTime)
truck_2 = LoadPackagesInTruck(truck_empty, packagesByTime, packageHashTable, distanceMatrix)

# ------Load Truck 3--------------------
# All remaining packages. This truck leaves at 10:20 after package 9's address 
# has been updated 
remainingPackages = []
for p in arrayOfPackages:
    note = p.note.split()
    if len(note) > 0:
        if note[0] == 'Delay:' and int(note[1][0]) == int(1):
            remainingPackages.append(p)
        elif note[0] == 'Update:':
            remainingPackages.append(p)
            
packagesByTime = GroupPackagesByDeliveryTime(remainingPackages, packagesByTime)
truck_3 = LoadPackagesInTruck(truck_empty, packagesByTime, packageHashTable, distanceMatrix)
# Truck 1
departure = datetime.datetime(2024, 1, 10, 8, 00, 00)
departure = departure.replace(hour=8, minute=0, second=00)
truck1 = Truck(1, departure, truck_1)
truck1.deliverPackages(packageHashTable)

# Truck 2
departure = datetime.datetime(2024, 1, 10, 8, 00, 00)
departure = departure.replace(hour=9, minute=5, second=00)
truck2 = Truck(2, departure, truck_2)
truck2.deliverPackages(packageHashTable)

# Truck 3
departure = datetime.datetime(2024, 1, 10, 8, 00, 00)
departure = departure.replace(hour=10, minute=20, second=00)
truck3 = Truck(3, departure, truck_3)
truck3.deliverPackages(packageHashTable)

#--------UI------------------------------------

print(\
"---------------------------------------------------\n\
|                                                 |\n\
|             WGUPS Routing Program               |\n\
|                                                 |\n\
---------------------------------------------------\n")

MainMenu(packageHashTable, [truck1, truck2, truck3], distanceMatrix)
            