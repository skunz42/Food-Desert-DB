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

    def getStores(self, value):
        if value == 'all':
            cursor = self.db.storeinfo.find({}, {"_id": 0})
        else:
            cursor = self.db.storeinfo.find({"City": value}, {"_id": 0})
        vals = list(cursor)
        retArr = []
        for v in vals:
            print(v['Name'])
            retArr.append(v)
        return retArr
