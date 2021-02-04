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