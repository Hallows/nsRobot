import pymysql
import init
import time as pytime

db = None

#传入一个到数据库的连接
#-------输入---------
#mydb:有效的数据库连接
def SQLConnect(mydb):
    global db
    db=mydb

#验证是否存在某位团长
#-------输入---------
#leaderQQ:团长的QQ号
#-------输出---------
#如果不存在此团长，或团长的审核状态为未通过，则返回-1
#如果团长正常存在，返回该团长在数据库内的ID用于后续操作
def hasLeader(leaderQQ):
    global db
    cursor = db.cursor()
    command="SELECT * FROM ns_leader WHERE QQNumber = '{}' AND effective = 0".format(leaderQQ)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    else:
        cursor.close()
        return - 1  #权限错误

#创建一个团队
#-------输入---------
#date:开团日期（格式示例:'2021-02-09'）
#Time:开团时间（格式示例:'21:05'）
#dungeon:副本名称，字符串
#comment:要求与说明，字符串
#useBlackList：是否启用黑名单，1为启用0为不启用，默认为0
#leaderID:团长的数据库ID，从has_Leader函数获取，此处不校验真实性！
#-------输出---------
#如果开团成功，返回新开团队的团队ID
#如果开团失败，返回-1
def createNewTeam(date, time, dungeon, comment, leaderID, useBlackList=0):
    global db
    cursor = db.cursor()
    try:
        command = "INSERT INTO ns_team(leaderID,dungeon,startDate,startTime,effective,allowBlackList,remark) VALUES({},'{}','{}','{}',0,{},'{}')".format(leaderID, dungeon, date, time, useBlackList, comment)
        cursor.execute(command)
        db.commit()
        command = "SELECT * FROM ns_team WHERE startDate='{}' AND leaderID={} AND startTime='{}'".format(date, leaderID, time)
        cursor.execute(command)
    except Exception as ex:
        print(str(ex))
        db.rollback()
        cursor.close()
        return -1 #开团失败
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    else:
        cursor.close()
        return - 1  #开团失败

#利用诨名获取心法相关信息
#-------输入---------
#mentalName:输入的心法诨名，将尝试在别名和正式命名中双重匹配
#needFullName:返回设定，如果不为0则返回心法的正式名称，默认为0即仅返回心法ID
#-------输出---------
#如果不存在此心法则返回-1
#如果匹配成功，返回此心法的ID或全名
def getMental(mentalName,needFullName=0):
    global db
    cursor = db.cursor()
    command = "SELECT * FROM ns_mental WHERE acceptName LIKE '%{}%' OR mentalName='{}'".format(mentalName,mentalName)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        cursor.close()
        if needFullName == 0:
            return result[0]
        else:
            fullName=result[1]
            return fullName
    else:
        cursor.close()
        return - 1  #无法获取心法

#向指定团队添加报名记录
#-------输入---------
#teamID:报团的团ID，由用户传入
#QQ:用户的QQ号，通过mirai直接获取
#nickName:用户输入的角色名
#mentalID:心法ID，通过getMental方法获取
#syana:是否双修心法，默认为0即不双修
#-------输出---------
#报名成功返回0
#如果此QQ已经有在此团队的报名记录则返回-1
#如果传入参数错误返回-2
#如果团队不存在返回-3（过期的团队视为不存在）
def addMember(teamID, QQ, nickName, mentalID, syana=0):
    global db
    cursor = db.cursor()
    command = "SELECT * FROM ns_team WHERE teamID={} AND effective=0".format(teamID)
    cursor.execute(command)
    if cursor.rowcount == 0:
        cursor.close()
        return -3
    command = "SELECT * FROM ns_member WHERE teamID={} AND memberQQ={}".format(teamID, QQ)
    cursor.execute(command)
    if cursor.rowcount == 0:
        try:
            command = "INSERT INTO ns_member(teamID,memberQQ,memberNickname,mentalID,syana) VALUES({},'{}','{}',{},{})".format(teamID,QQ,nickName,mentalID,syana)
            cursor.execute(command)
            db.commit()
        except Exception as ex:
            print(str(ex))
            cursor.close()
            return - 2  #写入错误
        cursor.close()
        return 0
    else:
        cursor.close()
        return - 1  #传入QQ在此团队已经有报名记录

#从指定团队中删除传入QQ的所有报名记录
#-------输入---------
#teamID:报团的团ID，由用户传入
#QQ:用户的QQ号，通过mirai直接获取
#-------输出---------
#报名成功返回0
#如果此QQ没有在此团队的报名记录则返回-1
#如果传入参数错误返回-2
#如果团队不存在或者已过期，返回-3
def delMember(teamID, QQ):
    global db
    cursor = db.cursor()
    command = "SELECT * FROM ns_team WHERE teamID={} AND effective=0".format(teamID)
    cursor.execute(command)
    if cursor.rowcount == 0:
        cursor.close()
        return -3 #团队不存在或已过期
    command = "SELECT * FROM ns_member WHERE teamID={} AND memberQQ={}".format(teamID, QQ)
    cursor.execute(command)
    if cursor.rowcount != 0:
        try:
            command = "DELETE FROM ns_member WHERE teamID={} AND memberQQ={}".format(teamID, QQ)
            cursor.execute(command)
            db.commit()
        except Exception as ex:
            print(str(ex))
            cursor.close()
            return - 2  #数据库写入错误
        cursor.close()
        return 0
    else:
        cursor.close()
        return - 1  #传入QQ没有在团队有报名记录

#撤销开团
#-------输入---------
#teamID:报团的团ID，由用户传入
#leaderID:团长的ID（只有自己才能撤销自己的开团）
#-------输出---------
#撤销成功返回0
#如果传入的团队不存在返回-1
#如果传入的团长不是传入团队的发起者返回-2
#数据库写入错误返回-3
def delTeam(teamID, leaderID:int):
    global db
    cursor = db.cursor()
    command = "SELECT * FROM ns_team WHERE teamID={}".format(teamID)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        if int(leaderID) == int(result[1]):
            try:
                command = "UPDATE ns_team SET effective=1 WHERE teamID={}".format(teamID)
                cursor.execute(command)
                db.commit()
            except Exception as ex:
                print(str(ex))
                cursor.close()
                return - 3  #数据库写入错误
            cursor.close()
            return 0
        else:
            cursor.close()
            return - 2  #传入的团长ID不是开团者
    else:
        cursor.close()
        return - 1  #查无此团

#添加一条团长申请
#-------输入---------
#QQ:新团长的QQ，从mirai获取
#nickName:新团长的昵称
#activeTime:活跃时间
#-------输出---------
#添加成功返回0
#如果此QQ已经报名但是没有通过审核，返回-1
#如果此QQ已经是通过审核的团长，返回-2
def newLeader(QQ, nickName, activeTime):
    global db
    cursor = db.cursor()
    command = "SELECT * FROM ns_leader WHERE QQNumber={} AND effective=1".format(QQ)
    cursor.execute(command)
    if cursor.rowcount != 0:
        cursor.close()
        return - 1
    else:
        command = "SELECT * FROM ns_leader WHERE QQNumber={}".format(QQ)
        cursor.execute(command)
        if cursor.rowcount != 0:
            cursor.close()
            return - 2
        else:
            command = "INSERT INTO ns_leader(QQNumber,nickName,activeTime,effective) VALUES('{}','{}','{}',1)".format(QQ, nickName, activeTime)
            cursor.execute(command)
            db.commit()
            cursor.close()
            return 0

#获取所有在开团队
#无输入
#-------输出---------
#如果当前没有在开团队，返回空列表
#如果存在在开团队，返回一个列表，其中每个团队独立一个字典，字典格式为：
#团队ID-teamID-int
#团长名字-leaderName-str
#团队名称-dungeon-str
#开组时间-startTime-str(仅返回月日时分)
#注释-comment-str
#
#返回的列表样例如下所示：
#[
#   {'teamID': 1000, 'leaderName': '渡空离', 'dungeon': 'test', 'startTime': '02-24 11:00', 'comment': 'test'},
#   {'teamID': 1001, 'leaderName': '辰韶', 'dungeon': '达摩洞', 'startTime': '12-31 21:00', 'comment': '25pt达摩洞，来十人熟手'}
# ]
def getTeam():
    global db
    updateDB()
    cursor = db.cursor()
    command = "SELECT * FROM ns_team WHERE effective=0"
    cursor.execute(command)
    out=[]
    if cursor.rowcount != 0:
        results = cursor.fetchall()
        for row in results:
            teamID = row[0]
            leaderID = row[1]
            dungeon = row[2]
            date = row[3]
            time = row[4]
            comment=row[7]
            startTime = "%s %s" % (date, time)
            startTime = startTime[5:]
            command = "SELECT * FROM ns_leader WHERE id={}".format(leaderID)
            cursor.execute(command)
            result = cursor.fetchone()
            leaderName=result[2]
            temp = {'teamID': teamID, 'leaderName': leaderName, 'dungeon': dungeon, 'startTime': startTime, 'comment':comment}
            out.append(temp)
    cursor.close()
    return out
        
#扫描数据库并更新团队状态，清理所有过期团队
#无输入
#无输出
def updateDB():
    global db
    cursor = db.cursor()
    command = "SELECT * FROM ns_team WHERE effective=0"
    cursor.execute(command)
    if cursor.rowcount != 0:
        results = cursor.fetchall()
        for row in results:
            teamID=row[0]
            date = row[3]
            time = row[4]
            dbtime = "%s %s"%(date,time)
            nowtime = pytime.strftime("%Y-%m-%d %H:%M", pytime.localtime())
            if dbtime < nowtime:
                closeTeam = "UPDATE ns_team SET effective=1 WHERE teamID={}".format(teamID)
                cursor.execute(closeTeam)
                db.commit()
                continue
        cursor.close()
        return
    else:
        cursor.close()
        return

#获取指定团队的状态
#-------输入---------
#teamID:团队ID
#needYear:可选，是否返回年
#-------输出---------
#如果团队不存在，返回空字典
#如果存在团队，返回一个字典，格式为：
#团队ID-teamID-int
#团长名字-leaderName-str
#团队名称-dungeon-str
#开组时间-startTime-str(仅返回月日时分)，例如02-24 19:00
#注释-comment-str
#团长ID-leaderID-str
#开团日期-date-格式：2021-02-24
#开团时间-time-格式：11:00
#例如：
#{'teamID': 1002, 'leaderName': '渡空离', 'dungeon': '25YX达摩洞', 'startTime': '01-31 20:00', 'comment': '25YX', 'leaderID': 1, 'date': '2021-01-31', 'time': '20:00'}
#如果指定了needYear，会在上述内容上额外增加一个'year'返回四位年份
def getInfo(teamID,needYear=0):
    global db
    out={}
    cursor = db.cursor()
    command = "SELECT * FROM ns_team WHERE teamID={}".format(teamID)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        teamID = result[0]
        leaderID = result[1]
        dungeon = result[2]
        date = result[3]
        time = result[4]
        comment=result[7]
        startTime = "%s %s" % (date, time)
        startTime = startTime[5:]
        command = "SELECT * FROM ns_leader WHERE id={}".format(leaderID)
        cursor.execute(command)
        result = cursor.fetchone()
        leaderName = result[2]
        out = {'teamID': teamID, 'leaderName': leaderName, 'dungeon': dungeon, 'startTime': startTime, 'comment': comment, 'leaderID': leaderID, 'date': date, 'time': time}
        if needYear != 0:
            out = {'teamID': teamID, 'leaderName': leaderName, 'dungeon': dungeon, 'startTime': startTime, 'comment': comment, 'leaderID': leaderID, 'date': date, 'time': time,'year':date[:4]}
        cursor.close()
        return out
    else:
        cursor.close()
        return out

#获取指定心法的阵眼
#-------输入---------
#mentalID:心法ID，可从getMental获取
#-------输出---------
#如果心法不存在，返回空字典
#如果存在，返回一个字典，格式为：
#阵眼名称-formationName
#一重-levelOne
#二重-levelTwo
#三重-levelThree
#四重-levelFour
#五重-levelFive
#六重-levelSix
#不返回七重（七重归一，空）
def getFormation(mentalID):
    global db
    out = {}
    cursor = db.cursor()
    command = "SELECT * FROM ns_formation WHERE mentalID={}".format(mentalID)
    cursor.execute(command)
    if cursor.rowcount == 1:
        result = cursor.fetchone()
        out = {'formationName': result[1], 'levelOne':result[2], 'levelTwo':result[3], 'levelThree':result[4], 'levelFour':result[5], 'levelFive':result[6], 'levelSix':result[7]}
        cursor.close()
        return out
    else:
        cursor.close()
        return out

#获取指定心法的信息
#-------输入---------
#mentalID:心法ID，可从getMental获取
#-------输出---------
#如果心法不存在，返回空字典
#如果存在，返回一个字典，格式为：
#心法官方名-name-str
#心法图标-icon-str
#心法颜色-color-str
#心法职能-works-int
#同门派心法-relation-int
#示例：
#{'name': '傲血战意', 'icon': 'axzy.png', 'color': 'ff6f53', 'works': 4, 'relation': 11}
def getMentalInfo(mentalID):
    global db
    out={}
    cursor = db.cursor()
    command = "SELECT * FROM ns_mental WHERE mentalID={}".format(mentalID)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        cursor.close()
        out={'name':result[1],'icon':result[2],'color':result[4],'works':result[5],'relation':result[6]}
        return out
    else:
        cursor.close()
        return out

#获取指定团队的所有报团人员
#-------输入---------
#teamID:团队ID
#-------输出---------
#如果团队不存在或者没有人报团返回空列表
#如果团队有人报团，则返回一个“列表-字典”的嵌套结构，其外层为一个列表，其中每个值为一个字典，存储了一个人的报团记录，字典的格式为：
#报团QQ号-QQNumber
#报团的角色昵称-nickName
#是否双修-syana-int-0为不双修，1为双修
#主心法的颜色-mentaColor
#主心法的图片-mainMentalIcon
#主心法的职能-mentalWorks-int
#双修心法的图标-secMentalIcon-如果是双修，此项为一个str，否则为None
#一个简略版的返回示例如下所示：
# [
#     {'QQNumber': '1263046789', 'nickName': '尹洛洛', 'syana': 0, 'mentalColor': 'ff81b0', 'mainMentalIcon': 'bxj.png', 'mentalWorks': 3, 'secMentalIcon': None},
#     {'QQNumber': '2906604935', 'nickName': '林籁', 'syana': 1, 'mentalColor': 'f04660', 'mainMentalIcon': 'mzllt.png', 'mentalWorks': 1, 'secMentalIcon': 'fysj.png'},
#       ...
#     {'QQNumber': '2946155251', 'nickName': '松下溪', 'syana': 0, 'mentalColor': 'b43c00', 'mainMentalIcon': 'fsj.png', 'mentalWorks': 4, 'secMentalIcon': None}
# ]
def getMember(teamID):
    global db
    out=[]
    cursor = db.cursor()
    command = "SELECT * FROM ns_member WHERE teamID={}".format(teamID)
    cursor.execute(command)
    if cursor.rowcount != 0:
        results = cursor.fetchall()
        cursor.close()
        for row in results:
            mentalID=int(row[3])
            if int(row[4]) == 1:
                primaryMentalInfo = getMentalInfo(mentalID=mentalID)
                if primaryMentalInfo['relation'] != 0:
                    secondaryMentaInfo = getMentalInfo(mentalID=primaryMentalInfo['relation'])
                else:
                    temp = {'QQNumber': row[1], 'nickName': row[2], 'syana': 0, 'mentalColor': primaryMentalInfo['color'], 'mainMentalIcon': primaryMentalInfo['icon'], 'mentalWorks': primaryMentalInfo['works'], 'secMentalIcon': None}
                    out.append(temp)
                    continue
                temp = {'QQNumber': row[1], 'nickName': row[2], 'syana': 1, 'mentalColor': primaryMentalInfo['color'], 'mainMentalIcon': primaryMentalInfo['icon'], 'mentalWorks': primaryMentalInfo['works'], 'secMentalIcon': secondaryMentaInfo['icon']}
                out.append(temp)
            else:
                primaryMentalInfo = getMentalInfo(mentalID=mentalID)
                temp = {'QQNumber': row[1], 'nickName': row[2], 'syana': 0, 'mentalColor': primaryMentalInfo['color'], 'mainMentalIcon': primaryMentalInfo['icon'], 'mentalWorks': primaryMentalInfo['works'], 'secMentalIcon': None}
                out.append(temp)
        return out
    else:
        cursor.close()
        return out