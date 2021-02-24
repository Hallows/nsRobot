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


def getDaily(server=init.SERVER):
    data = {"server": server, "token": "153166341"}
    r = requests.post(url + 'daily', data)
    r_data = json.loads(r.text)
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
    name = time.strftime("%y-%m-%d-%H-%M-%S-daily.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


def getGold(server=init.SERVER):
    data = {"server": server, "token": "153166341"}
    r = requests.post(url + 'gold', data)
    r_data = json.loads(r.text)

    if r_data['code'] == 0:
        return ''

    offical = float(r_data['data']['wanbaolou']).__int__()
    platform_max = 0
    platform_min = 1000

    for key, value in r_data['data'].items():
        if key == 'server' or key == 'wanbaolou':
            continue
        else:
            if float(value).__int__() > platform_max:
                platform_max = float(value).__int__()
            if float(value).__int__() < float(platform_min).__int__():
                platform_min = float(value).__int__()

    content = server + "当前金价为：\n" + "万宝楼：" + (offical - 3).__str__() + '-'+(
        offical + 3).__str__() + '\n' + "平台：" + platform_min.__str__() + '-' + platform_max.__str__() + '\n'

    w, h = 300, 100

    img = Image.new("RGB", (w + 20, h + 20), 0xffffff)
    drawer = ImageDraw.Draw(img)
    drawer.text((10, 10), content, 0x000000, font)
    name = time.strftime("%y-%m-%d-%H-%M-%S-gold.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


def getServer(server=init.SERVER):
    data = {"server": server, "token": "153166341"}
    r = requests.post(url + 'server', data)
    r_data = json.loads(r.text)

    if r_data['code'] == 0:
        return

    content = "服务器：" + server + '\n' + '状    态：\n'

    if r_data['data']['status'] == 1:
        img = Image.new("RGB", (300, 100), 0xd9ffe2)
    else:
        img = Image.new("RGB", (300, 100), 0xeaeaea)

    drawer = ImageDraw.Draw(img)

    drawer.text((10, 17), content, 0x000000, font)

    if r_data['data']['status'] == 1:
        drawer.text((130, 49), "正     常", 0x009342, font)
    else:
        if time.localtime().tm_hour >= 12:
            drawer.text((130, 49), "已倒闭", 0x0000ff, font)
        else:
            drawer.text((130, 49), "维护中", 0x727272, font)

    name = time.strftime("%y-%m-%d-%H-%M-%S-server.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


def getSand(server=init.SERVER):
    data = {"server": server, "token": "153166341"}
    r = requests.post(url + 'sand', data)
    r_data = json.loads(r.text)
    img_url = r_data['data']['url']
    img = requests.get(img_url).content

    name = time.strftime("%y-%m-%d-%H-%M-%S-sand.jpg", time.localtime())
    with open(init.IMAGE_PATH + name, 'wb') as i:
        i.write(img)
    return name


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
