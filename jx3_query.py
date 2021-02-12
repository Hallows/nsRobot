import requests
import json
import init
import time

url = "https://jx3api.com/api/"


def getDaily():
    data = {"server": "天鹅坪", "token": "153166341"}
    r = requests.post(url + 'daily', data)
    r_data = json.loads(r.text)
    return r_data


def getGold():
    data = {"server": "天鹅坪", "token": "153166341"}
    r = requests.post(url + 'gold', data)
    r_data = json.loads(r.text)
    return r_data['data']


def getServer(server='天鹅坪'):
    data = {"server": server, "token": "153166341"}
    r = requests.post(url + 'server', data)
    r_data = json.loads(r.text)
    return r_data['data']


def getSand():
    data = {"server": "天鹅坪", "token": "153166341"}
    r = requests.post(url + 'sand', data)
    r_data = json.loads(r.text)
    img_url = r_data['data']['url']
    img = requests.get(img_url).content

    Time = time.strftime("%y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    with open(init.IMAGE_PATH + Time + '.jpg', 'wb') as i:
        i.write(img)
    return {'path': init.IMAGE_PATH + Time + '.jpg'}


def getFlower(name: str):
    data = {"server": "天鹅坪",
            "flower": name,
            "token": "153166341"}
    r = requests.post(url + 'flower', data)
    r_data = json.loads(r.text)
    return r_data['data']


def getExam(subject: str):
    data = {
        "question":  subject,
        "token": "153166341"
    }
    r = requests.post(url + 'exam', data)
    r_data = json.loads(r.text)
    if r_data['code'] == 0:
        return ''
    return r_data['data']
