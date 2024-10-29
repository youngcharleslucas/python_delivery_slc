import datetime
from status import Status
from package import TruckPackage

class Truck:
    def __init__(self, id, departureTime, packages):
        self.id = id 
        self.departureTime = departureTime
        self.returnTime = None
        self.miles = None
        self.packages = packages # Array of TruckPackage objects
        
    def __str__(self):
        return "Truck: %s, %s, %s, %s, %s " % (self.id, self.departureTime,\
        self.returnTime, self.miles, self.packages)
        
    def name(self):
        return "Truck: %s" % (self.id)
        
    def status(self, timeEntered):
        # Convert the string time to datetime type
        timeString = timeEntered.split(':')
        try:
            timeInt = [int(timeString[0]), int(timeString[1])]
        except: 
            return False 
        hours = timeInt[0] % 25 # eliminate values that would be > 24 hrs
        minutes = timeInt[1] % 60 # eliminate minutes > 59
        timeRequest = dateTime.datetime(2024, 1, 10, 8, 00, 00)
        timeRequest.replace(hour=hour, minute=minutes, second=00)
        
        # Compare truck location with time entered
        status = Status.EN_ROUTE.name
        if timeRequest < self.departureTime:
            status = Status.AT_HUB.name
        elif timeRequest >= self.returnTime:
            status = Status.AT_HUB.name
            
        return f"Truck {self.id}: \n Status: {status}" 
            
        
    def deliverPackages(self, packageHashTable):
        truckMileage = float(0)
        speed = float(60.0000) / float(18.0000) 
        for destination in self.packages:
            if int(destination.packageId) == int(0):
                truckMileage += float(destination.distance)
                timeTraveled = int(float(truckMileage) * speed)
                timeDelta = datetime.timedelta(minutes = timeTraveled)
                self.returnTime = self.departureTime + timeDelta
                
            else:
                # Get the package from the hashTable
                package = packageHashTable.search(destination.packageId)
                
                package.truck = self.id
                package.departureTime = self.departureTime
                # Add destination distance to total truckMileage
                truckMileage += float(destination.distance)
                timeTraveled = int(float(truckMileage) * speed)
                # Get Timedelta since departure
                timeDelta = datetime.timedelta(minutes = timeTraveled)
                package.deliveryTime = self.departureTime + timeDelta
                # Update package 
                packageHashTable.insert(package.id, package)
        self.miles = truckMileage
        
        
        
        
        