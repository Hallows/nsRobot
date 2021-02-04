import MiraiConnnect as mirai
import time
import requests

miraiURL = 'http://0.0.0.0:8080'
miraiKey = 'NSROBOTdevmode'
miraiQQ = 2274927840

#获取版本
mirai.getVersion(miraiURL=miraiURL)
#获取session
session=mirai.getAuth(miraiURL=miraiURL,miraiKey=miraiKey)
#校验sesson并绑定bot
mirai.verify(miraiURL=miraiURL,session=session,botNumber=miraiQQ)

#发送一条消息
time.sleep(2)
requestData = {
    'sessionKey': session,
    "target": 773553072,
    "messageChain": [
        { "type": "Plain", "text": "hello\n" },
        { "type": "Plain", "text": "world" }
        ]
    }
res = requests.post('http://0.0.0.0:8080/sendGroupMessage', json=requestData)
jsonData = res.json()
if jsonData['code'] == 0:
    print('Sent')
else:
    print('Send failed')

#释放sesson
mirai.release(miraiURL=miraiURL,session=session,botNumber=miraiQQ)