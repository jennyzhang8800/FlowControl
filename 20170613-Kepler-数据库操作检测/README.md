>Kepler 在设定的时间内，检测MongoDB的更改情况。

### 1. 启动Mongod服务

首先，打开一个新的terminal（称为T1）,以master模式打开mongod
```
sudo mongod --master --dbpath /data/db
```

然后，打开一个新的terminal（T2）,查看oplog.$main这个聚集的内容
 
 ```
 mongo
 use local
 show collections

 ```
 可以看到有oplog.$main这个collection
 
 注！如果没有看到oplog.$main，请先关闭mongod服务，再重新启动。
 ```
 use  admin  
 db.shutdownServer()
 sudo mongod --master --dbpath /data/db
 ```

 
### 2. 启动MongoDB实时监控脚本

打开一个新的terminal（称为T3）
 ```
 python mongo-oplog-new.py
 ```

### 3. 启动Kepler工作流

![](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/CheckMongoChanges.PNG)

### 4. 对MongoDB作更改

打开一个新的terminal（称为T4）
```
mongo
use test
db.workflow.insert({"email":"test1@163.com"})
```
这时候可以看到T3有信息的输出，这条日志被记录在mongo-oplog.log中

同时Kepler界面也有信息输出,如下图：

![](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/CheckMongoChangesResult.PNG)

