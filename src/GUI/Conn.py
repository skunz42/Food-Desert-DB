# Sean Kunz

import tkinter as tk
from pymongo import MongoClient

class Conn:
    client = MongoClient(port=27017)
    db = client.CS432FP
    # Constructor
    def __init__(self):
        print(":concerned_froge:")

    '''***********************************************
                        getCities
        purpose:
            returns a list of distinct cities that are in the store collection
        parameters:
            None
        return:
            array
    ***********************************************'''
    def getCities(self):
        cursor = self.db.storeinfo.find({}, {"City": 1, "_id": 0}).distinct("City")
        return list(cursor)

    '''***********************************************
                        getMapOptions
        purpose:
            returns a list of distinct cities that are in the map collection
        parameters:
            None
        return:
            array
    ***********************************************'''
    def getMapOptions(self):
        cursor = self.db.mapinfo.find({}, {"City": 1, "_id": 0}).distinct("City")
        return list(cursor)

    '''***********************************************
                        getStores
        purpose:
            returns a list of stores in the database, based on city
        parameters:
            value - city name
        return:
            array
    ***********************************************'''
    def getStores(self, value):
        if value == 'all':
            cursor = self.db.storeinfo.find({}, {"_id": 0})
        else:
            cursor = self.db.storeinfo.find({"City": value}, {"_id": 0})
        vals = list(cursor)
        retArr = []
        for v in vals:
            retArr.append(v)
        return retArr

    '''***********************************************
                        getSummary
        purpose:
            returns a summary of the specified city
        parameters:
            value - city name
        return:
            dictionary
    ***********************************************'''
    def getSummary(self, value):
        arr = self.getStores(value)
        retDict = {}
        numRatings = 0
        totScore = 0.0
        pfd = 0 #Percent in a food desert
        # Calculates the total average
        for i in range(len(arr)):
            numRatings += arr[i]['Num_Ratings']
            tot = arr[i]['Num_Ratings'] * arr[i]['Rating']
            totScore += tot
        avg = 5.0 * (totScore/(numRatings*5.0))
        # Checks for percent in a food desert - might not be calculated
        cursor = self.db.mapinfo.find({"City": value}, {"_id":0})
        tmp = list(cursor)
        if len(tmp) > 0:
            pfd = tmp[0]['Percent Food Desert']
        else:
            pfd = 0
        retDict = {
            "Name": value,
            "Average Rating": avg,
            "Total Number of Ratings": numRatings,
            "Percent Pop in Food Desert": pfd,
            "Number of Stores": len(arr)
        }
        return retDict

    '''***********************************************
                        getMap
        purpose:
            returns a list of distinct cities that are in the store collection
        parameters:
            None
        return:
            array
    ***********************************************'''
    def getMap(self, value):
        cursor = self.db.mapinfo.find({"City": value}, {"_id": 0})
        return list(cursor)
