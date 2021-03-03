from PIL import Image, ImageDraw, ImageFont
import pymysql
from math import ceil
import time
from datetime import datetime
import init
import sqlConnect

boxLength = 200
boxHeight = 50

startX = 100
startY = 116

font = ImageFont.truetype(init.FONT_PATH + 'msyh.ttc', 20, index=1)


def GetDate(dateRaw: str):

    date = time.strptime(dateRaw, "%Y-%m-%d %H:%M")
    week = {0: "周一", 1: "周二", 2: "周三",
            3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    dateStr = week[date.tm_wday] + ' '
    dateStr += time.strftime("%m月%d日 %H:%M", date)
    return dateStr


def DrawRectangal(img: Image.Image, x: int, y: int, member: dict):

    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        (startX + x*boxLength,
         startY + (boxHeight / 2) + y * boxHeight,
         startX + (x+1)*boxLength,
         startY + (boxHeight / 2) + (y+1) * boxHeight),
        fill=GetRGB(member['mentalColor']),
        outline=(0, 0, 0),
        width=1
    )

    if len(member['nickName']) > 6:
        name = member['nickName'][0:6]
    else:
        name = member['nickName']

    drawer.text((startX + (0.3+x)*boxLength,
                 startY + (boxHeight / 2) + (y + 0.25) * boxHeight), name, font=font, fill=0x000000)

    r = boxLength / 10

    drawer.ellipse((startX + x*boxLength + (boxLength * 0.05),
                    startY + (boxHeight / 2) + y *
                    boxHeight + (boxHeight / 2 - r),
                    startX + x*boxLength + (boxLength * 0.05) + 2*r,
                    startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 + r)), fill=0x000000, outline=None)

    logo = Image.open(init.MENTAL_ICON_PATH + member['mainMentalIcon'])
    logo = logo.resize((int(r * 1.8), int(r * 1.8)), Image.ANTIALIAS)
    R, G, B, A = logo.split()
    img.paste(logo, (int(startX + x*boxLength + (boxLength * (0.25) - 1.9 * r)),
                     int(startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 - 0.9*r))), mask=A)
    if member['syana'] == 1:
        drawer.ellipse((startX + x*boxLength + (boxLength * 0.25) - r,
                        startY + (boxHeight / 2) + y*boxHeight +
                        (boxHeight / 2),
                        startX + x*boxLength + (boxLength * 0.05) + 2*r,
                        startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 + r)), fill=0x000000, outline=0xffffff, width=1)
        logo = Image.open(init.MENTAL_ICON_PATH + member['secMentalIcon'])
        logo = logo.resize((int(r * 0.9), int(r * 0.9)), Image.ANTIALIAS)
        R, G, B, A = logo.split()
        img.paste(logo, (int(startX + x*boxLength + (boxLength * (0.25) - 0.9 * r)),
                         int(startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 + 0.1*r))), mask=A)


def GetRGB(id: str) -> tuple:
    r = int(id[0:2], 16)
    g = int(id[2:4], 16)
    b = int(id[4:6], 16)
    return (r, g, b)


def GetImg(id: int):
    # 根据团队id生成图片，返回文件名

    teaminfo = sqlConnect.getInfo(id, needYear=1)

    if teaminfo == {}:
        return -1

    memberlist = sqlConnect.getMember(id)

    canvasLength = 1200
    canvasHeight = 480

    internal = []
    external = []
    healer = []
    tank = []

    for member in memberlist:

        if member['mentalWorks'] == 1:
            tank.append(member)
        elif member['mentalWorks'] == 2:
            healer.append(member)
        elif member['mentalWorks'] == 3:
            internal.append(member)
        elif member['mentalWorks'] == 4:
            external.append(member)
        else:
            return -2

    if len(internal) > 10 or len(external) > 10 or len(tank) + len(healer) > 5:
        num = max(ceil(len(internal) / 2),
                  ceil(len(external) / 2),
                  len(tank) + len(healer))

        canvasHeight += (num - 5) * boxHeight

    img = Image.new("RGB", (canvasLength, canvasHeight), (255, 255, 255))

    drawer = ImageDraw.Draw(img)

    tital = teaminfo['leaderName'] + ' ' + teaminfo['dungeon']

    titalFont = ImageFont.truetype(init.FONT_PATH + 'msyh.ttc', 40, index=1)
    w, h = titalFont.getsize(tital)

    if w > canvasLength:
        drawer.text((0, 10), tital, fill=0x000000, font=titalFont)
    else:
        drawer.text(((canvasLength - w)//2, 10), tital,
                    fill=0x000000, font=titalFont)

    datainfo = "（团队ID:" + \
        str(teaminfo['teamID']) + "） " + \
        GetDate(teaminfo['year']+'-' + teaminfo['startTime'])

    time_w, time_h = font.getsize(datainfo)

    team_w, team_h = font.getsize(teaminfo['comment'])

    if team_w + time_w < boxLength * 5:
        drawer.text((startX, startY - time_h - 5),
                    datainfo, fill=0x000000, font=font)
        drawer.text((startX + boxLength * 5 - team_w, startY -
                     team_h - 5), teaminfo['comment'], fill=0x000000, font=font)
    else:
        drawer.text((startX, startY - time_h - 5),
                    datainfo, fill=0x000000, font=font)
        drawer.text((startX + time_w + 5, startY -
                     team_h - 5), teaminfo['comment'], fill=0x000000, font=font)

    for i in range(5):
        drawer.rectangle(
            ((startX + (boxLength * i),
              startY,
              startX + boxLength*(i + 1),
              startY + boxHeight / 2)),
            fill=(255, 255, 255),
            outline=(0, 0, 0),
            width=1)
        drawer.text((startX + (boxLength * (i + 0.5)),
                     startY), int(i+1).__str__(), fill=(0, 0, 0), font=font)

    for i in range(len(external)):
        if i % 2 == 0:
            DrawRectangal(img, 0, i//2, external[i])
        elif i % 2 == 1:
            DrawRectangal(img, 1, i//2, external[i])

    for i in range(len(internal)):
        if i % 2 == 0:
            DrawRectangal(img, 2, i//2, internal[i])
        elif i % 2 == 1:
            DrawRectangal(img, 3, i//2, internal[i])

    for i in range(len(tank)):
        DrawRectangal(img, 4, i, tank[i])

    temp = len(tank)
    for i in range(len(healer)):
        DrawRectangal(img, 4, i+temp, healer[i])

    Time = time.strftime("%y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    name = Time + '-' + id.__str__() + '.jpg'
    img.save(init.IMAGE_PATH + name)

    return name
