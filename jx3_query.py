# coding=utf-8

import requests
import json
import init
import time
from PIL import Image, ImageDraw, ImageFont

url = "https://jx3api.com/api/"

font = ImageFont.truetype(init.FONT_PATH + 'hwxk.ttf', 30)
week = {0: "星期一", 1: "星期二", 2: "星期三",
        3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"}


def getDaily():
    data = {"server": "天鹅坪", "token": "153166341"}
    r = requests.post(url + 'daily', data)
    r_data = json.loads(r.text)

    # if r_data['code'] == 0:
    #     return ''

    curtime = time.localtime()

    content = "今日是公元%d年第%d天，%d月%d日，%s\n" % (
        curtime.tm_year, curtime.tm_yday, curtime.tm_mon, curtime.tm_mday, week[curtime.tm_wday])

    w, h = 0, 0

    for key, value in r_data.items():
        if key == "时间" or key == "星期":
            continue
        else:
            content += key
            content += ':'
            temp = value.replace(';', '、')
            content += temp
            content += '\n'

            w_temp, h_temp = font.getsize(key + ':' + temp)
            if w_temp > w:
                w = w_temp
            h += int(h_temp * 1.3)

    img = Image.new("RGB", (w + 20, h + 20), 0xffffff)

    drawer = ImageDraw.Draw(img)

    drawer.text((10, 10), content, 0x000000, font)

    img.save('1.jpg')

    print(content)

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


def getEye(mental: str):
    data = {
        "name": mental,
        "token": "153166341"
    }

    r = requests.post(url + 'eye', data)
    r_data = json.loads(r.text)
    if r_data['code'] == 0:
        return ''
    print(r_data)
    return r_data
