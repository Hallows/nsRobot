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
    command="SELECT * FROM ns_leader WHERE QQNumber = '{}' AND effective = 0".format(QQ)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        return result[id]
    else:
        return - 1  #权限错误

#创建一个团队
#-------输入---------
#db:有效的数据库连接
#date:开团日期（格式示例:'2021-02-09'）
#Time:开团时间（格式示例:'21:05:00'）
#dungeon:副本名称，字符串
#comment:要求与说明，字符串
#useBlackList：是否启用黑名单，1为启用0为不启用，默认为0
#leaderID:团长的数据库ID，从has_Leader函数获取，此处不校验真实性！
#-------输出---------
#如果开团成功，返回新开团队的团队ID
#如果开团失败，返回-1
def createNewTeam(db, date, time, dungeon, comment:0, useBlackList,leaderID):
    cursor = db.cursor()
    inputTime="{} {}".format(date,time)
    command="INSERT INTO ns_team(leaderID,dungeon,startTime,effective,allowBlackList,remark) VALUES({},{},{},0,{},{})".format(leaderID,dungeon,inputTime,useBlackList,remark)
    cursor.execute(command)
    command = "SELECT * FROM  ns_team WHERE startTime={}".format(inputTime)
    cursor.execute(command)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        return result[teamID]
    else:
        return -1 #开团失败