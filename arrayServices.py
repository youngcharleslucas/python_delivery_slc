from package import Package, DeliveryTimeGroup, TruckPackage
import datetime

# Sorts packages by delivery deadline. The delivery deadline is represented by 
# a DeliveryTimeGroup object. The DeliveryTimeGroup object will store the package
# ids under the delivery deadline. The order of DeliveryTimeGroups is by highest 
# priority to lowest priority.
# Return: Array of DeliveryTimeGroup (package ids grouped by delivery deadline)
# Input:
#   array = an unordered array of Package objects
#   packagesByDeliveryTimeArray = Array of DeliveryTimeGroup. Default is a new
#       array, but an existing array can be updated if passed in.
def GroupPackagesByDeliveryTime(array, packagesByDeliveryTimeArray = []):
    for i in range(0, len(array)):
        package = array[i] # Grabs each packge from list linearly
        deadline = ''
        
        # Change time type for grouping
        if(package.deadline != 'EOD'):
            deadline = package.deadline.time()
        else:
            deadline = package.deadline
        # Put packages to be delivered together in a earlier priority
        if package.note != '':
            note = package.note.split()
            if len(note) > 1:
                if note[0] == 'Combine:':
                    deliveryTime = datetime.datetime(2024, 1, 10, 8, 00, 00)
                    deliveryTime = deliveryTime.replace(hour=9, minute=00, second=00, microsecond=00)
                    deadline = deliveryTime.time()
        # Put packages to be delivered together in truck 2 in a earlier priority
        if package.note != '':
            note = package.note.split()
            if len(note) > 1:
                if note[0] == 'Truck:' and package.deadline == 'EOD':
                    deliveryTime = datetime.datetime(2024, 1, 10, 8, 00, 00)
                    deliveryTime = deliveryTime.replace(hour=10, minute=30, second=00, microsecond=00)
                    deadline = deliveryTime.time()        
        if(len(packagesByDeliveryTimeArray) == 0): # Adds first package
            packagesByDeliveryTimeArray.append(DeliveryTimeGroup(deadline, [package.id]))
        else:
            match = False
            for time in packagesByDeliveryTimeArray:
                if(time.time == deadline):
                    time.packageIds.append(package.id)
                    match = True
                    break
            if(not match): # No time group exists for package, create new group
                packagesByDeliveryTimeArray.append(DeliveryTimeGroup(deadline, [package.id]))
             
    # Move EOD group to end of array
    for x in range(0, len(packagesByDeliveryTimeArray) - 1):
        if(type(packagesByDeliveryTimeArray[x].time) is str):
            tempLast = packagesByDeliveryTimeArray[len(packagesByDeliveryTimeArray) - 1] 
            packagesByDeliveryTimeArray[len(packagesByDeliveryTimeArray) - 1] = packagesByDeliveryTimeArray[x]
            packagesByDeliveryTimeArray[x] = tempLast
        
    # Sort the times from earliest deadline to latest, selection sort
    for t in range(0, len(packagesByDeliveryTimeArray) - 2):
        lowestIndex = t
        for j in range(t+1, len(packagesByDeliveryTimeArray) - 1):
            if(packagesByDeliveryTimeArray[j].time < packagesByDeliveryTimeArray[lowestIndex].time):
                lowestIndex = j
        if(lowestIndex != t):
            temp = packagesByDeliveryTimeArray[lowestIndex]
            packagesByDeliveryTimeArray[lowestIndex] = packagesByDeliveryTimeArray[t]
            packagesByDeliveryTimeArray[t] = temp
    return packagesByDeliveryTimeArray  
        
# Retruns a list of 16 + 1 TruckPackage objects. The final TruckPackage object
# is for returning to the WGU Hub. The method sorts through packagesGroupByTime
# array, grabbing all the packages in the current array of required delivery times 
# before moving to the next array of required delivery times.  
#    truck = empty array
#    packagesGroupByTime = Array of DeliveryTimeGroup objects. 
#    packagesHashT = Hash table containing Package objects stored by thier package id 
#    distanceM = Distance Matrix, which contains an array of DistanceRow objects
def LoadPackagesInTruck(truck, packagesGroupByTime, packagesHashT, distancesM):
    truck = []
    currentPackage = TruckPackage(0,1, float(30)) # Starts at WGU
    for time in packagesGroupByTime:        
        # Find the closest package location
        while len(time.packageIds) > 0 and len(truck) < 17:
            nextClosestPackage = TruckPackage(currentPackage.packageId, currentPackage.locationId, float(30))
            for packageId in time.packageIds:
                #Get distance from current location
                package = packagesHashT.search(packageId)
                locationId = 999
                if(package.updateLocation != None):
                    locationId = package.updateLocation.id
                else:
                    locationId = package.locationId
                distance = distancesM[currentPackage.locationId - 1].GetDistance(locationId)
                if float(distance) < float(nextClosestPackage.distance):
                    nextClosestPackage = TruckPackage(package.id, locationId, distance)
            updatedPackageIds = []
            # Add next closest package to truck, remove package id from list 
            truck.append(nextClosestPackage)   
            for packageId in time.packageIds:
                if packageId != nextClosestPackage.packageId:
                    updatedPackageIds.append(packageId)
            time.packageIds = updatedPackageIds
            if len(truck) > 15:
                break
            currentPackage.packageId = nextClosestPackage.packageId
            currentPackage.locationId = nextClosestPackage.locationId
        if len(truck) > 15:
            break
    # Return back to WGU 
    lastPackage = truck[len(truck)-1]
    distance = distancesM[lastPackage.locationId - 1].GetDistance(1)
    returnToWGU = TruckPackage(0, 0, distance)
    truck.append(returnToWGU)
    return truck
    
# List all packages. This is for option 1 of the main menu. Listing packages 
# shows what package ID can be entered for other menu options 
def ListPackages(packageHashTable):
    listOfPackages = ''
    for i in range(1, 41):
        package = packageHashTable.search(i)
        listOfPackages = listOfPackages + package.listPackage() + "\n"
    return listOfPackages
