import csv
from hash import HashTable

class Packages:

    hash_table = HashTable()

    # Constructor for a package object containing package data from the csv file
    # O(N)
    def __init__(self):
        with open('data/packageData.csv') as file:

            self.data = csv.reader(file, delimiter=',')

            for row in self.data:

                self.key = row[0]
                Packages.hash_table.add(self.key, [self.key, row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
        


