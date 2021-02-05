import pymysql
import init

"命令格式：ns报团 团id 心法 "


def Input(data: list):
    db = pymysql.connect(host=init.dbHost, port=init.dbPort, user=init.dbUser,
                         password=init.dbPassword, db=init.dbName, charset=init.dbCharset)
