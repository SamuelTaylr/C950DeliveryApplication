import csv
from hash import HashTable

address_data = list(csv.reader(open('data/addressData.csv'), delimiter=','))
distance_data = list(csv.reader(open('data/distanceData.csv'), delimiter=','))
addressTable = HashTable()

with open('data/addressData.csv') as file:

    data = csv.reader(file, delimiter=',')

# creates list using address data from csv file
# O(N)
    for row in data:

        key = row[2]
        addressTable.add(key, [row[0], row[1], key])



