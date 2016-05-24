# FlowControl
this is a repo for FlowControl

# 方案设计
 
#### Open edX在线学习平台流程控制设计方案
 一.  总体目标
 
     定义学习流程模板，让每一个用户实现根据事先定义好的流程学习。
     即只有当用户完成了指定的学习内容后才可以学习后面的内容，否则没有权限查看相关页面进行学习。
     
 二. 设计思路
 
   + 从服务器端进行页面权限控制。
   + 定义用户组，只有在用户组内的用户才有权限访问相应页面，每一个用户在学习过程中跟据学习进度被自动移动到相应的用户组中。
   + 流程模板实现不同用户组对不同页面的访问权限定义。
   
三. 实现方法
 
   由于Open edX平台采用的是nginx代理服务器，加之有关用户认证方面的内容会转移到内部新安装的apache服务器交给shibleth处理。
   因此基于工作流的页面权限控制也应该先转给apache进行控制。
   
   具体实现如下：
   
   1. 	更改nginx配置文件，把指定uri的页面交给apache处理。（利用的是nginx代理服务器的负载均衡机制）
   
   （1）	配置文件路径为：/edx/app/nginx/sites-available/lms

         输入下面的命令，打开配置文件。
         
       ``` 
      cd /edx/app/nginx/sites-available/lms
      sudo vim lms
      ```
      

  （2）	更改配置文件，把uri 为http://crl.ptopenlab.com:8811/flow-control/  的页面转交给apache的8080端口。实现方法为在上述配置文件中加入下面的代码：
 
 ```
 upstream apache-lms-backend {
  server 127.0.0.1:8080 fail_timeout=0;
 }
location @proxy_to_apache_lms {
  proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
proxy_set_header X-Forwarded-Port $http_x_forwarded_port;
proxy_set_header X-Forwarded-For $http_x_forwarded_for;
  proxy_set_header Host $http_host;
  
  proxy_redirect off;
  proxy_pass http://apache-lms-backend;
}
location ~ ^/flow-control/?$ {
  try_files $uri @proxy_to_apache_lms;
}
```

##### 代码解释：


  ```
     # 指定后端服务端的地址为127.0.0.1:8080。重试时间间隔为0
      upstream apache-lms-backend {
      server 127.0.0.1:8080 fail_timeout=0;
     }
     # 定义一个命名的（名称为proxy_to_apache_lms） location，在内部定向时使用。proxy_set_header 用于设置重定向的header
     location @proxy_to_apache_lms {
    proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
    proxy_set_header X-Forwarded-Port $http_x_forwarded_port;
    proxy_set_header X-Forwarded-For $http_x_forwarded_for;
    proxy_set_header Host $http_host;
  
    proxy_redirect off;
    proxy_pass http://apache-lms-backend;
   }

  ```

这两部分代码实现nginx代理服务器的配置。upstream按照轮询（默认）方式进行负载，每个请求按时间顺序逐一分配到不同的后端服务器。
