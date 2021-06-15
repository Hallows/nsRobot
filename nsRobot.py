import MiraiConnnect as mirai
import serverAction as action
import json
import time
import requests
import websocket
import pymysql
import sqlConnect as sql 
try:
    import thread
except ImportError:
    import _thread as thread
try:
    import init
except ImportError:
    print("can not find init file")


miraiURL =init.miraiURL
miraiKey = init.miraiKey
miraiQQ = init.miraiQQ
session = 'newsession'
lastSQLReCon = None

def initMirai():
    mirai.setMiraiURL(miraiURL)
    #获取版本
    mirai.getVersion()
    #获取session
    global session
    session=mirai.verify(miraiKey=miraiKey)
    #校验sesson并绑定bot
    mirai.bind(botNumber=miraiQQ)
    #开启webSocket
    mirai.startWebSocket()
    #释放sesson
    #mirai.release(miraiURL=miraiURL,session=session,botNumber=miraiQQ)

def on_message(ws, message):
    incomeJson = json.loads(message)
    if incomeJson['data']['type'] == 'GroupMessage':
        if incomeJson['data']['messageChain'][1]['type'] == 'Plain':
            incomeQQ = incomeJson['data']['sender']['id']
            incomeMemberName = incomeJson['data']['sender']['memberName']
            incomeGroupChatID=incomeJson['data']['sender']['group']['id']
            incomeMessage = incomeJson['data']['messageChain'][1]['text']
            temp='Get income message from GroupChat {} named {}(QQ:{}) with text: {}'.format(incomeGroupChatID,incomeMemberName,incomeQQ,incomeMessage)
            print(temp)
            action.judge(message=incomeMessage, qid=incomeQQ, name=incomeMemberName, group=incomeGroupChatID)
            #mirai.sendGroupMessage(miraiURL,session,target=incomeGroupChatID,content="got your message!",messageType="TEXT",needAT=1,ATQQ=incomeQQ)
        # else:
        #     sql.SQLReConnect()
    if incomeJson['data']['type'] == 'NewFriendRequestEvent':
        eventID = incomeJson['data']['eventId']
        fromId = incomeJson['data']['fromId']
        groupId = incomeJson['data']['groupId']
        nickName = incomeJson['data']['nick']
        incomeMessage = incomeJson['data']['message']
        mirai.acceptNewFriend(eventID=eventID,fromId=fromId,groupId=groupId,message="你好，朋友",name=nickName)
        

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print('nsRobot Running!')
        time.sleep(1)
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    initMirai()
    wsURL = "ws://{}/all?verifyKey={}&sessionKey={}&qq={}".format(init.miraiURL[7:],miraiKey,mirai.session,miraiQQ)
    print(wsURL)
    sql.SQLConnect()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url=wsURL,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

