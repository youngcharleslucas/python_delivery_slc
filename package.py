from status import Status

class Package:
    def __init__(self, id, locationId, address, city, state, zipcode, weight, deadline, note): 
        self.id = id
        self.locationId = locationId
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.deadline = deadline
        self.note = note
        self.status = Status.AT_HUB.name
        self.deliveryTime = None 
        self.departureTime = None 
        self.truck = None
        self.updateTime = None 
        self.updateLocation = None
        
        
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s " %\
        (self.id, self.locationId, self.address, self.city, self.state, \
        self.zipcode, self.weight, self.deadline, self.status,\
        self.deliveryTime, self.departureTime, self.truck, self.updateTime,\
        self.updateLocation, self.note)
    
    
    def packageStatus(self, timeEntered):
        deadLine = ""
        if self.deadline != 'EOD':
            deadLine = f"{self.deadline.strftime('%X')}"
        else:
            deadLine = f"{self.deadline}"
        deliveryTime = self.deliveryTime.strftime("%X")
        departureTime = self.departureTime.strftime("%X")
        deliveryString = ""
        if timeEntered < self.departureTime:
            tStatus = Status.AT_HUB.name
        elif timeEntered > self.deliveryTime: 
            tStatus = Status.DELIVERED.name
            deliveryString = f", DELIVERED AT: {deliveryTime}, DEPARTURE: {departureTime}, TRUCK: {self.truck}" 
        else: 
            tStatus = Status.EN_ROUTE.name
            deliveryString = f", DEPARTURE: {departureTime}, TRUCK: {self.truck}"
            
        if self.updateTime != None and self.updateTime < timeEntered:            
            return f"ID: {self.id}, {self.updateLocation.street}, {self.city}, {self.state}, {self.updateLocation.zipcode}\n\t" +\
            f"STATUS: {tStatus}, DEADLINE: {deadLine}" + deliveryString + f""
        else:
            return f"ID: {self.id}, {self.address}, {self.city}, {self.state}, {self.zipcode}\n\t" +\
            f"STATUS: {tStatus}, DEADLINE: {deadLine}" + deliveryString + f""
        
    def listPackage(self):
        deadLine = ""
        if self.deadline != 'EOD':
            deadLine = f"{self.deadline.strftime('%X')}"
        else:
            deadLine = self.deadline
        return f"ID: {self.id}, DEADLINE: {deadLine}, {self.address}, {self.city}, {self.state}, {self.zipcode}"
        
class DeliveryTimeGroup:
    def __init__(self, time, packageIds):
        self.time = time
        self.packageIds = packageIds 
        
    def __str__(self):
        return "%s, %s " % (self.time, self.packageIds)
        
class TruckPackage:
    def __init__(self, packageId, locationId, distance):
        self.packageId = packageId
        self.locationId = locationId
        self.distance = distance
        
    def __str__(self):
        return "PackageId: %s, LocationId: %s, Distance From Previous: %s" % (self.packageId, self.locationId, self.distance)