>mongodb本身没有提供触发器，因此不能像MySQL这些数据库一样直接利用触发器监控数据库的操作。但Mongodb有主从备份机制，并且把所有的操作日志记录在oplog这个特殊的聚集中，因此可以通过读oplog里的内容，来实现对数据库操作的准实时监控。

### 1. oplog

oplog(operations log)是一个特殊的capped colletion(一个固定大小的集合,当集合的大小达到指定大小时,新数据覆盖老数据)，**oplog中保存了所有对存储在数据库中的数据进行修改操作的滚动记录。**

MongoDB把数据库操作应用在主成员，然后把这些操作记录在主成员的oplog。然后，次成员在异步过程中复制并且应用这些操作。所有的副本集成员包含一个oplog的复制，在local.oplog.rs这个聚集中，这使得副本集成员能够维持数据库当前的状态。

在oplog中的每一个操作都是幂等的，也就是说，oplog操作无论被一次或多次应用到目标数据集中都产生一样的结果。

#### 1.1 oplog的结构：

```
"ts" : Timestamp(6417682881216249, 1),  时间戳
"h" : NumberLong(0),  长度
"v" : 2,  
"op" : "n", 操作类型
"ns" : "",  操作的库和集合
"o2" : "_id"  update条件
"o" : {}  操作值，即document
```

+ ``ts``：timestamp时间戳，显示的是这个操作是什么时间执行的。
+ ``h``：是一个操作的唯一id,确保每一个操作能被唯一标识,使得在相同的时间能区分出不同的操作
+ ``v``:version,指明oplog的格式
+ ``op``：这是oplog中真正有意义的部分，指明了发生了什么操作。op的值通常有以下几种：
  + ``i``:insert插入操作
  + ``u``:update更新操作
  + ``d``:delete删除操作
  + ``c``:cmd 在高层次影响数据库
  + ``n``:no-ops空操作,在数据库或聚集中改变，但是没有对存储的数据发生变化
  + ``db``:宣告一个数据库的出现
+ ``ns``:namespace 这个操作的作用域。如这是test数据库中的workflow聚集
+ ``o``:根据op的不同而不同。
  + 如insert操作，'o'这部分包含的是被插入的整个document。
  + 对于update操作，有'o2'和'o'这两部分，'o2'包含的是更新的查询条件部分，'o'包含的是满足查询条件之指明被更新的document。
  
### 2. mongo-oplog.py

该python脚本实现对oplog的准实时监控。

先设定一个延迟时间```self.poll_time = poll_time```默认是1秒
然后主要是start()函数，实现时间戳的比对，并进行相应字段的处理
 ```
 def start(self):
    oplog = self.connection.local['oplog.$main']   #读取local库下的oplog.$main这个聚集
    ts = oplog.find().sort('$natural', -1)[0]['ts']   #获取一个时间边际，最大的时间
    while True:
        if self._ns_filter is None:
            filter = {}
        else:
            filter = {'ns': self._ns_filter}
        filter['ts'] = {'$gt': ts}  #filter的条件，timestamp比ts大。即上一次时间戳之后的操作。
        try:
            cursor = oplog.find(filter)
            #对此时间之后的进行处理
            while True:
                for op in cursor:
                    ts = op['ts']
                    id = self.__get_id(op)
                    self.all_with_noop(ns=op['ns'], ts=ts, op=op['op'], id=id, raw=op)
                    #可以指定处理插入监控，更新监控或者删除监控等
                time.sleep(self.poll_time)
                if not cursor.alive:
                    break
        except AutoReconnect:
            time.sleep(self.poll_time)
 ```
 
 ### 3. 运行
 
 1. 首先，打开一个新的terminal（称为T1）,以master模式打开mongod
 ```
 sudo mongod --master --dbpath /data/db
 ```
 
 2. 然后，重新打开一个terminal（称为T2）,运行mongo-oplog.py
 ```
 sudo python mongo-oplog.py
 ```
 
 3. 接下来，再重新打开一个terminal（称为T3）
 
 进入到我们要操作的数据库中
 ```
 use test
 ```
 
 在workflow这个聚集中,插入一条新的document
 ```
 db.workflow.insert({'email':'Cherry@163.com'}
 ```


可以看到在T2中会输出这个操作的日志。在T3中也显示了该document己插入。

T2:
![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170531-oplog%E7%9B%91%E6%8E%A7mongo%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C/pictures/mongo-oplog.PNG)

T3:
![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170531-oplog%E7%9B%91%E6%8E%A7mongo%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C/pictures/mongo-insert.PNG)


 
 
