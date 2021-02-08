import generate_image
import pymysql
import init

db = pymysql.connect(host=init.dbHost, port=init.dbPort, user=init.dbUser,
                     password=init.dbPassword, db=init.dbName, charset=init.dbCharset)

generate_image.GetImg(db, 1001)

db.close()
