> 下面是获得xblock所在章节（chapter）下的所xblock列表的方法

有两种方法可以获得XBLOCK的信息，分别是从API获取和从XBLOCK类获取

# 1. 从API获取

可以通过[Courses API](https://edx.readthedocs.io/projects/edx-platform-api/en/latest/courses/)获取

具体的官方文档为[get-a-list-of-course-blocks-in-a-block-tree](https://edx.readthedocs.io/projects/edx-platform-api/en/latest/courses/blocks.html#get-a-list-of-course-blocks-in-a-block-tree)

API格式如下：
```
GET /api/courses/v1/blocks/<usage_id>/?
    username=anjali
    &depth=all
    &requested_fields=graded,format,student_view_multi_device,lti_url,due
    &block_counts=video
    &student_view_data=video
    &block_types_filter=problem,html
```

1.1 关于如何获得usage_id? 

[点击查看官方文档](https://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/course_features/lti/lti_address_content.html#finding-the-usage-id-for-course-content)

（1）以“教员”身份进入到LMS

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/usage_id0.png)

(2) 点击xblock下方的"工作人员调试信息"

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/usage_id1.png)

(3)location的值即为当前xblock的usage_id

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170619-%E7%BB%83%E4%B9%A0%E9%A2%98%E6%B5%81%E7%A8%8B/pictures/usage_id2.png)


另外：
```
parent=i4x://Tsinghua/CS101/vertical/22f775172cfb4ee7ad37ba7f5ce38562
为当前xblock的父节点（即unit）的usage_id
```

usage_id的格式如下：

```
i4x:;_;_{org};_{course};_{type};_{display name}

```
例如：
```
i4x://Tsinghua/CS101/chapter/95a97b1222504f0d8663d45f271692e4
```

```
{org} -> Tsinghua
{course} -> CS101
{type} -> chapter
{display name} ->95a97b1222504f0d8663d45f271692e4
```

关于 {type}，根据edx的课程结构有以下的对应关系

| 名称 | 名称 | {type} |
|:---: | :---:| :---:|
| 章 | chapter | chapter |
| 节 | subsection | sequential |
| 单元 | unit | vertical |
| 组件 | component | quizzes,html,video等 |


可以看到unit 和component的usage_id可以通过以教员身份从LMS端“工作人员调试信息”中查看到，

但是subsection和chapter的usage_id就无法直接从LMS查看到了。

实际上，subsection和chapter的usage_id可以通过后台python程序中直接获得。

例如，xblock名称为“workflow”，则可以从workflow.py中调用self.get_parent()获取当前xblock的父节点

| 名称 | 名称 | {type} |python获取usage_id| usage_id |
|:---: | :---:| :---:|:---:|:---:|
| 章 | chapter | chapter |   self.get_parent().get_parent().get_parent()location  | i4x://Tsinghua/CS101/chapter/95a97b1222504f0d8663d45f271692e4 |
| 节 | subsection | sequential | self.get_parent().get_parent().location | i4x://Tsinghua/CS101/sequential/23cfd14026424006b3bb884e03d692fa |
| 单元 | unit | vertical | self.get_parent().location | i4x://Tsinghua/CS101/vertical/5d1f4847605d453fbbdd9ee8c29704f7 |
| 组件 | component | quizzes,html,video等 | self.location | i4x://Tsinghua/CS101/workflow/af94846445f34c34976700e1d8f0ab39 |


至此己经能够获得当前xblock，以及其多级父节点的usage_id

接下来就可以直接利用API，获得指定usage_id下的所有xblock


**例1:获得'第二章'(chapter)下所有的'练习'xblock**

```
http://cherry.cs.tsinghua.edu.cn/api/courses/v1/blocks/i4x://Tsinghua/CS101/chapter/95a97b1222504f0d8663d45f271692e4?username=s0712&depth=all&block_types_filter=quizzes2
```
上面的链接中:
```
api/courses/v1/blocks  : API
i4x://Tsinghua/CS101/chapter/95a97b1222504f0d8663d45f271692e4  :该章节的usage_id
username=s0712   : 指定用户名
depth=all  :（整数或全部）表示遍历块的深度。all意味着整个层次结构。
block_types_filter=quizzes2 : 用于筛选返回xblock的最终结果的块类型,这里只返回type:quizzes的xblock

```

返回结果为:

```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS

{
    "root": "i4x://Tsinghua/CS101/chapter/95a97b1222504f0d8663d45f271692e4",
    "blocks": {
        "i4x://Tsinghua/CS101/quizzes2/1d54f43f89134f50b579a61f0bcd5c89": {
            "display_name": "练习",
            "lms_web_url": "http://cherry.cs.tsinghua.edu.cn/courses/Tsinghua/CS101/2015_T1/jump_to/i4x://Tsinghua/CS101/quizzes2/1d54f43f89134f50b579a61f0bcd5c89",
            "type": "quizzes2",
            "id": "i4x://Tsinghua/CS101/quizzes2/1d54f43f89134f50b579a61f0bcd5c89",
            "student_view_url": "http://cherry.cs.tsinghua.edu.cn/xblock/i4x://Tsinghua/CS101/quizzes2/1d54f43f89134f50b579a61f0bcd5c89"
        },
        "i4x://Tsinghua/CS101/quizzes2/b3af4d3f30e84885bb6634bf869286e9": {
            "display_name": "练习",
            "lms_web_url": "http://cherry.cs.tsinghua.edu.cn/courses/Tsinghua/CS101/2015_T1/jump_to/i4x://Tsinghua/CS101/quizzes2/b3af4d3f30e84885bb6634bf869286e9",
            "type": "quizzes2",
            "id": "i4x://Tsinghua/CS101/quizzes2/b3af4d3f30e84885bb6634bf869286e9",
            "student_view_url": "http://cherry.cs.tsinghua.edu.cn/xblock/i4x://Tsinghua/CS101/quizzes2/b3af4d3f30e84885bb6634bf869286e9"
        },
        .....
```

**例2:获得'第二章第1节'（subsection）下所有的'练习'xblock**

usage_id=i4x://Tsinghua/CS101/sequential/23cfd14026424006b3bb884e03d692fa

```
http://cherry.cs.tsinghua.edu.cn/api/courses/v1/blocks/i4x://Tsinghua/CS101/sequential/23cfd14026424006b3bb884e03d692fa?username=s0712&depth=all&block_types_filter=quizzes2
```


**例3:获得'第二章第1节第1单元'（unit）下所有的'练习'xblock**

usage_id = i4x://Tsinghua/CS101/vertical/76d9f15432de4f08951d048e85203159

```
http://cherry.cs.tsinghua.edu.cn/api/courses/v1/blocks/i4x://Tsinghua/CS101/vertical/76d9f15432de4f08951d048e85203159?username=s0712&depth=all&block_types_filter=quizzes2
```


# 2.从XBLOCK类获取

任何一个XBLOCK类的定义都按下面的模板定义：

```
class WorkflowXBlock(XBlock):
    @XBlock.json_handler
    def submmit(self, data, suffix=''):
    
```

上述WokflowXBlock类中，可以定义若干个方法，每个方法都必须self作为第一个参数。

self代表的是当前XBLOCK对象，该对象拥有一些属性和方法。可以通过dir(self)查看该对象有哪些属性和方法[dir(self)]()

可以找到有``get_parent``和``get_children``方法，可以获得该xblock的父结点，以及所有子节点。

父子关系为：chapter -> subsection ->unit ->xblock

所以
```
self                                         即为当前xblock节点
self.get_parent()                            即为unit（单元）节点
self.get_parent().get_parent()               即为subsection(节)节点
self.get_parent().get_parent().get_parent()  即为chapter(章)节点
```

因此：通过下面的代码可以获得当前XBLOCK所在unit的所有子节点
```
 children = self.get_parent().get_children()
```
更进一步，获得当前XBLOCK所在单元的所有练习题的题号：
```
 children = self.get_parent().get_children()
 qNo_list=[]
 for item in children:
     if hasattr(item, "qNo"):
         qNo_list.append(item.qNo)
```
获得当前XBLOCK所在章的所有练习题的题号：

```
subsections = self.get_parent().get_parent().get_parent().get_children()
qNo_list=[]
for subsection in subsections:
    for unit in subsection.get_children():
        for xblock in unit.get_children():
            if hasattr(xblock, "qNo"):
                qNo_list.append(xblock.qNo)
```
