import requests
import json
import sys
import init

miraiURL = None
session = None

#设置miraiURL
def setMiraiURL(url):
    global miraiURL
    miraiURL = url
    return

#获取mirai版本
#输入-miraiURL: mirai的HTTPAPI地址
def getVersion():
    global miraiURL
    url=miraiURL+'/about'
    res = requests.get(url=url)
    jsonData = res.json()
    if jsonData['data']['version']:
        print('Connect success, got API version={}'.format(jsonData['data']['version']))
    else:
        raise SystemExit('ERROR: Connect failed, programme exit')

#获取授权码
#输入-miraiKey: mirai的默认连接key，从配置文件中获取
#输出-session获取成功返回0
def verify(miraiKey):
    global miraiURL
    global session
    url=miraiURL+'/verify'
    requestData = {'verifyKey': miraiKey}
    res = requests.post(url=url,json=requestData)
    jsonData = res.json()
    if jsonData['code'] == 0:
        print('Verify Success! Got session {}'.format(jsonData['session']))
        session = jsonData['session']
        return 0
    else:
        raise SystemExit('ERROR: Verify Failed with code {} and the session is {}'.format(jsonData['code'], requestData['authKey']))

#校验sesson并绑定bot
#输入-botNumber: 待绑定的机器人的QQ号
def bind(botNumber):
    global miraiURL
    global session
    requestData = {
        'sessionKey': session,
        'qq': botNumber
        }
    url=miraiURL+'/bind'
    res = requests.post(url=url, json=requestData)
    jsonData = res.json()
    if jsonData['code'] == 0:
        print('Verify Success!')
    else:
        raise SystemExit('ERROR: Verify Failed!')


#释放sesson并清除bot的信息缓存(程序结束前调用否则可能导致溢出)
#输入-botNumber: 待绑定的机器人的QQ号
def release(botNumber):
    global miraiURL
    global session
    requestData = {
        'sessionKey': session,
        'qq': botNumber
        }
    url=miraiURL+'/release'
    res = requests.post(url=url, json=requestData)
    jsonData = res.json()
    if jsonData['code'] == 0:
        print('Release Success!')
    else:
        raise SystemExit('ERROR: Release Failed!')

#设置指定的session所对应的对话开启webSocket代理服务（默认全局关闭）
def startWebSocket():
    global miraiURL
    global session
    requestData = {
        'sessionKey': session,
        "enableWebsocket": True
        }
    url=miraiURL+'/config'
    requests.post(url=url, json=requestData)
    print('WebSocketStarted!')
 
def acceptNewFriend(eventID, fromId, groupId, message,name):
    global miraiURL
    global session
    requestData = {
        'sessionKey': session,
        'eventId': int(eventID),
        'fromId': int(fromId),
        'groupId': int(groupId),
        'operate': 0,
        "message": message
        }
    url = miraiURL + '/resp/newFriendRequestEvent'
    res = requests.post(url=url, json=requestData)
    jsonData = res.json()
    if jsonData['code'] != 0:
        print("get error {} when send message".format(jsonData['code']))
    else:
        print("got new friend request from {} with QQ:{}".format(fromId,name))

#对指定群聊发送信息
#输入-target：目标群聊的群号
#输入-content：若需要发送文字则为文字内容，若需要发送图片为图片的本地位置
#输入-messageTye：默认为TEXT即文字，也可接受Image即图片
#输入-needAT：是否需要在发送内容前at指定人，默认为0即不at
#输入-ATQQ：如果需要at，传入uint型的QQ号，注意！不是字符串！
def sendGroupMessage(target, content: str, messageType="TEXT", needAT=False, ATQQ=None):
    global miraiURL
    global session
    chain=[]
    if needAT:
        temp={"type": "At", "target": ATQQ, "display": "@来源"}
        chain.append(temp)
        temp = {"type": "Plain", "text": " "}
        chain.append(temp)
    if messageType == "TEXT":
        temp = {"type": "Plain", "text": content}
        chain.append(temp)
    elif messageType == "Image":
        imagePath=getImgPath(content)
        temp = {"type": "Image", "path": imagePath}
        chain.append(temp)
    requestData = {
    "sessionKey": session,
    "target": target,
    "messageChain": chain
    }
    url=miraiURL+'/sendGroupMessage'
    res = requests.post(url=url, json=requestData)

    try:
        jsonData = res.json()
        if jsonData['code'] != 0: 
            print("get error {} when send message".format(jsonData['code']))
    except:
        print("Connect error,got{}").format(res.text)


def getImgPath(content:str):
    imagePath=init.IMAGE_PATH+content
    print(imagePath)
    return imagePath

#对指定群聊中的指定人发送临时消息
#输入-target：用于发起临时对话的群聊的群号
#输入-QQ：发送临时对话对象的QQ号
#输入-content：若需要发送文字则为文字内容，若需要发送图片为图片的本地位置
#输入-messageTye：默认为TEXT即文字，也可接受Image即图片
def sendTempMessage(target, QQ, content: str, messageType="TEXT"):
    global miraiURL
    global session
    chain = []
    if messageType == "TEXT":
        temp = {"type": "Plain", "text": content}
        chain.append(temp)
    elif messageType == "Image":
        imagePath=getImgPath(content)
        temp = {"type": "Image", "path": imagePath}
        chain.append(temp)
    requestData = {
    "sessionKey": session,
    "qq":QQ,
    "group": target,
    "messageChain": chain
    }
    url = miraiURL + '/sendTempMessage'
    res = requests.post(url=url, json=requestData)
    
    try:
        jsonData = res.json()
        if jsonData['code'] != 0:
            print("get error code {} when send Temp message".format(jsonData['code']))
    except:
        print("Connect error,got{}").format(res.text)




#------IMPORTANT-------
#此函数用于抛出错误提示，鉴于错误意料外的错误列表可能会很长，此函数恒放置于此文件最后！
#错误码-含义
#100-参数错误
#400-权限错误
#500-内部错误
def throwError(target, errCode):
    global miraiURL
    global session
    chain = []
    if errCode == 100:
        temp = {"type": "Plain", "text": "指令参数错误，请使用 ns帮助 查看所有指令列表"}
        chain.append(temp)
    if errCode == 400:
        temp = {"type": "Plain", "text": "权限错误，请联系管理员确认您是否有对应操作的权限"}
        chain.append(temp)
    if errCode == 500:
        temp = {"type": "Plain", "text": "出现了一个内部错误！请联系管理员反馈！"}
        chain.append(temp)
    requestData = {
    "sessionKey": session,
    "target": target,
    "messageChain": chain
    }
    url=miraiURL+'/sendGroupMessage'
    res = requests.post(url=url, json=requestData)
    jsonData = res.json()
    if jsonData['code'] != 0:
        print("get error when send message")
