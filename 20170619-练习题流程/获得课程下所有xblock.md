


**例:获得Tsinghua/CS101课程下所有的'练习'xblock**

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
