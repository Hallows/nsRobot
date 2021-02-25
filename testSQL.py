import sqlConnect as SQL
import pymysql

dbHost = '139.198.178.48'
dbPort = 3306
dbUser = 'root'
dbPassword = 'LOVE@alan1995'
dbName = 'ns_db'
dbCharset = 'utf8'

temp = pymysql.connect(host=dbHost, port=dbPort, user=dbUser, password=dbPassword, db=dbName, charset=dbCharset)

SQL.SQLConnect(temp)
#leaderID = SQL.has_Leader(602857593)
#print(leaderID)
#mentalID = SQL.getMental('补天诀')
#result = SQL.createNewTeam('2021-02-09', '19:00', '25YXDMD', 'suibian', leaderID, 1)
#result = SQL.addMember(1040, 602857593, '渡空离', mentalID, 1)
#result=SQL.delMember(1040,602857593)
#result=SQL.delTeam(1040,leaderID)
#print(SQL.newLeader(600857593, '渡空离', '啥时候都行'))
print(SQL.getInfo(1002))
