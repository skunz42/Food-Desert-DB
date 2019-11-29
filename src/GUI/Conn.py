# Sean Kunz

from pymongo import MongoClient

class Conn:
    client = MongoClient(port=27017)
    db = client.CS432FP
    def __init__(self):
        print(":concerned_froge:")

    def getCities(self):
        cursor = self.db.storeinfo.find({}, {"City": 1, "_id": 0}).distinct("City")
        return list(cursor)
