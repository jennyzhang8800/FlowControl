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

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/navigation-panel.png)



#### 1. 利用chrome的F12，先分析导航栏对应的html结构。

如下：

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/edx-lms-navigation.png)

可以看到导航栏定义在```<div class='acorrdion'>...</div>```之间，查看source,可以看到加载的js位于/static/js下。

#### 2. 根据关键词找到对应的源码：

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

html模板接收的数据格式如下：

```
  context = dict(
        [
            ('toc', table_of_contents),
            ('course_id', unicode(course.id)),
            ('csrf', csrf(request)['csrf_token']),
            ('due_date_display_format', course.due_date_display_format),
        ] + TEMPLATE_IMPORTS.items()
    )
```

toc:格式如下（仍然以第二讲为例）
```
  {
        'display_id': u'2',
        'sections': [
            {
                'url_name': u'9eea7983a1644804bfe4b662efd6d16d',
                'display_name': u'2.1\u524d\u8a00\u548c\u56fd\u5185\u5916\u73b0\u72b6',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            },
            {
                'url_name': u'85142d7343bb4f1fb0a588e59f51c902',
                'display_name': u'2.2OS\u5b9e\u9a8c\u76ee\u6807',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            },
            {
                'url_name': u'b4d247c196134cdbac9dd4e37465dcbe',
                'display_name': u'2.38\u4e2aOS\u5b9e\u9a8c\u6982\u8ff0',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            },
            {
                'url_name': u'7e545a6c25714f44a52e0205cfd71033',
                'display_name': u'2.4\u5b9e\u9a8c\u73af\u5883\u642d\u5efa',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            },
            {
                'url_name': u'19304745c4694ee1958fc9c111ba7e0d',
                'display_name': u'2.5x86-32\u786c\u4ef6\u4ecb\u7ecd',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            },
            {
                'url_name': u'be1c2ac233174d798fc827d46d37f809',
                'display_name': u'2.6ucore\u90e8\u5206\u7f16\u7a0b\u6280\u5de7',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            },
            {
                'url_name': u'23cfd14026424006b3bb884e03d692fa',
                'display_name': u'2.7\u6f14\u793a\u5b9e\u9a8c\u64cd\u4f5c\u8fc7\u7a0b',
                'graded': False,
                'format': '',
                'due': None,
                'active': False
            }
        ],
        'url_name': u'95a97b1222504f0d8663d45f271692e4',
        'display_name': u'\u7b2c2\u8bb2\u5b9e\u9a8c\u96f6\u64cd\u4f5c\u7cfb\u7edf\u5b9e\u9a8c\u73af\u5883\u51c6\u5907',
        'active': False
    },
```

### 3. 下面找到对应的python脚本

(python脚本的render函数应该以accordion.html作为参数)。

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



### 4. 修改index.py

1. 打开index.py

```
sudo vim /edx/app/edxapp/edx-platform/lms/djangoapps/courseware/views/index.py
```
2. 在index.py引入pymongo模块

```
import pymongo
```

3. 找到下的代码:

```
 courseware_context['accordion'] = render_accordion(
 self.request,
 self.course,
 table_of_contents['chapters'],
 courseware_context['language_preference'],

 )
```

改为:

```
courseware_context['accordion'] = render_accordion(
 self.request,
 self.course,
 table_of_contents['chapters'],
 courseware_context['language_preference'],
 self.real_user.email,
 )

```
4. 修改render_accordion
改为:

```
def render_accordion(request, course, table_of_contents, language_preference,email):
    """
    Returns the HTML that renders the navigation for the given course.
    Expects the table_of_contents to have data on each chapter and section,
    including which ones are active.
    """
    
    conn = pymongo.Connection('localhost', 27017)
    db = conn.test
    db.authenticate("edxapp","p@ssw0rd")
    result = db.workflow.find_one({'email':email}) #connect to collection
    if result:
        for item in result['workflow']:
            if item['visible'] == False:
                for index,item2 in enumerate(table_of_contents):
                    if(item2['url_name'] == item['url_name']):
    #                    table_of_contents[index]['sections']=[]
                        del table_of_contents[index]

    conn.disconnect()
    context = dict(
        [
            ('toc', table_of_contents),
            ('course_id', unicode(course.id)),
            ('csrf', csrf(request)['csrf_token']),
            ('due_date_display_format', course.due_date_display_format),
            ('time_zone', request.user.preferences.model.get_value(request.user, "time_zone", None)),
            ('language', language_preference),

        ] + TEMPLATE_IMPORTS.items()
    )
    return render_to_string('courseware/accordion.html', context)

```

修改前的[index.py](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/index.py.packup)

修改后的[index.py](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/index.py)
