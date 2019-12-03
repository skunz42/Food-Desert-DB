# Sean Kunz

import tkinter as tk
from pymongo import MongoClient

class Conn:
    client = MongoClient(port=27017)
    db = client.CS432FP
    def __init__(self):
        print(":concerned_froge:")

    def getCities(self):
        cursor = self.db.storeinfo.find({}, {"City": 1, "_id": 0}).distinct("City")
        return list(cursor)

    def getMapOptions(self):
        cursor = self.db.mapinfo.find({}, {"City": 1, "_id": 0}).distinct("City")
        return list(cursor)

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

    def getSummary(self, value):
        arr = self.getStores(value)
        retDict = {}
        numRatings = 0
        totScore = 0.0
        pfd = 0
        for i in range(len(arr)):
            numRatings += arr[i]['Num_Ratings']
            tot = arr[i]['Num_Ratings'] * arr[i]['Rating']
            totScore += tot
        avg = 5.0 * (totScore/(numRatings*5.0))
        retDict = {
            "Name": value,
            "Average Rating": avg,
            "Total Number of Ratings": numRatings,
            "Percent Pop in Food Desert": pfd
        }
        return retDict

    def getMap(self, value):
        cursor = self.db.mapinfo.find({"City": value}, {"_id": 0})
        return list(cursor)
