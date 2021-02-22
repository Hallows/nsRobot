import re
from pyunit_time import Time


def parseDate(date):
    tokens = ['月', '-', '.', '/', '\']
  
    for token in tokens:
        regex = re.findall('^\d{1,2}\'+token+'\d{1,2}', date)
        if regex:
            mm, dd = regex[0].split(token)
            date = mm + '月' + dd + '日'

    try:
        res = Time().parse(date)
        res = res[0]['keyDate'][:10]
        #for i in range(len(res)):
        #    print(res[i]['keyDate'][5:10] + ' ')
    except Exception as ex:
        print(str(ex))
        res = '日期错误！'

    return res
