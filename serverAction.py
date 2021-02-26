#动作指令判断函数，在此函数内判断需要采取的动作并起调相关子处理函数
#输入-message: 收到的全文本信息
#输入-QQ: 发信息的QQ号，通过主程序传递即可
#输入-name: 发来信息的昵称，用于后续相关确认通知，虽然大概率新版本不需要这样了
#输入-group: 接收到信息的群聊ID，用于后续相关确认通知，虽然大概率新版本不需要这样了
#输入-db: 数据库链接，在主程序建立到数据库的链接后直接将数据库作为对象传入即可
import sqlConnect as sql
import MiraiConnnect as mirai
import generate_image as img
from utils import parseDate, parseTime

keyNewTeam = ['开团', '新建团队', '创建团队']
keyShowall = ['全团显示', '显示全团', '查看全团', '全团查看']
keyQuery = ['查看团队', '查询团队', '查团']
keyEnroll = ['报名', '报团', '报名团队']
keyDisenroll = ['取消报名', '退团', '撤销报团', '取消报团', '撤销报名']
keyDeleteTeam = ['取消开团', '删除团队', '撤销团队', '撤销开团']
keyMacro = ['宏']
keyHelp = ['帮助', '指令', '查看指令','指令清单']
keyAuthor = ['作者', '制作团队', '制作名单']


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
        self.snd_vocation = snd_vocation

    def printMember(self):
        return self.name + '(' + self.fst_vocation + ')'


class nsTeam():
    def __init__(self, teamID, leader, date, time, dungeon, comment=''):
        self.teamID = teamID
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
            msg = img.GetImg(self.teamID)
            #msg += '\n'
            #for i in range(len(self.members)):
            #    msg += ' ' + self.members[i].printMember()

        return msg

    def addMember(self, member):
        if len(self.members) < self.volume:
            valid = True
            for i in range(len(self.members)):
                if valid and self.members[i].name == member.name:
                    msg = member.name + '已经在该团队中！'
                    valid = False
            if valid:
                if sql.addMember(self.teamID, member.qid, member.name, member.fst_vocation) < 0:
                    msg = '数据库错误！'
                else:
                    self.members.append(member)
                    msg = member.name + '成功报名于' + self.date + self.time + self.dungeon + self.comment
        else:
            msg = '该团队已满！'

        return msg

    def removeMember(self, member):
        for i in range(len(self.members)):
            if self.members[i].qid == member.qid:
                sql.delMember(self.teamID, member.qid)
                self.members.remove(self.members[i])
        msg = member.name + '成功取消报名！'

        return msg


class nsQueue():
    def __init__(self):
        self.teams = []

    def printQueue(self, number=None):
        if not self.teams:
            msg = '当前没有团队！'
        else:
            if number is not None: # 查询指定团队
                try:
                    msg = self.teams[number].printTeam(showMembers=True)
                except Exception as ex:
                    print(str(ex))
                    msg = '该团队不存在！'
            else: # 查询所有团队
                msg = ''
                for i in range(len(self.teams)):
                    msg += str(i+1) + '. ' + self.teams[i].printTeam() + '\n'

        return msg

    def createNewTeam(self, qid, date, time, dungeon, comment='', useBlackList=0):
        leader = sql.hasLeader(qid)
        if leader == -1:
            msg = '团长错误！'
        else:
            teamID = sql.createNewTeam(date, time, dungeon, comment, leader, useBlackList)
            if teamID == -1:
                msg = '数据库错误！'
            else:
                team = nsTeam(teamID, qid, date, time, dungeon, comment)
                self.teams.append(team)
                msg = '创建团队成功! ' + team.printTeam()

        return msg

    def removeTeam(self, qid, number):
        if number < 0 or number > len(self.teams)-1:
            msg = '该团队不存在！'
        else:
            if qid != self.teams[number].leader:
                msg = '删除团队失败，没有该权限！'
            else:
                if sql.delTeam(self.teams[number].teamID, qid) == 0:
                    self.teams.remove(self.teams[number])
                    msg = '删除团队成功！'
                else:
                    msg = '数据库错误！'

        return msg

    def addMember(self, teamNumber, member):
        try:
            msg = self.teams[teamNumber].addMember(member)
        except Exception as ex:
            print(str(ex))
            msg = '该团队不存在！'

        return msg

    def removeMember(self, teamNumber, member):
        try:
            msg = self.teams[teamNumber].removeMember(member)
        except Exception as ex:
            print(str(ex))
            msg = '该团队不存在！'

        return msg


def judge(message, qid, name, group, queue):
    if message[:2] != 'ns': #如果开头不是ns那么一切免谈，无事发生
        return

    ############## Main ###################
    command = message[2:].strip() #把ns去掉后面开始分割这个指令
    commandPart = command.split( ) #按照空格进行分割，但是后续要看看是不是加入更多的防傻判断
    entrance = commandPart[0].strip()

    if entrance in keyNewTeam:
        try: #尝试解析参数，如果出错说明输入参数有误
            date = parseDate(commandPart[1].strip())
            time = parseTime(commandPart[2].strip())
            dungeon = commandPart[3].strip()
            comment = commandPart[4].strip()
            assert(date != -1)
            assert(time != -1)
        except:
            mirai.throwError(target=group, errCode=100)
            return

        try: #尝试解析是否指定了黑名单
            useBlackList = commandPart[5].strip()
        except:
            useBlackList = 0

        #try:
        #    msg = queue.createNewTeam(qid, date, time, dungeon, comment, useBlackList)
        #except:
        #    msg = '新建团队失败'

        leader = sql.hasLeader(qid)
        if leader == -1:
            msg = '权限错误，请先申请成为团长'
        else:
            res = sql.createNewTeam(date, time, dungeon, comment, leader, useBlackList)
            if res == -1:
                msg = '数据库错误！'
            else:
                msg = '开团成功，{}，团队ID为{}, 集合时间{} {}'.format(dungeon, res, date, time)

        #msg = queue.createNewTeam(qid, date, time, dungeon, comment, useBlackList)
        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyShowall:
        res = sql.getTeam()
        if not res:
            msg = '当前没有在开团队'
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")
            return
        else:
            msg = ''
            for i in range(len(res)):
                g = res[i]
                msg += '{}. ID：{} {} {} {} {} \n'.format(str(i+1), 
                        g['teamID'], g['leaderName'], g['dungeon'], 
                        g['startTime'], g['comment'])
                msg += '--------------------------- \n'

        mirai.sendGroupMessage(target=group, content="在开团队已经通过临时会话发给您了~", messageType="TEXT",needAT=True,ATQQ=qid)
        mirai.sendTempMessage(target=group,QQ=qid,content=msg,messageType="TEXT")
    
    elif entrance in keyQuery:
        try:
            teamNumber = int(commandPart[1].strip())
        except:
            teamNumber = None

        #try:
        #    msg = queue.printQueue(teamNumber)
        #except:
        #    isValid = False # 非图片url通道
        #    msg = '查询错误'

        res = sql.getTeam()
        if not res or teamNumber is None:
            msg = '输入的团队ID不存在'
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")
        else:
            image = img.GetImg(teamNumber)
            if image == -1:
                msg = '此团队目前没有人报名'
                mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")
            else:
                mirai.sendGroupMessage(target=group, content=image, messageType="Image")
        #msg = queue.printQueue(teamNumber)
        #mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyEnroll:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())
        except:
            msg += '缺少团队ID '

        try:
            vocation = commandPart[2].strip()
            mental = sql.getMental(vocation)
            assert(mental != -1) # 检查心法是否存在
        except:
            msg += '缺少角色心法 '

        try:
            memberName = commandPart[3].strip()
        except:
            msg += '缺少角色名称 '

        try:
            syana = int(commandPart[4].strip())
            assert(syana==1 or syana==0)
        except:
            syana = 0

        #try:
        #    member = nsMember(memberName, qid, vocation)
        #    msg = queue.addMember(teamNumber, member)
        #except:
        #    msg += '新建队员错误'

        if msg == '':
            res = sql.addMember(teamNumber, qid, memberName, mental, syana)
            if res == 0:
                team = sql.getInfo(teamNumber)
                msg = '已成功报名 {} {}团长 {} {}-{}'.format(
                        team['startTime'], team['leaderName'], 
                        team['dungeon'], vocation, memberName)
            elif res == -1:
                msg = '已经在此团队中'
            elif res == -3:
                msg = '团队不存在或已过期'
            else:
                msg = '数据库错误！'

        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyDisenroll:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())
        except:
            msg += '缺少团队ID'

        #try:
        #    memberName = commandPart[2].strip()
        #except:
        #    msg += '缺少角色名称 '

        #try:
        #    member = nsMember('', qid, None)
        #    msg = queue.removeMember(teamNumber, member)
        #except:
        #    msg += '新建队员错误'

        if msg == '':
            res = sql.delMember(teamNumber, qid)
            if res == 0:
                team = sql.getInfo(teamNumber)
                msg = '已成功取消报名 {} {}团长'.format(
                        team['startTime'], team['leaderName'])
            elif res == -1:
                msg = '不在此团队中'
            elif res == -3:
                msg = '团队不存在或已过期'
            else:
                msg = '数据库错误！'

        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyDeleteTeam:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())
            #msg = queue.removeTeam(qid, teamNumber)
        except:
            msg = '缺少团队ID'

        if msg == '':
            leader = sql.hasLeader(qid)
            if leader == -1:
                msg = '权限错误，请先申请成为团长'
            else:
                res = sql.delTeam(teamNumber, leader)
                if res == 0:
                    msg = '团队{}已经取消'.format(teamNumber)
                elif res == -1:
                    msg = '此团队不存在'
                elif res == -2:
                    msg = '取消开团失败，没有该权限'
                else:
                    msg = '数据库错误！'

        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyMacro:
        msg = ''

        try:
            mental = sql.getMental(commandPart[1].strip())
            assert(mental != -1) # 检查心法是否存在
        except:
            msg += '缺少心法名称'
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)
            return

        if msg == '':
            try:
                with open('./macro/'+str(mental), 'r') as f:
                    lines = f.readlines()
                    msg = ' '.join(lines)
            except:
                msg = '心法文件错误'
                mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)
                return
       
        mirai.sendGroupMessage(target=group, content='宏命令已经通过临时会话私发给您了', messageType="TEXT",needAT=True,ATQQ=qid)
        mirai.sendTempMessage(target=group,QQ=qid,content=msg,messageType="TEXT")

    elif entrance in keyHelp:
        msg = '在线用户手册： \nhttps://github.com/Hallows/nsRobot/blob/main/doc/userGuide.md'
        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyAuthor:
        msg = '致谢与授权说明： \nhttps://github.com/Hallows/nsRobot/blob/main/README.md'
        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

