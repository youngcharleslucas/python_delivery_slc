class Location:
    def __init__(self, id, location, street, zipcode):
        self.id = id
        self.location = location
        self.street = street 
        self.zipcode = zipcode 
        
    def __str__(self):
        return "%s, %s, %s, %s " % (self.id, self.location, self.street, self.zipcode)

# This represenst a row in the distance matrix object
class DistanceRow:
    def __init__(self, location, distances):
        self.location = location 
        self.distances = distances 
        
    def __str__(self):
        return "%s, %s, %s, %s " % (self.location.id, self.location.street, self.location.zipcode, self.distances)
        
    def GetDistance(self, locationId):
        return self.distances[locationId - 1]