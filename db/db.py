## database opeterion DB password mongo atlas:  euQ7nDEBuGhdhdJ  user: admin
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://admin:euQ7nDEBuGhdhdJ@atrialfibrillationclust.zmhheka.mongodb.net/?retryWrites=true&w=majority")

DB = client["AtrialFibrillationDB"]

def InitDB():
    print("db initialization")
