from truck import Truck, individualPackageReport

truck = Truck()

def promptInfo():
    truck.deliveryMethod()
    print('\nAll deliveries were completed in', "{0:.2f}".format(truck.getDistance(), 2), 'miles.')


# Method called by main depending on user input, calls delivery
# O(1)
def optionOne():

    truck.truckAttributes()
    truck.deliveryMethod(input('Enter time in "HH:MM" format: '))
    truck.packageReport(int(input('\nEnter package ID: ')))


# Method called by main depending on user input, provides various reports
# O(1)
def optionTwo():

    truck.truckAttributes()
    truck.deliveryMethod(input('\nEnter time in "HH:MM" format: '))
    truck.packageReport()


# Method called by main depending on user input, provides various reports
# O(1)
def optionThree():

    truck.truckAttributes()
    individualPackageReport(int(input('\nEnter Package Id to See Info: ')))
