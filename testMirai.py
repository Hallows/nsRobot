import requests
import json
import sys
import time

#获取版本
res = requests.get('http://0.0.0.0:8080/about')
jsonData = res.json()
if jsonData['data']['version']:
    print('Connect success, got API version={}'.format(jsonData['data']['version']))
else:
    raise SystemExit('ERROR: Connect failed, programme exit')

#鉴权
requestData = {'authKey': 'INITKEYW56fGXcy'}
res = requests.post('http://0.0.0.0:8080/auth',json=requestData)
jsonData = res.json()
if jsonData['code'] == 0:
    print('Authorize Success! Got AuthCode {}'.format(jsonData['session']))
    sessonKey=jsonData['session']
else:
    raise SystemExit('ERROR: Authorize Failed with code {} and the authKey is {}'.format(jsonData['code'], requestData['authKey']))

#校验sesson并绑定bot
requestData = {
    'sessionKey': sessonKey,
    'qq': 2274927840
    }
res = requests.post('http://0.0.0.0:8080/verify', json=requestData)
jsonData = res.json()
if jsonData['code'] == 0:
    print('Verify Success!')
else:
    raise SystemExit('ERROR: Verify Failed!')

#发送一条消息
time.sleep(2)
requestData = {
    'sessionKey': sessonKey,
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

#等待回复
time.sleep(10)

#获取接收
res = requests.get('http://0.0.0.0:8080/fetchLatestMessage', params= {'sessionKey': sessonKey, 'count': 1})
print(jsonData['data'][0]['messageChain'][1]['text'])


#释放sesson
requestData = {
    'sessionKey': sessonKey,
    'qq': 2274927840
    }
res = requests.post('http://0.0.0.0:8080/release', json=requestData)
jsonData = res.json()
if jsonData['code'] == 0:
    print('Release Success!')
else:
    raise SystemExit('ERROR: Release Failed!')
