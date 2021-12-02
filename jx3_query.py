# coding=utf-8

import requests
import json
import init
import time
import sqlConnect
import generate_image as genimg
from PIL import Image, ImageDraw, ImageFont

url = "https://www.jx3api.com/app/"

font = ImageFont.truetype(init.FONT_PATH + 'msyh.ttc', 30, index=0)
week = {0: "星期一", 1: "星期二", 2: "星期三",
        3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"}


# 日常查询接口
def getDaily(server):
    data = {"server": server}
    r = requests.post(url + 'daily', data)
    r_data = json.loads(r.text)
    print(r_data)
    if r_data['msg'] != 'success':
        return 'error'

    curtime = time.localtime()
    content = "今日是公元%d年第%d天，%d月%d日，%s\n" % (
        curtime.tm_year, curtime.tm_yday, curtime.tm_mon, curtime.tm_mday, week[curtime.tm_wday])

    w, h = 0, 0

    title = {'dayWar': '秘境大战', 'dayBattle': '今日战场', 'dayPublic': '驰援任务', 'dayDraw': '美人画像', 'weekPublic': '武林通鉴·公共任务', 'weekFive': '武林通鉴·秘境任务', 'weekTeam': '武林通鉴·团队秘境','dayCamp':"阵营日常"}
    for key, value in r_data['data'].items():
        if key == "date" or key == "week":
            continue
        else:
            content += title[key]
            content += ':'
            temp = value.replace(';', '、')
            content += temp
            content += '\n'

            w_temp, h_temp = font.getsize(title[key] + ':' + temp)
            if w_temp > w:
                w = w_temp
            h += int(h_temp * 1.3)

    img = Image.new("RGB", (w + 20, h + 20), 0xffffff)
    drawer = ImageDraw.Draw(img)
    drawer.text((10, 10), content, 0x000000, font)
    name = time.strftime("%y-%m-%d-%H-%M-%S-daily.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


# 金价查询接口
def getGold(server):
    data = {"server": server}
    r = requests.post(url + 'demon', data)
    r_data = json.loads(r.text)
    message = ''
    if r_data['msg'] != 'success':
        return 'error'
    gold = r_data['data']
    message += '金价·'+server+'\n'
    message += '万  宝 楼：1元 = '+gold['wanbaolou']+'金\n'
    goldsum = 0
    n = 0
    for key, value in gold.items():
        if key == 'server' or key == 'wanbaolou' or value == 'None' or key == 'time':
            continue
        else:
            goldsum += float(value)
            n = n + 1
    message += '平台均价：1元 = ' + str(round(goldsum/n, 2)) + '金'
    return message

    # 生成图片方式
    # offical = float(r_data['data']['wanbaolou']).__int__()
    # platform_max = 0
    # platform_min = 1000
    #
    # for key, value in r_data['data'].items():
    #     if key == 'server' or key == 'wanbaolou':
    #         continue
    #     else:
    #         if float(value).__int__() > platform_max:
    #             platform_max = float(value).__int__()
    #         if float(value).__int__() < float(platform_min).__int__():
    #             platform_min = float(value).__int__()
    #
    # content = server + "当前金价为：\n" + "万宝楼：" + (offical - 3).__str__() + '-'+(
    #     offical + 3).__str__() + '\n' + "平台：" + platform_min.__str__() + '-' + platform_max.__str__() + '\n'
    #
    # w, h = 300, 100
    #
    # img = Image.new("RGB", (w + 20, h + 20), 0xffffff)
    # drawer = ImageDraw.Draw(img)
    # drawer.text((10, 10), content, 0x000000, font)
    # name = time.strftime("%y-%m-%d-%H-%M-%S-gold.jpg", time.localtime())
    # img.save(init.IMAGE_PATH + name)

    # return name


# 开服查询接口
def getServer(server):
    data = {"server": server}
    r = requests.post(url + 'check', data)
    r_data = json.loads(r.text)

    if r_data['msg'] != 'success':
        return 'error'
    if isinstance(r_data['data'], list):
        return 'UncertainServer'
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


# 奇遇前置查询接口
def getMethod(name):
    data = {"name": name}
    r = requests.post(url + 'require', data)
    r_data = json.loads(r.text)
    message = ''
    if r_data['msg'] != 'success':
        message = 'error'
        return message

    method = r_data['data']
    message += name + '·前置条件\n'
    message += '触发方法：' + method['means'] + '\n'
    message += '满足条件：' + method['require'] + '\n'
    message += '其他可能：' + method['maybe'] + '\n'
    message += '物品奖励：' + method['reward']
    return message


def getSandTable(server=init.SERVER):
    data = {"server": server, "token": "153166341"}
    r = requests.post(url + 'sand', data)
    r_data = json.loads(r.text)

    if r_data['code'] != 1:
        return ''

    img_url = r_data['data']['url']
    img = requests.get(img_url).content

    name = time.strftime("%y-%m-%d-%H-%M-%S-sand.jpg", time.localtime())
    with open(init.IMAGE_PATH + name, 'wb') as i:
        i.write(img)
    return name


def getFlower(name: str, server: str):
    data = {"server": server,
            "flower": name}
    r = requests.post(url + 'flower', data)
    r_data = json.loads(r.text)
    if r_data['msg'] != 'success':
        message = 'error'
        return message

    i = 0
    w, h = 500, 1000

    content = init.SERVER + " · " + name + "\n广陵邑：\n"
    i += 2
    for item in r_data['data']['广陵邑']:
        i += 3
        content += '  ' + item['name']
        if 'color' in item.keys():
            content += '(' + item['color'] + ')'
        content += '：\n    '
        for line in item['line']:
            content += line + ' '
        content += '线\n     '
        content += item['price'].__str__() + '倍\n'

    content += "枫叶泊·天苑：\n"
    i += 1
    for item in r_data['data']['枫叶泊·天苑']:
        i += 3
        content += '  ' + item['name'] + '(' + item['color'] + ')：\n    '
        for line in item['line']:
            content += line + ' '
        content += '线\n     '
        content += item['price'].__str__() + '倍\n'

    content += "枫叶泊·乐苑：\n"
    i += 1
    for item in r_data['data']['枫叶泊·乐苑']:
        i += 3
        content += '  ' + item['name'] + '(' + item['color'] + ')：\n    '
        for line in item['line']:
            content += line + ' '
        content += '线\n     '
        content += item['price'].__str__() + '倍\n'

    img = Image.new("RGB", (w, 37*i), 0xffffff)
    drawer = ImageDraw.Draw(img)
    drawer.text((10, 10), content, 0x000000, font)

    name = time.strftime("%y-%m-%d-%H-%M-%S-flower.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


def getExam(subject: str):
    data = {"question":  subject}
    r = requests.post(url + 'exam', data)
    r_data = json.loads(r.text)
    if r_data['code'] != 200:
        return 'error'

    w, h = 0, 0
    i = 0
    content = ''

    for question in r_data['data']:
        content += question['question'] + '\n' + \
            '  ' + question['answer'] + '\n\n'
        if max(font.getsize(question['question'])[0], font.getsize('  ' + question['answer'])[0]) > w:
            w = max(font.getsize(question['question'])[0], font.getsize(
                '  ' + question['answer'])[0])

        i += 3

    h = i * 37

    img = Image.new("RGB", (w + 20, h), 0xffffff)
    drawer = ImageDraw.Draw(img)
    drawer.text((10, 10), content, 0x000000, font)

    name = time.strftime("%y-%m-%d-%H-%M-%S-exam.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


def getFormation(mentalID: int):

    formation = sqlConnect.getFormation(mentalID)

    w, h = 0, 0
    i = 0

    content = formation['formationName'] + '\n'
    i += 1

    for key, value in formation.items():
        if key == "mentalID" or key == "formationName":
            continue
        content += value + '\n'
        if font.getsize(value + '\n')[0] > w:
            w = font.getsize(value + '\n')[0]

        i += 1

    content += "七重归一：无\n"
    i += 1

    h = i * 37

    img = Image.new("RGB", (w+20, h + 20), 0xffffff)
    drawer = ImageDraw.Draw(img)
    drawer.text((10, 10), content, 0x000000, font)

    name = time.strftime("%y-%m-%d-%H-%M-%S-eye.jpg", time.localtime())
    img.save(init.IMAGE_PATH + name)

    return name


def GetMedicine(mentalname: str = None):
    if mentalname:
        mentalid = sqlConnect.getMental(mentalname)
        if mentalid == -1:
            return -1
        mentalname = sqlConnect.getMental(mentalname,1)
        medicines = sqlConnect.getMedicine(mentalID =mentalid)
        mentalinfo = sqlConnect.getMentalInfo(mentalid)
        tital = "当前版本下" + mentalname + "的可用小药为："
        content = []
        for medicine in medicines:
            content.append(medicine['class'] + ":" + medicine['name'] +  '  ' + medicine["gainType"] + "提高" + medicine['value'] +"点" )
        content.append("此列表仅为推荐，请根据自身属性选择合适小药")
        name = time.strftime("%y-%m-%d-%H-%M-%S-medicine.jpg", time.localtime())
        genimg.getImgFromText(tital=tital, content=content, font="STXINWEI.TTF", size=30,
                              titalColor='000000', contentColor='13244f', backColor='b2cdf6', path=init.IMAGE_PATH + name,lineEdit=1.05)
    else:
        medicines = sqlConnect.getMedicine()
        content = []
        tital = "小药"
        for medicine in medicines:
            content.append(medicine['class'] + ":" + medicine['name'] +
                           '  ' + medicine["gainType"] + "提高" + medicine['value'] + "点")
        name = time.strftime("%y-%m-%d-%H-%M-%S-medicine.jpg", time.localtime())
        genimg.getImgFromText(tital=tital, content=content, font="STXINWEI.TTF", size=30, titalColor='000000',
                              contentColor='13244f', backColor='b2cdf6', path=init.IMAGE_PATH + name, lineEdit=1.05)
    return name
    
    
def getRandom():
    r = requests.post(url + 'random')
    r_data = json.loads(r.text)
    message = ''
    if r_data['msg'] != 'success':
        message = 'error'
        return message

    method = r_data['data']
    message += method['text']
    
    return message
