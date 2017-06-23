> 下面是获得xblock所在章节（chapter）下的所xblock列表的方法

## 1. 从API获取

可以通过[Courses API](https://edx.readthedocs.io/projects/edx-platform-api/en/latest/courses/)获取

具体的官方文档为[get-a-list-of-course-blocks-in-a-block-tree](https://edx.readthedocs.io/projects/edx-platform-api/en/latest/courses/blocks.html#get-a-list-of-course-blocks-in-a-block-tree)

```
GET /api/courses/v1/blocks/<usage_id>/?
    username=anjali
    &depth=all
    &requested_fields=graded,format,student_view_multi_device,lti_url,due
    &block_counts=video
    &student_view_data=video
    &block_types_filter=problem,html
```

关于如何获得usage_id? [点击查看官方文档](https://edx.readthedocs.io/projects/edx-partner-course-staff/en/latest/course_features/lti/lti_address_content.html#finding-the-usage-id-for-course-content)

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



另:

**例1:获得Tsinghua/CS101课程下所有的'练习'xblock**

API为:
```
GET /api/courses/v1/blocks/?course_id=<course_id>
GET /api/courses/v1/blocks/?course_id=<course_id>
    &username=anjali
    &depth=all
    &requested_fields=graded,format,student_view_multi_device,lti_url
    &block_counts=video
    &student_view_data=video
    &block_types_filter=problem,html
```

具体的官方文档为：[get-a-list-of-course-blocks-in-a-course](https://edx.readthedocs.io/projects/edx-platform-api/en/latest/courses/blocks.html#get-a-list-of-course-blocks-in-a-course)

下面是一个实例:
```
http://cherry.cs.tsinghua.edu.cn/api/courses/v1/blocks/?course_id=Tsinghua/CS101/2015_T1&all_blocks=true&depth=all&block_types_filter=quizzes2
```
上面的链接中:
```
api/courses/v1/blocks  : API
course_id=Tsinghua/CS101/2015_T1  :课程ID为Tsinghua/CS101/2015_T1
all_blocks=true  : 返回所有的block
depth=all  :（整数或全部）表示遍历块的深度。all意味着整个层次结构。
block_types_filter=quizzes2 : 用于筛选返回xblock的最终结果的块类型,这里只返回type:quizzes的xblock

```

返回的结果为：

```
HTTP 200 OK
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS

{
    "root": "i4x://Tsinghua/CS101/course/2015_T1",
    "blocks": {
        "i4x://Tsinghua/CS101/quizzes2/884c3d0dd1934c8fa06d66720ef6aa26": {
            "display_name": "练习",
            "lms_web_url": "http://cherry.cs.tsinghua.edu.cn/courses/Tsinghua/CS101/2015_T1/jump_to/i4x://Tsinghua/CS101/quizzes2/884c3d0dd1934c8fa06d66720ef6aa26",
            "type": "quizzes2",
            "id": "i4x://Tsinghua/CS101/quizzes2/884c3d0dd1934c8fa06d66720ef6aa26",
            "student_view_url": "http://cherry.cs.tsinghua.edu.cn/xblock/i4x://Tsinghua/CS101/quizzes2/884c3d0dd1934c8fa06d66720ef6aa26"
        },
        "i4x://Tsinghua/CS101/quizzes2/5e79bc9be44a461f846725edeab9c85f": {
            "display_name": "练习",
            "lms_web_url": "http://cherry.cs.tsinghua.edu.cn/courses/Tsinghua/CS101/2015_T1/jump_to/i4x://Tsinghua/CS101/quizzes2/5e79bc9be44a461f846725edeab9c85f",
            "type": "quizzes2",
            "id": "i4x://Tsinghua/CS101/quizzes2/5e79bc9be44a461f846725edeab9c85f",
            "student_view_url": "http://cherry.cs.tsinghua.edu.cn/xblock/i4x://Tsinghua/CS101/quizzes2/5e79bc9be44a461f846725edeab9c85f"
        },
        ...
        
```
