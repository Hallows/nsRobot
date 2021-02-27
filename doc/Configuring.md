# 南山机器人-部署教程
##### 待到秋来九月八，我花开后百花杀
> 此机器人是基于[mirai](https://github.com/mamoe/mirai)，[mirai-console](https://github.com/mamoe/mirai-console)，[Mirai Http](https://github.com/project-mirai/mirai-api-http)以及[Graia Application for mirai-api-http](https://github.com/GraiaProject/Application)实现的，在此我们假定您已经完成了上述框架的部署，启动了mirai-console，并且从net.mamoe.mirai.api.http.config.Setting取得了authKey  
> 此机器人采用的数据库为mysql，在此我们也假定您安装好了mysql，配置并启动成功，且新建了一个名为ns_db的数据库，在数据库建立完成后，可以使用ns_db.sql文件构建ns_db数据库中的表和数据  
> 请在开始之前，安装python3.8或以上版本并使用`pip install -r requirements.txt`安装所需依赖

## 部署nsBot
从Release中下载最新的发布版，将其解压到任一目录中
## 配置nsBot 
在解压出的目录下找到`init.py`。**请记住，所有关于机器人的设置全部集中在init.py文件中**  
在init中，我们需要修改的是：
```python
#数据库相关
dbUser = ''
dbPassword = ''
dbName = 'ns_db'
dbCharset = 'utf8'
```
这里的dbUser和dbPassword的值需要为你的数据库的用户名和密码
```python
#mirai相关
IMAGE_PATH = ""
miraiQQ =
miraiKey = ''
```
这里的IMAGE_PATH应为你Mirai Http所要求的图片路径，一般的，应该为在mirai路径下的/data/net.mamoe.mirai-api-http/images/文件夹  
miraiQQ为你机器人的账号，要注意，这个账号应当已经在mirai-console中登录过，以及这个值应为int型。miraiKey应为先前所获取的authKey
```python
#日常相关
SERVER = ''
```
这里的SERVER的值为日常查询模块中的默认服务器

## 启动nsBot
在上述设置完成后，可以执行`python3 nsBot.py`以启动机器人，一般的，如果成功启动，你将会得到`nsRobot Running!`的返回值，若出现异常，请根据异常抛出的问题进行解决。