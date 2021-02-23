import pymysql

#验证是否存在某位团长
#-------输入---------
#db:有效的数据库连接
#leaderQQ:团长的QQ号
#-------输出---------
#如果不存在此团长，或团长的审核状态为未通过，则返回-1
#如果团长正常存在，返回该团长在数据库内的ID用于后续操作
def has_Leader(db, leaderQQ):
    cursor = db.cursor()
    command="SELECT * FROM ns_leader WHERE QQNumber = '{}' AND effective = 0".format(leaderQQ)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        return result[0]
    else:
        return - 1  #权限错误

#创建一个团队
#-------输入---------
#db:有效的数据库连接
#date:开团日期（格式示例:'2021-02-09'）
#Time:开团时间（格式示例:'21:05'）
#dungeon:副本名称，字符串
#comment:要求与说明，字符串
#useBlackList：是否启用黑名单，1为启用0为不启用，默认为0
#leaderID:团长的数据库ID，从has_Leader函数获取，此处不校验真实性！
#-------输出---------
#如果开团成功，返回新开团队的团队ID
#如果开团失败，返回-1
def createNewTeam(db, date, time, dungeon, comment, leaderID, useBlackList=0):
    cursor = db.cursor()
    try:
        command = "INSERT INTO ns_team(leaderID,dungeon,startDate,startTime,effective,allowBlackList,remark) VALUES({},'{}','{}','{}',0,{},'{}')".format(leaderID, dungeon, date, time, useBlackList, comment)
        cursor.execute(command)
        db.commit()
        command = "SELECT * FROM ns_team WHERE startDate='{}' AND leaderID={} AND startTime='{}'".format(date, leaderID, time)
        cursor.execute(command)
    except:
        db.rollback()
        return -1 #开团失败
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        return result[0]
    else:
        return - 1  #开团失败

#获取心法对应的心法ID
#-------输入---------
#db:有效的数据库连接
#mentalName:输入的心法名称，将尝试在别名和正式命名中双重匹配
#-------输出---------
#如果不存在此心法则返回-1
#如果匹配成功，返回此心法的ID
def getMental(db, mentalName):
    cursor = db.cursor()
    command = "SELECT * FROM ns_mental WHERE acceptName LIKE '%{}%' OR mentalName='{}'".format(mentalName)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        return result[0]
    else:
        return - 1  #无法获取心法

#向指定团队添加报名记录
#-------输入---------
#db:有效的数据库连接
#teamID:报团的团ID，由用户传入
#QQ:用户的QQ号，通过mirai直接获取
#nickName:用户输入的角色名
#mentalID:心法ID，通过getMental方法获取
#syana:是否双修心法，默认为0即不双修
#-------输出---------
#报名成功返回0
#如果此QQ已经有在此团队的报名记录则返回-1
#如果传入参数错误返回-2
def addMember(db, teamID, QQ, nickName, mentalID, syana=0):
    cursor = db.cursor()
    command = "SELECT * FROM ns_member WHERE teamID={} AND memberQQ={}".format(teamID, QQ)
    if cursor.rowcount == 0:
        try:
            command = "INSERT INTO ns_member(teamID,memberQQ,memberNickname,mentalID,syana) VALUES({},'{}','{}',{},{})".format(teamID,QQ,nickName,mentalID,syana)
            cursor.execute(command)
            db.commit()
            return 0
        except:
            return -2#写入错误
    else:
        return - 1  #传入QQ在此团队已经有报名记录

