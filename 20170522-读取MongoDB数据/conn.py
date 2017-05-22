from pymongo import MongoClient
def connMongo():
    client = MongoClient("localhost",27017)
    db = client.test
    result = db.workflow.find_one({"email":"jennyzhang8800@163.com"})
    return result

if __name__ == '__main__':
    result=connMongo()
    print (type(result))
    print result
    
