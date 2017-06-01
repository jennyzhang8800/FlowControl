#!/usr/bin/env python 
import sys
from pymongo import MongoClient

#connection build
def connMongo(database_name,collection_name):
    client = MongoClient("localhost",27017) #connect to MongoDB
    db = client.get_database(database_name) #connect to database
    col = db.get_collection(collection_name) #connect to collection
    return col

#Query
def queryMongo(col,query_commend):
    result = col.find_one(query_commend)
    return result
#Insert
def insertMongo(col,insert_commend):
    result = col.insert(insert_commend)
    return result
if __name__ == '__main__':
    #get parameter from commend line
    database_name = sys.argv[1]
    collection_name = sys.argv[2]
    commend = eval(sys.argv[3]) #invert string to dict

    col = connMongo(database_name,collection_name)
    result = insertMongo(col,commend)
    
    
