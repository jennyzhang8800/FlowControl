> 本例实现：通过Kepler中的参数，指定要查询的数据库名， collection名，以及查询条件。实现从MongoDB中查询数据并返回到Kepler

1. **Kepler端的Panel如下图所示:**
![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170524-%E9%80%9A%E8%BF%87%E5%8F%82%E6%95%B0%E6%9F%A5%E8%AF%A2MongoDB-%E5%B0%81%E8%A3%85%E6%88%90%E5%AD%90%E6%B5%81%E7%A8%8B/pictures/panel.PNG)

其中的参数
+ db_name: 数据据名称
+ col_name: collection名称
+ query_commend: 查询语句

通过QueryMongoDB这个CompositeActor实现查询

返回结果通过Display显示出来


2. **CompositeActor的实现**

实质是通过调用/home/jenny/Kepler-2.5/test目录下的 queryMongo.py脚本实现查询功能，在Kepler中External Execution这个Actor可以实现外部脚本的执行

![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170524-%E9%80%9A%E8%BF%87%E5%8F%82%E6%95%B0%E6%9F%A5%E8%AF%A2MongoDB-%E5%B0%81%E8%A3%85%E6%88%90%E5%AD%90%E6%B5%81%E7%A8%8B/pictures/QueryMongoDB.PNG)

3. **queryMongo.py**
 ```
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

if __name__ == '__main__':
    #get parameter from commend line
    database_name = sys.argv[1]
    collection_name = sys.argv[2]
    query_commend = eval(sys.argv[3]) #invert string to dict

    col = connMongo(database_name,collection_name)
    result = queryMongo(col,query_commend)
    print result
 ```
