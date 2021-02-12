from PIL import Image, ImageDraw, ImageFont
import pymysql
from math import ceil
import time
from datetime import datetime
import init

boxLength = 200
boxHeight = 50

startX = 100
startY = 116

font = ImageFont.truetype(init.FONT_PATH + 'msyh.ttc', 20, index=1)


def GetDate(date: datetime):
    print(date)
    week = {0: "周一", 1: "周二", 2: "周三",
            3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    dateStr = week[date.weekday()] + ' '
    dateStr += time.strftime("%m月%d日 %H:%M", date.timetuple())
    return dateStr


def DrawRectangal(db: pymysql.connections.Connection, img: Image.Image, x: int, y: int, info: list):

    drawer = ImageDraw.Draw(img)

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM ns_mental WHERE mentalID = " + info[3].__str__())
    mental = cursor.fetchone()

    drawer.rectangle(
        (startX + x*boxLength,
         startY + (boxHeight / 2) + y * boxHeight,
         startX + (x+1)*boxLength,
         startY + (boxHeight / 2) + (y+1) * boxHeight),
        fill=GetRGB(mental[4]),
        outline=(0, 0, 0),
        width=1
    )

    drawer.text((startX + (0.3+x)*boxLength,
                 startY + (boxHeight / 2) + (y + 0.25) * boxHeight), info[2], font=font, fill=0x000000)

    r = boxLength / 10

    drawer.ellipse((startX + x*boxLength + (boxLength * 0.05),
                    startY + (boxHeight / 2) + y *
                    boxHeight + (boxHeight / 2 - r),
                    startX + x*boxLength + (boxLength * 0.05) + 2*r,
                    startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 + r)), fill=0x000000, outline=None)

    logo = Image.open(init.MENTAL_ICON_PATH + mental[2])
    logo = logo.resize((int(r * 1.8), int(r * 1.8)), Image.ANTIALIAS)
    R, G, B, A = logo.split()
    img.paste(logo, (int(startX + x*boxLength + (boxLength * (0.25) - 1.9 * r)),
                     int(startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 - 0.9*r))), mask=A)
    while True:
        if info[4] == 1:
            if mental[6] == 0:
                break
            cursor.execute(
                "SELECT * FROM ns_mental WHERE mentalID = " + mental[6].__str__())
            mentalConnection = cursor.fetchone()
            drawer.ellipse((startX + x*boxLength + (boxLength * 0.25) - r,
                            startY + (boxHeight / 2) + y*boxHeight +
                            (boxHeight / 2),
                            startX + x*boxLength + (boxLength * 0.05) + 2*r,
                            startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 + r)), fill=0x000000, outline=0xffffff, width=1)
            logo = Image.open(init.MENTAL_ICON_PATH + mentalConnection[2])
            logo = logo.resize((int(r * 0.9), int(r * 0.9)), Image.ANTIALIAS)
            R, G, B, A = logo.split()
            img.paste(logo, (int(startX + x*boxLength + (boxLength * (0.25) - 0.9 * r)),
                             int(startY + (boxHeight / 2) + y*boxHeight + (boxHeight / 2 + 0.1*r))), mask=A)
        break


def GetRGB(id: str) -> tuple:
    r = int(id[0:2], 16)
    g = int(id[2:4], 16)
    b = int(id[4:6], 16)
    return (r, g, b)


def GetMember(db: pymysql.connections.Connection, id: int):
    # 读取数据库得到数据，返回列表

    cursor = db.cursor()
    cursor.execute("SELECT * FROM ns_member WHERE teamID = " + id.__str__())
    memberlist = cursor.fetchall()

    return (id, memberlist)


def GenerateImage(db: pymysql.connections.Connection, teamdata: tuple):
    # 根据列表生成图片，返回文件名

    canvasLength = 1200
    canvasHeight = 480

    memberCount = len(teamdata[1])
    internal = []
    external = []
    healer = []
    tank = []

    cursor = db.cursor()

    if not memberCount:
        return "No Team"

    for member in teamdata[1]:
        cursor.execute(
            "SELECT * FROM ns_mental WHERE mentalID = " + member[3].__str__())

        mental = cursor.fetchone()

        if mental[5] == 1:
            tank.append(member)
        elif mental[5] == 2:
            healer.append(member)
        elif mental[5] == 3:
            internal.append(member)
        elif mental[5] == 4:
            external.append(member)

    cursor.execute("SELECT * FROM ns_team WHERE teamID = " +
                   teamdata[0].__str__())
    teaminfo = cursor.fetchone()

    cursor.execute("SELECT * FROM ns_leader WHERE id = " +
                   teaminfo[1].__str__())
    leaderinfo = cursor.fetchone()

    if len(internal) > 10 or len(external) > 10 or len(tank) + len(healer) > 5:
        print(ceil(len(internal) / 2))
        num = max(ceil(len(internal) / 2),
                  ceil(len(external) / 2),
                  len(tank) + len(healer))

        canvasHeight += (num - 5) * boxHeight

    img = Image.new("RGB", (canvasLength, canvasHeight), (255, 255, 255))

    drawer = ImageDraw.Draw(img)

    tital = leaderinfo[2] + " " + teaminfo[2]

    titalFont = ImageFont.truetype(init.FONT_PATH + 'msyh.ttc', 40, index=1)
    w, h = titalFont.getsize(tital)

    if w > canvasLength:
        drawer.text((0, 10), tital, fill=0x000000, font=titalFont)
    else:
        drawer.text(((canvasLength - w)//2, 10), tital,
                    fill=0x000000, font=titalFont)

    datainfo = "（团队ID:" + teamdata[0].__str__() + "） " + GetDate(teaminfo[3])

    time_w, time_h = font.getsize(datainfo)

    team_w, team_h = font.getsize(teaminfo[6])

    if team_w + time_w < boxLength * 5:
        drawer.text((startX, startY - time_h - 5),
                    datainfo, fill=0x000000, font=font)
        drawer.text((startX + boxLength * 5 - team_w, startY -
                     team_h - 5), teaminfo[6], fill=0x000000, font=font)
    else:
        drawer.text((startX, startY - time_h - 5),
                    datainfo, fill=0x000000, font=font)
        drawer.text((startX + time_w + 5, startY -
                     team_h - 5), teaminfo[6], fill=0x000000, font=font)

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
            DrawRectangal(db, img, 0, i//2, external[i])
        elif i % 2 == 1:
            DrawRectangal(db, img, 1, i//2, external[i])

    for i in range(len(internal)):
        if i % 2 == 0:
            DrawRectangal(db, img, 2, i//2, internal[i])
        elif i % 2 == 1:
            DrawRectangal(db, img, 3, i//2, internal[i])

    for i in range(len(tank)):
        DrawRectangal(db, img, 4, i, tank[i])

    temp = len(tank)
    for i in range(len(healer)):
        DrawRectangal(db, img, 4, i+temp, healer[i])

    Time = time.strftime("%y-%m-%d-%H-%M-%S", time.localtime(time.time()))

    name = init.IMAGE_PATH + Time + '-' + teamdata[0].__str__() + '.jpg'

    img.save(name)

    return name


def GetImg(id: int) -> str:
    db = pymysql.connect(host=init.dbHost, port=init.dbPort, user=init.dbUser,
                         password=init.dbPassword, db=init.dbName, charset=init.dbCharset)
    return GenerateImage(db, GetMember(db, id))
    db.close()
