import datetime
from arrayServices import ListPackages  

def MainMenu(packageHashTable, trucks, destinationM):
    mainMenu = "\
Select option below:\n\
1. List packages\n\
2. List locations\n\
3. Package status\n\
4. Truck status\n\
5. Exit\n"

    EXIT = False
    while EXIT == False: 
        userInput = input(mainMenu)
        try:
            userInput = int(userInput)
            print("\n")
        except: 
            print("Invalid input. Please enter a number from the menu and press 'Enter'/'Return'")
            continue
        if(userInput == 1):
            print(ListPackages(packageHashTable))
        if(userInput == 2):
            print("LOCATIONS:\n")
            for i in range(0, len(destinationM)):
                print("ID:",destinationM[i].location)
            print("\n")
        if(userInput == 3):
            ViewPackageStatus(packageHashTable)
        if(userInput == 4):
            TruckOptions(packageHashTable, trucks)
        if(userInput == 5):        
            EXIT = True
    print("End of program")
    
def ViewPackageStatus(packageHashTable):
    packageOrAllOption = "\
Would you like to view the status of one package or all packages?\n\
1. Single package\n\
2. All packages\n\
3. Return to main menu\n"
    EXIT = False
    while EXIT == False:
        userInput = input(packageOrAllOption)
        try:
            userInput = int(userInput)
        except: 
            print("Invalid input. Please enter a number from the menu and press 'Enter'/'Return'")
            continue
        if(userInput == 1):
           EXIT = ViewSinglePackageStatus(packageHashTable)
           print("\n")
        if(userInput == 2):
            EXIT = ViewAllPackagesStatus(packageHashTable)
            print("\n")
        if(userInput == 3):
            EXIT = True
            
def ViewAllPackagesStatus(packageHashTable):
    message = "\
Enter a time to view that status of all packages during that time. Else enter \
nothing to view the current status of all packages.\n\
(time format XX:XX, hours 00-24)\n"
    EXIT = False
    while EXIT == False:
        print("\n")
        userInput = input(message)
        print("\n")
        requestTime = datetime.datetime(2024, 1, 10, 8, 00, 00)
        try:
            
            if userInput == '':
                requestTime = requestTime.replace(hour=20, minute=00, second=00)
            else:
                userInput = userInput.split(":")
                hours = int(userInput[0])
                minutes = int(userInput[1])
                requestTime = requestTime.replace(hour=hours, minute=minutes, second=00)
        except:
            print("Incorrect time or time format, try again\n\n")
            continue
        for i in range(1, 41):
            package = packageHashTable.search(i)
            print(package.packageStatus(requestTime))
        EXIT = True
        print("\n")
    return True
    
def ViewSinglePackageStatus(packageHashTable):
    idMessage = "Enter the package number: "
    timeMessage = "\
Enter a time to view that status of all packages during that time. Else enter\
nothing to view the current status of all packages.\n\
(time format XX:XX, hours 00-24)\n"
    EXIT = False
    while EXIT == False:
        print("\n")
        userIdInput = input(idMessage)
        userTimeInput = input(timeMessage)
        print("\n")
        requestTime = datetime.datetime(2024, 1, 10, 8, 00, 00)
        try:   
            userIdInput = int(userIdInput)
            if userIdInput < 1 or userIdInput > 40:
                raise TypeError("Invalid package id. Choose an id between 1-40\n")
            if userTimeInput == '':
                requestTime = requestTime.replace(hour=20, minute=00, second=00)
            else:
                userTimeInput = userTimeInput.split(":")
                hours = int(userTimeInput[0])
                minutes = int(userTimeInput[1])
                requestTime = requestTime.replace(hour=hours, minute=minutes, second=00)
        except:
            print("Incorrect time or package id, try again\n")
            continue
        package = packageHashTable.search(userIdInput)
        print(package.packageStatus(requestTime))
        EXIT = True
    return True
    
def TruckStatus(trucks):
    display = "\
Truck        Departaure      Return       Miles\n\
-------------------------------------------------------\n"
    totalMiles = float(0)
    for truck in trucks:
        departure = truck.departureTime.strftime("%X")
        returnTime = truck.returnTime.strftime("%X")
        miles = "%.1f" % truck.miles
        totalMiles = totalMiles + truck.miles
        
        
        row = f"\
Truck {truck.id}      {departure}       {returnTime}       {miles}\n"
        display = display + row
    totalMiles = "%.1f" % totalMiles
    endRow = f"\n\
Total miles: {totalMiles}\n"
    display = display + endRow 
    print(display)
    print("\n")
    return True
        
def TruckRoute(packageHashTable, trucks):
    timeMessage = "\
Enter a time to view that status the truck. Else enter nothing to view the current \n\
status of the truck. (time format XX:XX, hours 00-24):\n"
    EXIT = False
    while EXIT == False:
        userTruckInput = input("Select a truck (1/2/3): ")
        userTimeInput = input(timeMessage)
        print("\n")
        requestTime = datetime.datetime(2024, 1, 10, 8, 00, 00)
        try:   
            userTruckInput = int(userTruckInput)
            if userTruckInput < 1 or userTruckInput > 3:
                raise TypeError("Invalid truck id. Choose an id between 1-3\n")
            if userTimeInput == '':
                requestTime = requestTime.replace(hour=20, minute=00, second=00)
            else:
                userTimeInput = userTimeInput.split(":")
                hours = int(userTimeInput[0])
                minutes = int(userTimeInput[1])
                requestTime = requestTime.replace(hour=hours, minute=minutes, second=00)
        except:
            print("Incorrect time or truck id, try again.\n")
            continue
        truck = trucks[int(userTruckInput) - 1]
        departureString = truck.departureTime.strftime("%X")
        returnTime = ''
        if requestTime >= truck.returnTime:
            returnTime = truck.returnTime.strftime("%X")
        else:
            returnTime = '---'
        display = f"\
Truck: {truck.id}\n\
Departure time: {departureString}\n\
Return time: {returnTime}\n\
Route: \n\n\
PACKAGE ID  | DELIVERY TIME | LOCATION ID | DISTANCE | TOTAL DISTANCE\n\
----------------------------------------------------------------------\n"
        totalDistance = float(0)
        for tPackage in truck.packages:
            if tPackage.packageId != 0:
                package = packageHashTable.search(tPackage.packageId)
                packageId = ''
                if package.id < 10:
                    packageId = "0" + str(package.id)
                else:
                    packageId = package.id
                packageDistanceTotal = float(0)
                packageDistanceTotalString = ''
                deliveryM = ''
                locationId = package.locationId
                if package.updateTime != None and package.updateTime < requestTime:
                    locationId = package.updateLocation.id
                locationIdString = locationId
                if locationId < 10:
                    locationIdString = "0" + str(locationId)
                else:
                    locationIdString = str(locationId)
                if package.deliveryTime < requestTime:
                    deliveryM = package.deliveryTime.strftime("%X")
                    packageDistanceTotal = totalDistance + tPackage.distance
                    totalDistance = packageDistanceTotal
                    packageDistanceTotalString = "%.1f" % packageDistanceTotal
                else:
                    deliveryM = '--------'
                    packageDistanceTotalString = '----'
                row = f"\
{packageId}              {deliveryM}         {locationIdString}           {tPackage.distance}           {packageDistanceTotalString}\n"
                display = display + row 
            else:
                print(display)
                EXIT = True
                return True


def TruckOptions(packageHashTable, trucks):
    message = f"\
1. View summary of truck mileage\n\
2. View truck route\n"
    EXIT = False
    while EXIT == False:
        userInput = input(message)
        try:   
            userInput = int(userInput)
            if userInput < 1 or userInput > 2:
                raise TypeError("Invalid option. Choose between 1-2\n")
        except:
            print("Incorrect option, try again.\n")
            continue
        if userInput == 1:
            EXIT = TruckStatus(trucks)
        elif userInput == 2:
            EXIT = TruckRoute(packageHashTable, trucks)
        else:
            EXIT = True
            return EXIT
            
