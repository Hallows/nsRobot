# 动作指令判断函数，在此函数内判断需要采取的动作并起调相关子处理函数
# 输入-message: 收到的全文本信息
# 输入-QQ: 发信息的QQ号，通过主程序传递即可
# 输入-name: 发来信息的昵称，用于后续相关确认通知，虽然大概率新版本不需要这样了
# 输入-group: 接收到信息的群聊ID，用于后续相关确认通知，虽然大概率新版本不需要这样了
# 输入-db: 数据库链接，在主程序建立到数据库的链接后直接将数据库作为对象传入即可
from time import strptime
import sqlConnect as sql
import MiraiConnnect as mirai
import generate_image as img
import jx3_query as jx3api
from utils import parseDate, parseTime, parseWeekday
import time as Lib_Time
try:
    import init
except ImportError:
    print("can not find init file")

keyNewTeam = ['开团', '新建团队', '创建团队']
keyShowall = ['全团显示', '显示全团', '查看全团', '全团查看', '团队列表']
keyQuery = ['查看团队', '查询团队', '查团']
keyEnroll = ['报名', '报团', '报名团队']
keyDisenroll = ['取消报名', '退团', '撤销报团', '取消报团', '撤销报名']
keyDeleteTeam = ['取消开团', '删除团队', '撤销团队', '撤销开团']
keyMacro = ['宏']
keyHelp = ['帮助', '指令', '查看指令', '指令清单']
keyAuthor = ['作者', '制作团队', '制作名单']
keyMedicament = ['小药', '药品', '食物']
keyFormation = ['阵眼', '阵法', '阵']
keyDaily = ['日常', '日常查询']
keyGold = ['金价']
keyServer = ['开服']
keyMethod = ['攻略', '条件', '前置']
keyFlower = ['花价']
keyExam = ['科举']
keyMedicine = ['小药']
keyBroadcast = ['通知']


def judge(message, qid, name, group):
    if message.strip()[:2].lower() != 'ns':  # 如果开头不是ns那么一切免谈，无事发生
        return

    ############## Main ###################
    command = message.strip()[2:].strip()  # 把ns去掉后面开始分割这个指令
    commandPart = command.split()  # 按照空格进行分割，但是后续要看看是不是加入更多的防傻判断
    servername = init.SERVER
    try:
        entrance = commandPart[0].strip()
    except:
        entrance = ''

    if entrance in keyNewTeam:
        try:  # 尝试解析参数，如果出错说明输入参数有误
            date = parseDate(commandPart[1].strip())
            time = parseTime(commandPart[2].strip())
            dungeon = commandPart[3].strip()
            comment = commandPart[4].strip()
            assert(date != -1)
            assert(time != -1)
        except:
            mirai.throwError(target=group, errCode=100)
            return

        try:  # 尝试解析是否指定了黑名单
            useBlackList = commandPart[5].strip()
        except:
            useBlackList = 0

        leader = sql.hasLeader(qid)
        if leader == -1:
            msg = '权限错误，请先申请成为团长'
        else:
            res = sql.createNewTeam(date, time, dungeon, comment, leader, useBlackList)
            if res == -1:
                msg = '数据库错误！请联系管理员'
            else:
                msg = '开团成功，{}，团队ID为{}, 集合时间{} {} {}'.format(dungeon, res, date, parseWeekday(date), time)

        mirai.sendGroupMessage(target=group, content=msg,messageType="TEXT", needAT=True, ATQQ=qid)

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
                msg += '{}. ID：{} {} {} {} {} {} \n'.format(str(i+1),
                                                            g['teamID'], g['leaderName'], g['dungeon'],
                                                            g['startTime'], parseWeekday(g['startTime']), g['comment'])
                msg += '------------------- \n'

        mirai.sendGroupMessage(target=group, content="在开团队已经通过临时会话发给您了~如果没收到请加机器人好友",messageType="TEXT", needAT=True, ATQQ=qid)
        mirai.sendTempMessage(target=group, QQ=qid,content=msg, messageType="TEXT")

    elif entrance in keyQuery:
        try:
            teamNumber = int(commandPart[1].strip())
            res = sql.getInfo(teamNumber)
        except:
            res = []
            teamNumber = None

        if teamNumber is None or not res:
            msg = '输入的团队ID不存在'
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")
        else:
            image = img.GetImg(teamNumber)
            if image == -1:
                msg = '此团队目前没有人报名'
                mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")
            else:
                mirai.sendGroupMessage(target=group, content=image, messageType="Image")

    elif entrance in keyEnroll:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())
        except:
            msg += '缺少团队ID '

        try:
            vocation = commandPart[2].strip()
            mental = sql.getMental(vocation)
            assert(mental != -1)  # 检查心法是否存在
        except:
            msg += '缺少角色心法或心法不存在 '

        try:
            memberName = commandPart[3].strip()
        except:
            msg += '缺少角色名称 '

        try:
            syana = int(commandPart[4].strip())
            assert(syana == 1 or syana == 0)
        except:
            syana = 0

        if msg == '':
            res = sql.addMember(teamNumber, qid, memberName, mental, syana)
            if res == 0:
                team = sql.getInfo(teamNumber)
                msg = '已成功报名 {} {}团长 {} {}-{}'.format(team['startTime'], team['leaderName'],team['dungeon'], vocation, memberName)
            elif res == -1:
                msg = '已经在此团队中'
            elif res == -3:
                msg = '团队不存在或已过期'
            else:
                msg = '数据库错误！请联系管理员'
        else:
            msg += '\n报团格式：ns报团 团队ID 心法 角色名\n双修心法请在报团命令最后额外加空格加1'

        mirai.sendGroupMessage(target=group, content=msg,messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyDisenroll:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())
        except:
            msg += '缺少团队ID'

        if msg == '':
            res = sql.delMember(teamNumber, qid)
            if res == 0:
                team = sql.getInfo(teamNumber)
                msg = '已成功取消报名 {} {}团长'.format(team['startTime'], team['leaderName'])
            elif res == -1:
                msg = '不在此团队中'
            elif res == -3:
                msg = '团队不存在或已过期'
            else:
                msg = '数据库错误！请联系管理员'

        mirai.sendGroupMessage(target=group, content=msg,messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyDeleteTeam:
        msg = ''

        try:
            teamNumber = int(commandPart[1].strip())
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
                    msg = '数据库错误！请联系管理员'

        mirai.sendGroupMessage(target=group, content=msg,messageType="TEXT", needAT=True, ATQQ=qid)

    elif entrance in keyMacro:
        msg = ''

        try:
            mental = sql.getMental(commandPart[1].strip())
            assert(mental != -1)  # 检查心法是否存在
        except:
            msg += '缺少心法名称或心法不存在'
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)
            return

        if msg == '':
            try:
                with open(init.MACRO_PATH+str(mental), 'r') as f:
                    lines = f.readlines()
                    msg = ''.join(lines)
            except:
                msg = '心法文件错误！请联系管理员'
                mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)
                return

        mirai.sendGroupMessage(target=group, content='宏命令已经通过临时会话私发给您了，如果没收到请加机器人好友',messageType="TEXT", needAT=True, ATQQ=qid)
        mirai.sendTempMessage(target=group, QQ=qid,content=msg, messageType="TEXT")

    elif entrance in keyHelp:
        msg = '在线用户手册： \nhttps://github.com/Hallows/nsRobot/blob/main/doc/userGuide.md'
        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyAuthor:
        msg = '致谢与授权说明： \nhttps://github.com/Hallows/nsRobot/blob/main/README.md'
        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyFormation:
        try:
            mentalName = str(commandPart[1].strip())
        except:
            msg = '通用阵眼：田螺(会会+无视防御)\n常用外功阵眼:\n凌雪(攻会会) 鲸鱼(破无会) 剑纯(会会无)\n常用内功阵眼:\n莫问(攻会无) 大师(攻破无) 气纯(会会无) \n花间(回蓝破防) 毒经(破会会)'
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")
            return
        mentalID = sql.getMental(mentalName=mentalName)
        if mentalID != -1:
            try:
                image = jx3api.getFormation(mentalID)
                mirai.sendGroupMessage(target=group, content=image, messageType="Image")
                return
            except:
                msg = '无法获得心法名称，请检查名称'
                mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyDaily:
        if len(commandPart) > 1:
            servername = str(commandPart[1].strip())
        msg = jx3api.getDaily(servername)
        if msg == 'error':
            mirai.sendGroupMessage(target=group, content='日常查询错误！请联系管理员', messageType="TEXT")
        else:
            mirai.sendGroupMessage(target=group, content=msg, messageType="Image")

    elif entrance in keyGold:
        if len(commandPart) > 1:
            servername = str(commandPart[1].strip())
        msg = jx3api.getGold(servername)
        if msg == 'error':
            mirai.sendGroupMessage(target=group, content='金价查询错误！请联系管理员', messageType="TEXT")
        else:
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyServer:
        if len(commandPart) > 1:
            servername = str(commandPart[1].strip())
        msg = jx3api.getServer(servername)
        if msg == 'error':
            mirai.sendGroupMessage(target=group, content='服务器状态查询错误！请联系管理员', messageType="TEXT")
        elif msg == 'UncertainServer':
            mirai.sendGroupMessage(target=group, content='请输入正确的区服名！', messageType="TEXT")
        else:
            mirai.sendGroupMessage(target=group, content=msg, messageType="Image")

    elif entrance in keyMethod:
        name = ''
        if len(commandPart) > 1:
            name = str(commandPart[1].strip())
        msg = jx3api.getMethod(name)
        if msg == 'error':
            mirai.sendGroupMessage(target=group, content='参数错误！或者联系管理员', messageType="TEXT")
        else:
            mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT")

    elif entrance in keyFlower:
        name = ''
        if len(commandPart) > 1:
            name = str(commandPart[1].strip())
        if len(commandPart) > 2:
            servername = str(commandPart[2].strip())
        msg = jx3api.getFlower(name, servername)
        if msg == 'error':
            mirai.sendGroupMessage(target=group, content='花价查询错误！请联系管理员', messageType="TEXT")
        else:
            mirai.sendGroupMessage(target=group, content=msg, messageType="Image")

    elif entrance in keyExam:
        subject = ''
        if len(commandPart) > 1:
            subject = str(commandPart[1].strip())
        msg = jx3api.getExam(subject)
        if msg == 'error':
            mirai.sendGroupMessage(target=group, content='科举查询错误！请联系管理员', messageType="TEXT")
        else:
            mirai.sendGroupMessage(target=group, content=msg, messageType="Image")
    
    elif entrance in keyMedicine:
        if len(commandPart) == 0:
            msg = jx3api.GetMedicine()
        else:
            msg = jx3api.GetMedicine(commandPart[1].strip())
        if msg == -1:
            mirai.sendGroupMessage(target=group,content = "小药查询错误，请检查心法名称",messageType="TEXT")
        else:
            mirai.sendGroupMessage(target = group,content = msg,messageType="Image")
    
    elif entrance in keyBroadcast:
        try:
            teamID=commandPart[1].strip()
            broadMsg=commandPart[2].strip()
        except:
            mirai.throwError(target=group, errCode=100)
            return
        teamInfo=sql.getInfo(teamID=teamID)
        if teamInfo==[]:
            mirai.sendGroupMessage(target=group,content = "输入的团队ID不存在",messageType="TEXT")
            return
        leader=sql.hasLeader(qid)
        if leader==-1:
            mirai.sendGroupMessage(target=group,content = "你还不是团长，请联系管理员",messageType="TEXT",needAT=True, ATQQ=qid)

        teamInfo=sql.getMember(teamID=teamID)
        if teamInfo==[]:
            mirai.sendGroupMessage(target=group,content = "此团队暂时无人报名",messageType="TEXT")
            return
        mirai.sendGroupMessage(target=group,content = "信息开始私聊给指定团队，根据人数机器人可能无响应数分钟",messageType="TEXT")
        for key in teamInfo:
            QQ=key['QQNumber']
            print('sending to {}'.format(QQ))
            mirai.sendTempMessage(target=group,QQ=QQ,content=broadMsg,messageType="TEXT")
            Lib_Time.sleep(5)
        return

    else:
        msg = '未知指令，请通过 ns帮助 进行查看'
        mirai.sendGroupMessage(target=group, content=msg, messageType="TEXT", needAT=True, ATQQ=qid)
