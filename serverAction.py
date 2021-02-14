#动作指令判断函数，在此函数内判断需要采取的动作并起调相关子处理函数
#输入-message: 收到的全文本信息
#输入-QQ: 发信息的QQ号，通过主程序传递即可
#输入-name: 发来信息的昵称，用于后续相关确认通知，虽然大概率新版本不需要这样了
#输入-group: 接收到信息的群聊ID，用于后续相关确认通知，虽然大概率新版本不需要这样了
#输入-db: 数据库链接，在主程序建立到数据库的链接后直接将数据库作为对象传入即可
import pymysql
import MiraiConnnect as mirai
import supportComponent as support

keyNewTeam = ['开团','新建团队']
miraiURL = 'http://0.0.0.0:8080'

def judge(miraiURL,session,db,message, QQ, name, group):
    if message[:2] == 'ns': #如果开头不是ns那么一切免谈，无事发生
        command = message[2:] #把ns去掉后面开始分割这个指令
        commandPart = command.split( ) #按照空格进行分割，但是后续要看看是不是加入更多的防傻判断
        if commandPart[0] in keyNewTeam:
            try:#尝试解析参数，如果出错说明输入参数有误
                date = commandPart[1]
                time = commandPart[2]
                dungeon = commandPart[3]
                comment = commandPart[4]
            except:
                mirai.throwError(miraiURL=miraiURL, session=session, target=group, errCode=100)
            
            try:#尝试解析是否指定了黑名单
                useBlackList = commandPart[5]
            except:
                useBlackList = 0
            
            res = createNewTeam(db, data, time, dungeon, comment, useBlackList, QQ)
            if res == 0:
                temp='收到开团指令 日期：{} 时间：{} 副本名称：{} 注释：{} 是否启用黑名单：{}'.format(date,time,dungeon,comment,useBlackList)
                print(temp)
            elif res == 1:
                print("权限错误")
                mirai.throwError(miraiURL=miraiURL, session=session, target=group, errCode=400)
        #elif commandPart[0] in 

def createNewTeam(db, date, time, dungeon, comment, useBlackList,QQ):
    cursor = db.cursor()
    command="SELECT * FROM ns_leader WHERE QQNumber = '{}' AND effective = 0".format(QQ)
    cursor.execute(command)
    #insert into ns_team(teamID,leaderID,dungeon,startTime,effective,allowBlackList,remark) VALUES(1023,1,'25YX达摩洞','2021-02-09 21:03:33',0,0,'25YX');
    if cursor.rowcount != 0:
        print("got correct leader!")
        result = cursor.fetchone()
        
        cursor.execute(command)
    else:
        return 1 #权限错误