import re
from pyunit_time import Time


def parseDate(date):
    tokens = ['月', '-', '.', '/', '//']
    date = date.replace('周', '星期').replace('礼拜', '星期')

    for token in tokens:
        regex = re.findall('^\d{1,2}\\'+token+'\d{1,2}', date)
        if regex:
            mm, dd = regex[0].split(token)
            date = mm + '月' + dd + '日'

    try:
        res = Time().parse(date)
        res = res[0]['keyDate'][:10] # yyyy-mm-dd HH:MM:SS
        #for i in range(len(res)):
        #    print(res[i]['keyDate'][5:10] + ' ')
    except Exception as ex:
        print(str(ex))
        res = -1 #'日期错误！'

    return res

def parseTime(time):
    try:
        res = Time('2021-01-01 00:00:00').parse(time)
        res = res[0]['keyDate'][11:16] # yyyy-mm-dd HH:MM:SS
    except Exception as ex:
        print(str(ex))
        res = -1 #'时间错误！'

    return res
