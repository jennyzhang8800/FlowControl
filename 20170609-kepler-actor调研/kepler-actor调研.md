## 1. Is Present

+ 输入：一个多端口，该端口接收任意类型的值。端口的宽度必须与输出端口的宽度相匹配。
+ 输出：一个多端口，该端口广播布尔值：真（如果对应的输入通道接收了一个token）;假（如果对应的输入通道没有收到token）

+ 功能简介：

  + 该Actor输出“ture”或者“false”取决于它是否接收到一个数据token

  + 该Actor通过其多端口的输入通道，读取任意类型的token;如果通道上存在token，则actor在输出端口的相应通道上输出布尔值true；如果通道上不存在token，则actor在输出端口的相应通道上输出布尔值false；输入和输出端口的宽度（即每个端口上的通道数）必须相同。

  + 注意，当与同步导演（如SDF）一起使用时，这个角色最有用。在PN Director下，输入总是存在（根据定义）。在DE Drector下，该Actor只有在其中一个输入通道有数据时才会触发。
![](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/IsPresentActor-Kepler.PNG)



## 2.StatusChecker

+ **功能简介** 

  + 检查正在运行的作业的状态

  + 该Actor执行UNIX命令（如ls或：C:/Program Files/Internet Explorer/IEXPLORE.EXE）并且比较执行结果到指定的正则表达式（例如，*.HTML）。

  + 该Actor取决于系统特定的可执行文件和操作系统特性

  + 输出的执行结果到一个指定的输出文件。一旦执行完成，Actor通过输出端口将结果以字符串的形式输出。

  + 命令是通过命令参数或通过命令端口指定的，并且可以选择一个可选参数。
  
+ **参数**
  + ***命令***（commend）:命令必须要在远程主机上执行。命令必须指定为字符串。
  + ***输出文件***（outputFile）:输出文件的文件名（可选）。如果指定了输出文件，则命令的输出结果会写到这个文件中
  + ***有触发器***（hasTrigger）:激活触发器输入端口
  + ***睡眠时间***（sheepTime）:checks之间的延迟，以毫秒为单位。参数是long型的，默认值是0，这意味着actor不会在两个checks之间sleep
  + ***检查条件***（checkCondition）:将与输出进行比较的正则表达式。
  + ***最大检查个数***(maxChecks):check的最大数目。默认值是- 1，这意味着actor将继续检查，直到满足条件为止。
  
+ **端口**
  + ***命令***(commend):接受执行命令的输入端口。命令必须指定为字符串。
  + ***参数***（argument）:接受命令参数的输入端口（可选）
  + ***输入文件句柄***(infileHandle):接受输入文件路径的输入端口（可选）。如果命令接受输入文件而不是参数列表，则使用该命令。
  + ***触发器***(trigger):一个没有声明类型的多端口，（换句话说，该端口可以接受任何数据类型：double，in,array，等等）如果该端口被相连，直到到触发端口接收输入token,该actor才不会被触发。连接这个端口是可选的，但在安排actor在某个时间执行时有用。
  + ***输出文件句柄***(outfileHandle):如果已指定一个输出文件,该输出端口则广播输出文件路径
  + ***输出***(output):一个输出端口，它在执行完命令后，广播由执行命令生成的数据，作为字符串输出。
  + ***退出码***(exitCode):一个输出端口，指示命令是否成功执行。如果命令成功执行，则退出码为1。
  + ***交互输出***(iterativeOutput):输出端口，用于广播每次迭代的输出。
  ![](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/Status%20Checker.PNG)

## 3.Stop

+ **功能简介** 
  + Stop actor在当前迭代完成后停止工作流。
  + 该actor通过其输入端口接收布尔token。 当actor收到一个true token，它会停止工作流。当当前迭代完成时，取决于工作流Director
  + 在SDF Director下，当前的迭代结束，当Stop actor收到一个true token时停止执行。
  + 在DE Derector下，actors可以在Stop调用之后调用（如果具有时间戳t和值true的事件到达Stop actor，然后结束当前迭代。意味着用时间戳T处理事件队列中的所有事件，其中一些事件可能在Stop actor调用之前还没有被处理过）
  + Stop actor不是停止PN工作流的最好方法，它没有定义好的迭代概念。要停止一个PN工作流，设计工作流，在工作流停止时，所有参与者都缺少数据。Director会发现这种饥饿，并停止工作流程。注意：如果不确定性是可以接受的，则可以使用Stop actor。
    
+ **端口**
  + 输入(input):接受布尔tocken的多端口。当该端口接收到一个true token时，工作流就停止了。如果该端口未连接，则当actor触发时，actor请求暂停。
  ![](https://github.com/jennyzhang8800/FlowControl/blob/master/pictures/StopActor.PNG)
   
  
