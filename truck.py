import csv

from distance import addressTable
from package import Packages
import datetime

distanceData = list(csv.reader(open('data/distanceData.csv'), delimiter=','))

# Method to find closest destination using list comprehension, receives destination
# list and current position as parameters.
# O(N)
def findDestination(currentPosition, destinations):
    
    position = int(currentPosition)
    closestDistance = 15.0
    closestLocation = None
    n = 0
    distanceCalc = distanceData[position][int(n)]
    distanceCalc = float(distanceCalc)

    for distance in [x for x in destinations if int(x) < position]:

        if distanceCalc < float(closestDistance) and distance in destinations:
            closestLocation = distance
            closestDistance = distanceData[position][int(distance)]

    for distance in [x for x in destinations if int(x) > position]:

        if distanceCalc < float(closestDistance) and distance in destinations:
            closestLocation = distance
            closestDistance = distanceData[int(distance)][position]

    return closestLocation, closestDistance


def distanceHome(start):
    
    return float(distanceData[int(start)][0])

# Method that prints simple package report
# O(1)
def individualPackageReport(id=None):
    
    package = Truck.packageList.get(str(id))
    print(package)


class Truck:

    # Method that creates reports for each package and a more general report based on a timestamp.
    # Adds either a timestamp for the delivery or "At Hub" or "Out for delivery" to each package's list
    # O(N)
    def packageReport(self, id=None):

        if id is None:

            for index in range(1, 41):

                self.package = Truck.packageList.get(str(index))

                if self.deliveries[index] is not None:

                    self.package.append(str(self.deliveries[index]))

                elif (int(index) in self.truck2Packages and self.truck1Away) or (int(index) in self.truck2Packages and
                        self.truck2Away) or (int(index) in self.truck3Packages and self.truck3Away):

                    self.package.append("Out for Delivery")

                else:

                    self.package.append("At Hub")

                print(self.package)
                self.package.pop()
        else:

            self.package = Truck.packageList.get(str(id))

            if self.deliveries[id] is not None:

                self.package.append(str(self.deliveries[id]))

            elif (int(id) in self.truck2Packages and self.truck1Away) or (int(id) in self.truck2Packages and
                                                                          self.truck2Away) or (
                    int(id) in self.truck3Packages and self.truck3Away):

                self.package.append("Out for Delivery")

            else:

                self.package.append("At Hub")

            print(self.package)
            self.package.pop()

        return

    # Static variables
    packageList = Packages().hash_table

    # Creates a global variable for truck speed for distance calculations
    global speed
    speed = 18 / 60

    # init method that calls the truckAttributes method to set all variables
    # O(1)
    def __init__(self):

        self.truckAttributes()

    # method that initializes variables used in the program and sets package lists for trucks
    # O(1)
    def truckAttributes(self):

        self.deliveries = [None] * 41

        self.truck1Home = False
        self.truck2Home = False
        self.truck3Home = False

        self.truck1Away = False
        self.truck2Away = False
        self.truck3Away = False

        self.truck1Distance = 0.0
        self.truck2Distance = 0.0
        self.truck3Distance = 0.0

        self.truck1DestinationList = []
        self.truck2DestinationList = []
        self.truck3DestinationList = []

        self.truck1DestinationPriorityList = []
        self.truck2DestinationPriorityList = []
        self.truck3DestinationPriorityList = []

        self.truck1Position = 0
        self.truck2Position = 0
        self.truck3Position = 0

        self.truck1CurrentPosition = 0.0
        self.truck2CurrentPosition = 0.0
        self.truck3CurrentPosition = 0.0

        self.truck1NextDelivery = 0.0
        self.truck2NextDelivery = 0.0
        self.truck3NextDelivery = 0.0

        self.truck1Packages = [13, 14, 15, 16, 19, 29, 30, 31, 34, 37, 40, 1, 4, 7, 39, 8]
        self.truck2Packages = [3, 18, 36, 38, 6, 10, 11, 12, 17, 20, 21, 22, 23, 24, 25, 26]
        self.truck3Packages = [9, 27, 28, 33, 35, 2, 5, 32]

        self.truck1PackagePriority = [13, 14, 15, 16, 29, 30, 31, 34, 37, 40]
        self.truck2PackagePriority = [6, 20, 25]
        self.truck3PackagePriority = []

        Truck.packageList.add("9", ['9', '300 State St', 'Salt Lake City', 'UT', '84103', 'EOD', '2',
                                    'Wrong address listed'])

    # Method that returns total mileage for all three trucks
    # O(1)
    def getDistance(self):

        return float(self.truck1Distance + self.truck2Distance + self.truck3Distance)

    # Method that "loads" the packages onto each truck.  Packages for each truck have been preset
    # in the truckAttributes method
    # O(N)
    def loadPackages(self):

        for i in self.truck1Packages:

            address = Truck.packageList.get(str(i))[1]
            addressId = addressTable.get(address)[0]

            if addressId not in self.truck1DestinationList:

                self.truck1DestinationList.append(addressId)

                if i in self.truck1PackagePriority:
                    self.truck1DestinationPriorityList.append(addressId)

        for i in self.truck2Packages:

            address = Truck.packageList.get(str(i))[1]
            addressId = addressTable.get(address)[0]

            if addressId not in self.truck2DestinationList:

                self.truck2DestinationList.append(addressId)

                if i in self.truck2PackagePriority:
                    self.truck2DestinationPriorityList.append(addressId)

        for i in self.truck3Packages:

            address = Truck.packageList.get(str(i))[1]
            addressId = addressTable.get(address)[0]

            if addressId not in self.truck3DestinationList:

                self.truck3DestinationList.append(addressId)

                if i in self.truck3PackagePriority:
                    self.truck3DestinationPriorityList.append(addressId)

    # Removes packages from the delivery list for each truck for each location once
    # the current location is equivalent to the package address
    # O(N)
    def unloadTruck(self, truck_list, priority_list, location):

        self.removal_list = []

        for i in truck_list:

            address = Truck.packageList.get(str(i))[1]
            addressId = addressTable.get(address)[0]

            if addressId == str(location):
                self.removal_list.append(i)
                self.deliveries[i] = self.currentTime.time()

        for item in self.removal_list:

            truck_list.remove(item)

            if item in priority_list:
                priority_list.remove(item)

    # Method that handles selection of delivery locations for each of the three trucks
    # Calls the find destination method repeatedly as long as packages remain on each truck
    # O(N^2)
    def deliveryMethod(self, time="22:00"):

        # Sets time that deliveries start and creates an instance of loadPackages
        self.endTime = datetime.datetime.strptime(time, '%H:%M').time()
        self.currentTime = datetime.datetime.strptime('08:00', '%H:%M')
        self.loadPackages()

        # Sets the initial next destination for all trucks 
        # If there is a priority package on the truck, then the closest priority package is selected
        if len(self.truck1DestinationPriorityList) > 0:

            self.truck1NextLocation = findDestination(self.truck1Position,
                                                      self.truck1DestinationPriorityList)

        elif len(self.truck1DestinationList) > 0:

            self.truck1NextLocation = findDestination(self.truck1Position,
                                                      self.truck1DestinationList)

        if len(self.truck2DestinationPriorityList) > 0:

            self.truck2NextLocation = findDestination(self.truck2Position,
                                                      self.truck2DestinationPriorityList)

        elif len(self.truck2DestinationList) > 0:

            self.truck2NextLocation = findDestination(self.truck2Position,
                                                      self.truck2DestinationList)

        if len(self.truck3DestinationPriorityList) > 0:

            self.truck3NextLocation = findDestination(self.truck3Position,
                                                      self.truck3DestinationPriorityList)

        elif len(self.truck3DestinationList) > 0:

            self.truck3NextLocation = findDestination(self.truck3Position,
                                                      self.truck3DestinationList)

        self.truck1NextDelivery = float(self.truck1NextLocation[1])
        self.truck2NextDelivery = float(self.truck2NextLocation[1])
        self.truck3NextDelivery = float(self.truck3NextLocation[1])
        self.truck1Away = True

        # Loop runs while a truck still has a package on it
        # Trucks deliver priority items first
        # Loop is broken when all truck lists are empty
        # Loop also can end if the time based stop point is reached
        while not ((len(self.truck1DestinationList) < 1 and len(self.truck2DestinationList) < 1 and len(
                self.truck3DestinationList) < 1) or (self.currentTime.time() >= self.endTime)):

            # increments time by a minute each loop
            self.currentTime += datetime.timedelta(minutes=1)

            # Sends off truck 2 and 3 at certain triggers
            if self.currentTime.time() == datetime.datetime.strptime('09:05:00', '%H:%M:%S').time():
                self.truck2Away = True
            # Sends out Truck 3 to deliver only once truck 1 is at the hub and a certain time has been reached
            # in the loop
            if self.truck1Home and self.currentTime.time() >= datetime.datetime.strptime('10:20:00', '%H:%M:%S').time():
                Truck.packageList.add("9", ["9", "410 S State St", "Salt Lake City", "UT", "84111", "EOD", "2", "None"])
                self.truck3Away = True

            # Handles different destinations for all three trucks
            # Selects the destination in the list, then "unloads" the package
            # when the truck is at the destination.  Once the priority list and the
            # destination list are empty, sets truckAway to False to return truck to hub.
            if self.truck1CurrentPosition >= self.truck1NextDelivery:

                self.truck1CurrentPosition -= self.truck1NextDelivery
                # Sets trucks position to the next location in the destination list
                self.truck1Position = self.truck1NextLocation[0]
                # Calls unloadTruck method to remove package from list at current position
                self.unloadTruck(self.truck1Packages, self.truck1PackagePriority, self.truck1Position)
                # Removes destination from list
                self.truck1DestinationList.remove(self.truck1NextLocation[0])
                # Truck "Delivers" priority packages first
                if len(self.truck1DestinationPriorityList) > 0:

                    self.truck1DestinationPriorityList.remove(self.truck1NextLocation[0])
                # Calls findDestination method to find the next position in the priority list as long as there are more
                # packages in said list to deliver, if not, moves to destination list
                if len(self.truck1DestinationPriorityList) > 0:

                    self.truck1NextLocation = findDestination(self.truck1Position, self.truck1DestinationPriorityList)

                elif len(self.truck1DestinationList) > 0:

                    self.truck1NextLocation = findDestination(self.truck1Position, self.truck1DestinationList)

                elif len(self.truck1DestinationList) < 1 and self.truck1NextLocation[0] != 0:

                    self.truck1DestinationList.append(0)
                    self.truck1NextLocation = (0, distanceHome(self.truck1Position))

                self.truck1NextDelivery = float(self.truck1NextLocation[1])

            # If no remaining deliveries, sets truckHome boolean to true
            if len(self.truck1DestinationList) < 1:
                self.truck1Home = True

            if not self.truck1Home and self.truck1Away:
                self.truck1CurrentPosition += speed
                self.truck1Distance += speed

            # Truck 2
            if self.truck2CurrentPosition >= self.truck2NextDelivery:

                self.truck2CurrentPosition -= self.truck2NextDelivery
                self.truck2Position = self.truck2NextLocation[0]
                self.unloadTruck(self.truck2Packages, self.truck2PackagePriority, self.truck2Position)
                self.truck2DestinationList.remove(self.truck2NextLocation[0])

                if len(self.truck2DestinationPriorityList) > 0:
                    self.truck2DestinationPriorityList.remove(self.truck2NextLocation[0])

                if len(self.truck2DestinationPriorityList) > 0:

                    self.truck2NextLocation = findDestination(self.truck2Position, self.truck2DestinationPriorityList)

                elif len(self.truck2DestinationList) > 0:

                    self.truck2NextLocation = findDestination(self.truck2Position, self.truck2DestinationList)

                elif len(self.truck2DestinationList) < 1 and self.truck2NextLocation[0] != 0:

                    self.truck2DestinationList.append(0)
                    self.truck2NextLocation = (0, distanceHome(self.truck2Position))

                self.truck2NextDelivery = float(self.truck2NextLocation[1])

            if len(self.truck2DestinationList) < 1:
                self.truck2Home = True

            if not self.truck2Home and self.truck2Away:
                self.truck2CurrentPosition += speed
                self.truck2Distance += speed

            # Truck 3
            if self.truck3CurrentPosition >= self.truck3NextDelivery:

                self.truck3CurrentPosition -= self.truck3NextDelivery
                self.truck3Position = self.truck3NextLocation[0]
                self.unloadTruck(self.truck3Packages, self.truck3PackagePriority, self.truck3Position)
                self.truck3DestinationList.remove(self.truck3NextLocation[0])

                if len(self.truck3DestinationPriorityList) > 0:
                    self.truck3DestinationPriorityList.remove(self.truck3NextLocation[0])

                if len(self.truck3DestinationPriorityList) > 0:

                    self.truck3NextLocation = findDestination(self.truck3Position, self.truck3DestinationPriorityList)

                elif len(self.truck3DestinationList) > 0:

                    self.truck3NextLocation = findDestination(self.truck3Position, self.truck3DestinationList)

                elif len(self.truck3DestinationList) < 1 and self.truck3NextLocation[0] != 0:

                    self.truck3DestinationList.append(0)
                    self.truck3NextLocation = (0, distanceHome(self.truck3Position))

                self.truck3NextDelivery = float(self.truck3NextLocation[1])

            if len(self.truck3DestinationList) < 1:
                self.truck3Home = True

            if not self.truck3Home and self.truck3Away:
                self.truck3CurrentPosition += speed
                self.truck3Distance += speed
