>Open edX 练习题流程

### 1. 流程定义

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B.png)


### 2. edx课程结构-数据存储

 edx课程数据存储在Mongo数据库中。通过查看官方文档：[modulestores](http://edx.readthedocs.io/projects/edx-developer-guide/en/latest/modulestores/index.html)得知，课程结构数据存储在modulestroe集合中。
 
 通过下面的命令查看课程结构：
 
 （1）连接MongoDB
 ```
 mongo
 show dbs
 ```
 可以看到下面的信息：
 ```
admin                            0.078GB
cs_comments_service_development  0.078GB
edxapp                           0.203GB
local                            0.078GB
test   
 ```
（2）打开edxapp数据库
```
use edxapp
```
(3)查看modulestores集合
```
show collections
```
可以看到下面的信息:
```
fs.chunks
fs.files
modulestore
modulestore.active_versions
modulestore.definitions
modulestore.structures
system.indexes
```

查看'modulestore'的内容
```
db.modulestore.find().pretty()
```
即可看到课程结构数据，类似于以下形式：

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/modulestores-section2.png)

上图是CS101课程某一章（section）的结构：可以看到该sections的name,以及下面的subsection的信息

看下面的这个例子加以说明：

edx lms页面里看到的界面是这样的(第2讲，下面有7个subsection)：

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/edx-sections2.png)

对应的URL为：http://cherry.cs.tsinghua.edu.cn/courses/Tsinghua/CS101/2015_T1/courseware/95a97b1222504f0d8663d45f271692e4/9eea7983a1644804bfe4b662efd6d16d/

Mongo数据库中的对应的数据如下：
```
{
"_id" : {
"tag" : "i4x",
"org" : "Tsinghua",
"course" : "CS101",
"category" : "chapter",
"name" : "95a97b1222504f0d8663d45f271692e4",
"revision" : null
},
"definition" : {
"data" : {

},
"children" : [
"i4x://Tsinghua/CS101/sequential/9eea7983a1644804bfe4b662efd6d16d",
"i4x://Tsinghua/CS101/sequential/85142d7343bb4f1fb0a588e59f51c902",
"i4x://Tsinghua/CS101/sequential/b4d247c196134cdbac9dd4e37465dcbe",
"i4x://Tsinghua/CS101/sequential/7e545a6c25714f44a52e0205cfd71033",
"i4x://Tsinghua/CS101/sequential/19304745c4694ee1958fc9c111ba7e0d",
"i4x://Tsinghua/CS101/sequential/be1c2ac233174d798fc827d46d37f809",
"i4x://Tsinghua/CS101/sequential/23cfd14026424006b3bb884e03d692fa"
]
},
"edit_info" : {
"edited_by" : NumberLong(195),
"subtree_edited_on" : ISODate("2016-03-16T07:37:58.556Z"),
"edited_on" : ISODate("2016-03-11T06:54:34.173Z"),
"subtree_edited_by" : NumberLong(195)
},
"metadata" : {
"start" : "2015-10-26T00:00:00Z",
"display_name" : "第2讲 实验零 操作系统实验环境准备"
}
}
```
通过分析上面的json数据，可以发现下面的信息：

第一个有用的信息是：
```
"name" : "95a97b1222504f0d8663d45f271692e4" 表示的是sections的ID，对应URL中的倒数第二项http://cherry.cs.tsinghua.edu.cn/courses/Tsinghua/CS101/2015_T1/courseware/95a97b1222504f0d8663d45f271692e4/9eea7983a1644804bfe4b662efd6d16d/
```
第二个有用的信息是：
```
"children" : [...] 表示的是subsection的信息，这里有7项。这里可以提取出URL的最后一项

```
第三个有用的信息是：
```
"display_name" : "第2讲 实验零 操作系统实验环境准备"
```



## 3.控制课程导航栏

>可以通过控制课程章节导航栏的显示，来实现章节的访问控制。
如下图：第1讲不显示

1. 分析控制脚本

利用chrome的F12，先分析导航栏对应的html结构。如下：

可以看到导航栏定义在```<div class='acorrdion'>...</div>```之间，查看source,可以看到加载的js位于/static/js下。

因此，根据关键词找到对应的源码：

```
cd /edx
sudo find -name accordion
```

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/edx-accordion.html.png)

可以找到** /edx/app/edxapp/edx-platform/lms/templates/courseware/accordion.html **  

这里定义了导航栏的html模板：
```
.....
.....
% for chapter in toc:
    ${make_chapter(chapter)}
% endfor
```
从html代码可以分析出，html模板接收的数据中应含有'toc'字段

下面找到对应的python脚本(python脚本的render函数应该以accordion.html作为参数)。

通过下面的命令查找包含‘accordion.html’的所有文件
```
sudo find /edx/app/edxapp/edx-platform/lms|xargs grep -ri "accordion.html" -l
```
结果找到了下面的路径
** /edx/app/edxapp/edx-platform/lms/djangoapps/courseware/views/index.py**

可以看到render_accordion这个函数：
```
def render_accordion(request, course, table_of_contents):
    """
    Returns the HTML that renders the navigation for the given course.
    Expects the table_of_contents to have data on each chapter and section,
    including which ones are active.
    """
    context = dict(
        [
            ('toc', table_of_contents),
            ('course_id', unicode(course.id)),
            ('csrf', csrf(request)['csrf_token']),
            ('due_date_display_format', course.due_date_display_format),
        ] + TEMPLATE_IMPORTS.items()
    )
    return render_to_string('courseware/accordion.html', context)



```

因此通过控制context的内容，就可以控制前台导航栏的显示了！

在github仓库对应的源码：
[edxapp/edx-platform/lms/templates/courseware/accordion.html ](https://github.com/edx/edx-platform/blob/master/lms/templates/courseware/accordion.html)

[/edx/app/edxapp/edx-platform/lms/djangoapps/courseware/views/index.py](https://github.com/edx/edx-platform/blob/master/lms/djangoapps/courseware/views/index.py)

