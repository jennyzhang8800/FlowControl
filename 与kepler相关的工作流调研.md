#1.工作流
>**工作流概念起源**：工作流的概念起源于*办公自动化领域*。它所关注的问题是处理过程的自动化，它根据一系列定义的规则，把文档、信息或任务在参与者之间传递，以达到某种目的

>**工作流定义**：工作流管理联盟（WfMC）对工作流的定义：一类能够完全或者部分*自动执行*的经营过程，根据一系列过程规则、文档、信息或任务能够在不同的执行者之间传递、执行。

---
#2.工作流系统
>**工作流系统定义**：工作流管理联盟(WfMC，Workflow Management Coalition)给出的关于工作流管理系统的定义是：工作流管理系统是一个软件系统，它完成工作流的定义和管理，并按照在计算机中预先定义好的工作流逻辑推进工作流实例的执行。

---

###2.1商业工作流系统与科学工作流系统

+  **商业工作流系统**：传统的工作流系统，即目前应用在企业领域的BPM（Business Process Management），例如JBPM和Activiti。
+  **科学工作流系统**：是获取科学数据（包括传感器数据、医学影像、卫星图像、仿真输出、各类观测数据等等），并对所获取到的数据执行复杂分析的灵活的工具。如目前主流的科学工作流系统：Taverna,Kepler,VIEW,Swift,Pegasus

**开源工作流引擎**

![workflow-engine.PNG](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/workflow-engine.PNG)

**特点**

![workflow-table.png](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/workflow-table.PNG)

有关这五种科学工作流更多详细信息，[点击查看](https://github.com/jennyzhang8800/FlowControl/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81%E6%8A%A5%E5%91%8A.doc)

**两者对比**

![compare.png](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/compare.PNG)

---
#3.Kepler系统
###3.1 简介
>**Keplert系统**:由UC Berkeley大学开发的Ptolemy系统，用于研究并发、实时以及嵌入式系统的建模、仿真和设计。Kepler系统很好地继承和发展了Ptolemy面向角色建模的特性，并加入了大量新特性，用于支持科学工作流。主要体现在对科学数据的获取、处理。

**Kepler网址：**[https://kepler-project.org/](https://kepler-project.org/)

----

###3.2 语言及特点
**Kepler系统使用JAVA语言编写，充分利用了JAVA语言的面向对象特点，具有可移植性强等优点。**

+ Kepler科学工作流能够在理工的很多学科，帮助科学家、分析员和电脑程序员创建、运行和分享模型及解析。
+ Kepler能*操作很多格式的数据*，既可以本地运行，也可以联网运行。
+ Kepler能够*有效地整合分散的软件构件*，比如说能将R脚本和编译后的C代码合并，或者使远程、分布式的模型的运行更容易。
+ 使用Kepler的*图形用户界面*，用户只要通过简单操作，就能选择和连结相关的分析构件和数据源，从而创建一个科学工作流。

总之，Kepler软件能帮助用户分享、复用那些由科学社区开发的数据、工作流和构件，从而满足一般的公共需求。

----

###3.3 总体架构和模块划分

  给定一个网络服务描述的URL，KEPLER系统中的WebService actor 就能被实例化为在服务描述中的任意特定操作。在实例化之后。WebService actor 将被整合进一个科学工作流中，就像一个本地构件一样。

  Harvester 组件是KEPLER的众多网络服务之一。就像通用的WebService actor 一样。对于那些基于网络服务的应用和工作流来说，Harvester特性使得快速的原型设计和开发更加便利

 **相关术语**

+ 角色（actor）：执行一系列复杂操作的组件，是SWF中处理科学数据的实体。
+ 参数（parameter）：角色可配置的值。
+ 端口（port）：角色间供相互连接的通道，有输入端口和输出端口。
+ 连接（relation）：用于连接角色的端口，是数据传递的通道。

在用Kepler/PtolemyII构建的科学工作流中，独立处理具体任务的组件实体被称为“actor”。

  “actor”之间通信的接口是“port”，有input port和output port两种。

  actor使用“parameter”来配置和定制相关的行为。

  actor之间通过“channel”相互连接

  “director”指定了模型执行的语义，定义了actor如何执行，以及相互之间如何通信。用户定制好的工作流模型，包括一个特定领域的“director”，以及至少一个“actor”。工作流执行的时候，“director”控制数据在“actor”中的流动，按照定制好的流程，调度部署每个“actor”的迭代执行。

  在Kepler/PtolemyII系统中，定制好的科学工作流模型以XML文件形式存储，该XML文件满足MoML（Modeling Markup Language）XML模式要求。
MoML使用DTD（文档类型定义）定义

**Kepler工作流**

![kepler-panel-1.PNG](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/kepler-panel-1.PNG)
![kepler-panel-2.PNG](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/Kepler-panel-2.PNG)

----

###3.4 基于web的工作流（后台利用Kepler）
**架构图**

![achitecture.PNG](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/achitecture.PNG)

**Web接口层**
+ 提供给用户一个设计良好、方便易用的接口，以组装、查看、执行、管理工作流实例。
+ 提供给用于一个一站式服务的web环境，从数据资源获取、结果数据反馈、用户信息管理、及其它服务。
+ 使用Ajax等web技术开发。

**工作流引擎及中间件层**
+ 提供一个稳定的工作流引擎 ，并支持资源、引擎、web等之间的通信。
+ 使用Kepler：管理actor的分类信息；处理工作流实例的运行；动态添加算法模型（actor）。 
 
**数据资源层**
+ 完成对物理资源及分布式资源（大规模科学数据，如IPCC、NCAR等）的存取。

---
#4. 参考文献
【1】[科学工作流报告](https://github.com/jennyzhang8800/FlowControl/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81%E6%8A%A5%E5%91%8A.doc)

【2】[科学工作流kepler及其应用](https://github.com/jennyzhang8800/FlowControl/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81kepler%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8.ppt)

【3】[基于科学工作流的铁路行车安全评价系统研究_杜彦华](https://github.com/jennyzhang8800/FlowControl/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81/%E5%9F%BA%E4%BA%8E%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%9A%84%E9%93%81%E8%B7%AF%E8%A1%8C%E8%BD%A6%E5%AE%89%E5%85%A8%E8%AF%84%E4%BB%B7%E7%B3%BB%E7%BB%9F%E7%A0%94%E7%A9%B6_%E6%9D%9C%E5%BD%A6%E5%8D%8E.pdf)

【4】[基于Kepler工作流的OWS服务链应用_张建博](https://github.com/jennyzhang8800/FlowControl/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81/%E5%9F%BA%E4%BA%8EKepler%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%9A%84OWS%E6%9C%8D%E5%8A%A1%E9%93%BE%E5%BA%94%E7%94%A8_%E5%BC%A0%E5%BB%BA%E5%8D%9A.pdf)

【5】[基于科学工作流的空间数据处理技术探讨_柴胜](https://github.com/jennyzhang8800/FlowControl/blob/master/%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE/%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81/%E5%9F%BA%E4%BA%8E%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%9A%84%E7%A9%BA%E9%97%B4%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E6%8A%80%E6%9C%AF%E6%8E%A2%E8%AE%A8_%E6%9F%B4%E8%83%9C.pdf)


