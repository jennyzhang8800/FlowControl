### 1. 测试页面
  
* 在/var/www/目录下新建FlowControl目录
    ```
           cd /var/www
           sudo mkdir FlowControl
     ```
    
* 在FlowControl目录下新建5个测试页面（index.html,1.html,2.html,3.html,4.html）

    + **index.html**: 是导航页面，初始时在导航页面用户不能直接访问1，2,3,4中的任何一个页面
    + **1.html**: 是流程开始的第一个页面，当用户在index.html中点击“1.html”时，要求输入用户名密码进行验证，只有合法用户才能访问。有关页面访问控制是如何实现的，参见：
    + **2.html**: 当用户进入1.html后，如果点击“submit”按扭，则页面跳转到2.html 。此时如果返回到index.html,我们再点击“1.html”和“2.html”中任何一项，都是可以直接访问的。因为在1.html中点击submit按钮时，会触发后台/script/index.py脚本中的jump2函数，该函数调用addUser.sh脚本把当前用户加入到可以访问2.html页面的用户列表中。
    + **3.html**:当用户进入2.html后，如果点击“submit”按扭，则页面跳转到3.html。此时如果返回到index.html,我们再点击“1.html”、“2.html”和“3.html”中任何一项，都是可以直接访问的。
    + **4.html**:当用户进入3.html后，如果点击“submit”按扭，则页面跳转到4.html。此时如果返回到index.html,我们再点击“2.html”和“3.html”中任何一项，就不可以再直接访问了。因为在3.html中点击submit按钮时，会触发后台/script/index.py脚本中的jump4函数，该函数调用moveUser.sh脚本把当前用户从可以访问2.html和3.html页面的用户列表中删除。

       以上测试页面实现了对单个页面访问权限的控制，以及动态添加，删除用户对不同页面的访问。

### 2. 脚本文件

* 在/var/www/目录下新建script目录，存放实验涉及到的脚本
```
        cd /var/www
        sudo mkdir script
```

* script下有三个脚本
        
       + **index.py** :是后面与前台进行交互的脚本，需要修改mod_python的支持以及修改apache配置文件。
                  index.py中定义了三个函数：jump2(),jump3(),jump4()。这三个函数分别实现在不同页面进行用户权限的更改。函数中调用addUser.sh实现用户加入到可访问页面列表中，removeUser.sh实现把用户从可访问该页面的列表中删除。
       + **addUser.sh**:实现给用户授权页面访问
       + **removeUser.sh**:收回用户访问页面权限

### 3. mod_python的配置
[点击查看](http://blog.csdn.net/jenyzhang/article/details/44985645)

  index.py的使用需要在apache的配置文件中作如下修改：
      在/etc/apache2/apache2.conf文件中加入下面的内容：
      
           <Directory /var/www/script>
                 setHandler mod_python
                 PythonHandler mod_python.publisher
            </Directory>
           

### 4. 页面权限控制的实现

 [点击查看](http://blog.csdn.net/jenyzhang/article/details/51604718)
 
### 5. 实验示例

  * **index.html页面**
  
![1.png](https://github.com/jennyzhang8800/FlowControl/blob/master/20160624-apache%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%AE%9E%E9%AA%8C/pictures/1.PNG)
   
   **注意：此时点击任何一个按钮都不能直接访问到相关页面**
   
  * **点击index.html页面中的1.html按钮，要求用户认证**
![2.png](https://github.com/jennyzhang8800/FlowControl/blob/master/20160624-apache%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%AE%9E%E9%AA%8C/pictures/2.PNG)

  * **输入用户名，密码认证成功后能进入到1.html中。**
  
   此时如果返回到index.html，再次点击1.html按钮，是可以直接访问1.html页面的，无需再次认证。（调用addUser.sh可实现为页面添加用户）
![3.png](https://github.com/jennyzhang8800/FlowControl/blob/master/20160624-apache%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%AE%9E%E9%AA%8C/pictures/3.PNG)

  * **点击1.html页面中的submit按钮，可直接跳到2.html。**
  
    此时如果返回到index.html，点击1.html，2.html按钮中任何一个，是可以直接访问页面的
    
  * **点击2.html页面中的submit按钮，可直接跳到3.html。**
  
    此时如果返回到index.html，点击1.html，2.html,3.html按钮中任何一个，是可以直接访问页面的
![4.png](https://github.com/jennyzhang8800/FlowControl/blob/master/20160624-apache%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6%E5%AE%9E%E9%AA%8C/pictures/4.PNG)

  * **点击3.html页面中的submit按钮，可直接跳到4.html。**
  
    此时如果返回到index.html，点击2.html,3.html按钮中任何一个，己经不可以直接访问页面了。因为后台脚本己经把用户从该页面中删除（调用removeUser.sh）
![5.png](https://github.com/jennyzhang8800/FlowControl/blob/master/20160624-apache流程控制实验/pictures/5.PNG)
![6.png](https://github.com/jennyzhang8800/FlowControl/blob/master/20160624-apache流程控制实验/pictures/6.PNG)


**以上实验过程中可以看出：可以实现对用户访问页面权限的动态添加与删除。**
   

    
