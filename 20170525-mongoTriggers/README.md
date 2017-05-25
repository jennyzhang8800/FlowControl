1. 关于mongoTriggers的使用：https://github.com/jennyzhang8800/mongoTriggers/blob/master/%E4%BD%BF%E7%94%A8%E5%B8%AE%E5%8A%A9.md

分析：mongoTriggers只能监测在.js这个特定的文件中执行的对MongoDB的操作。不能实现对MongoDB的监控。

------

下面是对MongoDB的日志文件进行实时获取信息的方法，以实现对MongoDB操作的准实时监控。

+ python实现：https://github.com/RedBeard0531/mongo-oplog-watcher/blob/master/mongo_oplog_watcher.py
http://www.tuicool.com/articles/NbMNJrJ
+ nodejs实现：http://www.kuqin.com/database/20130412/334113.html
+ https://stackoverflow.com/questions/9691316/how-to-listen-for-changes-to-a-mongodb-collection
