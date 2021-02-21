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
keyQuery = ['查看团队', '查询团队', '查看', '查询']
keyEnroll = ['报名']
keyDisenroll = ['取消报名', '退出']
keyDeleteTeam = ['取消开团', '删除团队']
keyHelp = ['帮助']
keyAuthor = ['制作人员']
#miraiURL = 'http://0.0.0.0:8080'

def containKeys(text, keys=['pt', 'yx', '普通', '英雄', '25']):
    for key in keys:
        if key in text:
            return True

    return False

class nsMember():
    def __init__(self, name, qid, fst_vocation, snd_vocation=None):
        self.name = name
        self.qid = qid
        self.fst_vocation = fst_vocation

    def printMember(self):
        return self.name + '(' + self.fst_vocation + ')'


class nsTeam():
    def __init__(self, leader, date, time, dungeon, comment=''):
        self.leader = leader
        self.date = date
        self.time = time
        self.dungeon = dungeon
        self.comment = comment

        self.members = []
        self.volume = 25 if containKeys(self.dungeon) else 10

    def printTeam(self, showMembers=False):
        msg = str(len(self.members)) + '/' + str(self.volume) + '人 ' + self.date + self.time + self.dungeon + self.comment
        if showMembers: # 是否显示队员
            msg += '\n'
            for i in range(len(self.members)):
                msg += ' ' + self.members[i].printMember()

        return msg

    def addMember(self, member):
        if len(self.members) < self.volume:
            valid = True
            for i in range(len(self.members)):
                if valid and self.members[i].name == member.name:
                    msg = member.name + '已经在该团队中！'
                    valid = False
            if valid:
                self.members.append(member)
                msg = member.name + '成功报名于' + self.date + self.time + self.dungeon + self.comment
        else:
            msg = '该团队已满！'

        return msg

    def removeMember(self, member):
        for i in range(len(self.members)):
            if self.members[i].name == member.name:
                self.members.remove(m)
        msg = member.name + '成功取消报名！'

        return msg


class nsQueue():
    def __init__(self):
        self.teams = []

    def printQueue(self, number=None):
        if not self.teams:
            msg = '当前没有团队！'
        else:
            if number is not None: # 查询单个团队
                try:
                    msg = self.teams[number].printTeam(showMembers=True)
                except:
                    msg = '该团队不存在！'
            else: # 查询所有团队
                msg = ''
                for i in range(len(self.teams)):
                    msg += str(i+1) + '. ' + self.teams[i].printTeam() + '\n'

        return msg

    def createNewTeam(self, qid, date, time, dungeon, comment=''):
        team = nsTeam(qid, date, time, dungeon, comment)
        self.teams.append(team)
        msg = '创建团队成功! ' + team.printTeam()

        return msg

    def removeTeam(self, qid, number):
        if self.teams[number].leader != qid:
            msg = '删除团队失败，没有该权限！'
        else:
            self.teams.remove(self.teams[number])
            msg = '删除团队成功！'

        return msg

    def addMember(self, teamNumber, member):
        try:
            msg = self.teams[teamNumber].addMember(member)
        except:
            msg = '该团队不存在！'

        return msg

    def removeMember(self, teamNumber, member):
        try:
            msg = self.teams[teamNumber].removeMember(member)
        except:
            msg = '该团队不存在！'

        return msg


def judge(miraiURL, session, db, message, qid, name, group, queue):
    if message[:2] != 'ns': #如果开头不是ns那么一切免谈，无事发生
        return

    ############## Main ###################
    command = message[2:].strip() #把ns去掉后面开始分割这个指令
    commandPart = command.split( ) #按照空格进行分割，但是后续要看看是不是加入更多的防傻判
断
    entrance = commandPart[0].strip()

    if entrance in keyNewTeam:
        try: #尝试解析参数，如果出错说明输入参数有误
            date = commandPart[1].strip()
            time = commandPart[2].strip()
            dungeon = commandPart[3].strip()
            comment = commandPart[4].strip()
        except:
            mirai.throwError(miraiURL=miraiURL, session=session, target=group, errCode=100)

        try: #尝试解析是否指定了黑名单
            useBlackList = commandPart[5].strip()
        except:
            useBlackList = 0

        msg = queue.createNewTeam(qid, date, time, dungeon, comment)
        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")
        #res = createNewTeam(db, date, time, dungeon, comment, useBlackList, QQ)
        #if res == 0:
        #    temp='收到开团指令 日期：{} 时间：{} 副本名称：{} 注释：{} 是否启用黑名单：{}'.format(date, time, dungeon, comment, useBlackList)
        #    print(temp)
        #    mirai.sendGroupMessage(miraiURL, session, target=group, content=temp, messageType="TEXT")
        #elif res == 1:
        #    print("权限错误")
        #    mirai.throwError(miraiURL=miraiURL, session=session, target=group, errCode=400)

    elif entrance in keyQuery:
        try:
            teamNumber = int(commandPart[1].strip())-1
        except:
            teamNumber = None

        msg = queue.printQueue(teamNumber)
        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")

    elif entrance in keyEnroll:
        msg = ''

        try:
            vocation = commandPart[1].strip()
            #assert(vocation in vocationList) TODO 增加职业检查
        except:
            msg += '缺少角色职业 '

        try:
            teamNumber = int(commandPart[2].strip())-1
        except:
            msg += '缺少团队编号 '

        try:
            memberName = commandPart[3].strip()
        except:
            msg += '缺少角色名称 '

        try:
            member = nsMember(memberName, qid, vocation)
            msg = queue.addMember(teamNumber, member)
        except:
            msg = '新建成员错误'

        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")

    elif entrance in keyDisenroll:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())-1
        except:
            msg += '缺少团队编号 '

        try:
            memberName = commandPart[2].strip()
        except:
            msg += '缺少角色名称 '

        try:
            member = nsMember(memberName, qid, None)
            msg = queue.removeMember(teamNumber, member)
        except:
            msg = '新建成员错误'

        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")

    elif entrance in keyDeleteTeam:
        try:
            teamNumber = int(commandPart[1].strip())-1
            msg = queue.removeTeam(qid, teamNumber)
        except:
            msg = '缺少团队编号'

        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")

    elif entrance in keyHelp:
        msg = '制作中WIP'
        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")

    elif entrance in keyAuthor:
        msg = '特别致谢：Magicat'
        mirai.sendGroupMessage(miraiURL, session, target=group, content=msg, messageType="TEXT")


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

    return 0


