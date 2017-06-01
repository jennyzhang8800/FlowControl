>本例结合Kepler与oplog实现：Kepler中的某活动对Mongodb进行修改，并且自动获得Mongodb操作日志提供的修改信息。

### oplog

参考上一次的备份说明：[点击查看](https://github.com/jennyzhang8800/FlowControl/tree/master/20170531-oplog%E7%9B%91%E6%8E%A7mongo%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C)

### 运行说明

1. 以master启动mongod守护

```
sudo mongod --master --dbpath /data/db
```
这时候在local这个数据库下，可以看到oplog.$main这个聚集
```
mongo
use local
show collections
```
![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170531-oplog%E7%9B%91%E6%8E%A7mongo%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C/pictures/local.oplog.PNG)

oplog.$main中记录的就是操作日志。我们实现的MongoDB监控就是对该日志进行过滤并实时读取。

2. 把test文件夹下的所有脚本，放到/home/jenny/Kepler-2.5/test目录下。

```/home/jenny/Kepler-2.5/test```这个路径是interactMongo.kar中的外部执行(External Execution)actor中设定的路径

3. 启动Kepler,打开interactMongo.kar

![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170601-Kepler%E7%BB%93%E5%90%88oplog%E5%AE%9E%E7%8E%B0%E7%9B%91%E6%8E%A7Mongo%E6%93%8D%E4%BD%9C/pictures/kepler.PNG)
