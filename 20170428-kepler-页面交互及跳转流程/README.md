### 页面交互及跳转流程实验

#### 实验效果

启动kepler流程，能够通过页面与用户进行交互，等待用户操作并获得用户填写的数据，然后进行下一个流程。

#### 流程界面如下：

![image](https://github.com/jennyzhang8800/FlowControl/blob/master/20170428-kepler-%E9%A1%B5%E9%9D%A2%E4%BA%A4%E4%BA%92%E5%8F%8A%E8%B7%B3%E8%BD%AC%E6%B5%81%E7%A8%8B/pictures/flow.png)

#### 具体流程：

1. 点击运行按钮会自动弹出注册页面，在该页面点“确定后”,会触发如下动作：
```
首先，kepler会获得页面中所填入的信息"index.html"
然后，跳转到第一个题的页面"1.html"
```

2. 在第一题的页面1.html，点击“提交后”，会触发如下动作：

```
首先，kepler会获得页面中所填入的信息"
然后，跳转到第二个题的页面"2.html"
```

3. 在第二题的页面2.html，点击“提交后”，会触发如下动作：

```
首先，kepler会获得页面中所填入的信息"
然后，跳转到结束"3.html"
```

#### 演示

**　与用户交互端（Browser）　**

1. index.html页面中 ->填入注册信息 -> 确认

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170428-kepler-%E9%A1%B5%E9%9D%A2%E4%BA%A4%E4%BA%92%E5%8F%8A%E8%B7%B3%E8%BD%AC%E6%B5%81%E7%A8%8B/pictures/index.html.png)

跳转到1.html页面

2. "1.html"页面中 -> 填写答案 -> 提交

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170428-kepler-%E9%A1%B5%E9%9D%A2%E4%BA%A4%E4%BA%92%E5%8F%8A%E8%B7%B3%E8%BD%AC%E6%B5%81%E7%A8%8B/pictures/1.html.png)

跳转到2.html页面

3. "2.html"页面中 -> 填写答案 -> 提交

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170428-kepler-%E9%A1%B5%E9%9D%A2%E4%BA%A4%E4%BA%92%E5%8F%8A%E8%B7%B3%E8%BD%AC%E6%B5%81%E7%A8%8B/pictures/2.html.png)

跳转到end.html页面

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170428-kepler-%E9%A1%B5%E9%9D%A2%E4%BA%A4%E4%BA%92%E5%8F%8A%E8%B7%B3%E8%BD%AC%E6%B5%81%E7%A8%8B/pictures/end.html.png)


** kepler 引擎端　**

![](https://github.com/jennyzhang8800/FlowControl/blob/master/20170428-kepler-%E9%A1%B5%E9%9D%A2%E4%BA%A4%E4%BA%92%E5%8F%8A%E8%B7%B3%E8%BD%AC%E6%B5%81%E7%A8%8B/pictures/kepler-rev.png)
