import csv
import datetime
from location import Location, DistanceRow
from chainingHashTable import ChainingHashTable 
from package import Package
from status import Status 

# Imports a csv and returns an array of the csv
def ImportCsvToArray(fileName):
    importedArray = []
    with open(fileName) as csvFile:
        csvRows = csv.reader(csvFile, delimiter = ',')
        next(csvRows) #skips the header 
        index = 0
        for csvRow in csvRows:
            importedArray.append([])
            for j in range(len(csvRow)):
                importedArray[index].append(csvRow[j])
            index += 1
    return importedArray
    
# Imports the distance table from csv using the method ImportCsvArray, then 
# converts the imported distance rows to an array of DistanceRow objects. DistanceRow objects 
# contain the field location which holds a Location object representing a delivery
# destination. The other field in DistanceRowThe array is distances, which is an 
# array of floats representing the distance from the current location to other 
# locations. 
# Returns: Array of DistanceRow 
#   To find the index of a location in the table, use the locationId - 1 as the 
#   index for matrix. ex: matrix[locationId - 1]
def CreateDistanceMatrix():
    distancesCsv = ImportCsvToArray('Distances.csv') 
    matrix = []
    locations = []
    csvLength = len(distancesCsv) - 1
    index = 0
    for distanceCsv in distancesCsv: 
        location = Location(index + 1, distanceCsv[0], distanceCsv[1], distanceCsv[2])
        distanceRow = []
        j = 3
        while(True):
            distanceRow.append(float(distanceCsv[j]))
            if(float(distanceCsv[j]) == float(0.0)):
                break
            else:
                j += 1
                continue 
        k = index + 1
        while(k <= csvLength):
            distanceRow.append(float(distancesCsv[k][j]))
            k += 1
        matrix.append(DistanceRow(location, distanceRow)) 
        index += 1
    return matrix
    
# Imports packages from csv and loads them as Package objects into a hash table
# with unordered buckets. The sorting key used is the package id. The distance 
# matrix is passed in as a parameter. This is to assign a location id to each 
# package. This id will be used for looking up distances. Returns a hash table.
# of packages.
def LoadPackagesToHashTable(matrix):
    packageArray = ImportCsvToArray('Package.csv')
    hashTable = ChainingHashTable()
    for packageRow in packageArray:
        locationId = 999
        index = 0
        for row in matrix: 
            if (hash(row.location.street) == hash(packageRow[1])):
                locationId = row.location.id
                break
        deadline = 'XXX'
        if(packageRow[5] == 'EOD'):
            deadline = packageRow[5]
        else:
            timeString = packageRow[5].split(':')
            deadline = datetime.datetime(2024, 1, 10, 8, 00, 00)
            deadline = deadline.replace(hour=int(timeString[0]), minute=int(timeString[1].replace(" AM", "")), second=00)
        package = Package(int(packageRow[0]), int(locationId), packageRow[1], \
        packageRow[2], packageRow[3], packageRow[4], packageRow[6], deadline, \
        packageRow[7])
        
        note = packageRow[7].split()
        if(len(note) > 4):
            updateString = note[1].split(':')
            updateTime = datetime.datetime(2024, 1, 10, 8, 00, 00)
            updateTime = updateTime.replace(hour=int(updateString[0]), minute=int(updateString[1]), second=00)
            package.updateTime = updateTime
            package.updateLocation = matrix[int(note[4]) - 1].location
        hashTable.insert(package.id, package)
    return hashTable