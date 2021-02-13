import requests
import json
import sys

#获取mirai版本
#输入-miraiURL: mirai的HTTPAPI地址
def getVersion(miraiURL):
    url=miraiURL+'/about'
    res = requests.get(url=url)
    jsonData = res.json()
    if jsonData['data']['version']:
        print('Connect success, got API version={}'.format(jsonData['data']['version']))
    else:
        raise SystemExit('ERROR: Connect failed, programme exit')

#获取授权码
#输入-miraiURL: mirai的HTTPAPI地址
#输入-miraiKey: mirai的默认连接key，从配置文件中获取
#输出-sessionKey: 返回的有效的session
def getAuth(miraiURL, miraiKey):
    url=miraiURL+'/auth'
    requestData = {'authKey': miraiKey}
    res = requests.post(url=url,json=requestData)
    jsonData = res.json()
    if jsonData['code'] == 0:
        print('Authorize Success! Got AuthCode {}'.format(jsonData['session']))
        sessionKey = jsonData['session']
        return sessionKey
    else:
        raise SystemExit('ERROR: Authorize Failed with code {} and the authKey is {}'.format(jsonData['code'], requestData['authKey']))

#校验sesson并绑定bot
#输入-miraiURL: mirai的HTTPAPI地址
#输入-session: 有效的session，通过getAuth()获取
#输入-botNumber: 待绑定的机器人的QQ号
def verify(miraiURL,session,botNumber):
    requestData = {
        'sessionKey': session,
        'qq': botNumber
        }
    url=miraiURL+'/verify'
    res = requests.post(url=url, json=requestData)
    jsonData = res.json()
    if jsonData['code'] == 0:
        print('Verify Success!')
    else:
        raise SystemExit('ERROR: Verify Failed!')


#释放sesson并清除bot的信息缓存(程序结束前调用否则可能导致溢出)
#输入-miraiURL: mirai的HTTPAPI地址
#输入-session: 有效的session，通过getAuth()获取
#输入-botNumber: 待绑定的机器人的QQ号
def release(miraiURL,session,botNumber):
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
#输入-miraiURL: mirai的HTTPAPI地址
#输入-session: 待开启WS服务的有效session，通过getAuth()获取
def startWebSocket(miraiURL, session):
    requestData = {
        'sessionKey': session,
        "enableWebsocket": True
        }
    url=miraiURL+'/config'
    requests.post(url=url, json=requestData)
    print('WebSocketStarted!')

#对指定群聊发送信息
#输入-miraiURL: mirai的HTTPAPI地址
#输入-session: 待开启WS服务的有效session，通过getAuth()获取
#输入-target：目标群聊的群号
#输入-content：若需要发送文字则为文字内容，若需要发送图片为图片URL
#输入-messageTye：默认为TEXT即文字，也可接受Image即图片
#输入-needAT：是否需要在发送内容前at指定人，默认为0即不at
#输入-ATQQ：如果需要at，传入uint型的QQ号，注意！不是字符串！
def sendGroupMessage(miraiURL, session, target,  content:str,messageType="TEXT", needAT=0, ATQQ=0):
    chain=[]
    if (needAT == 1):
        temp={"type": "At", "target": ATQQ, "display": "@来源"}
        chain.append(temp)
    if (messageType == "TEXT"):
        temp = {"type": "Plain", "text": content}
        chain.append(temp)
    elif (messageType == "image"):
        temp = {"type": "Image", "url": content}
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

#------IMPORTANT-------
#此函数用于抛出错误提示，鉴于错误意料外的错误列表可能会很长，此函数恒放置于此文件最后！
#错误码-含义
#100-参数错误
def throwError(miraiURL, session, target,errCode):
    chain = []
    if errCode == 100:
        temp = {"type": "Plain", "text": "指令参数错误，请使用 ns帮助 查看所有指令列表"}
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
