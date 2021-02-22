import re
from pyunit_time import Time


def parseDate(date):
  res = re.findall('^\d{1,2}月\d{1,2}', date)
  if res:
    mm, dd = res[0].split('月')
    date = mm + '月' + dd + '日'

  res = re.findall('^\d{1,2}-\d{1,2}', date)
  if res:
    mm, dd = res[0].split('-')
    date = mm + '月' + dd + '日'

  res = re.findall('^\d{1,2}\.\d{1,2}', date)
  if res:
    mm, dd = res[0].split('.')
    date = mm + '月' + dd + '日'

  try:
    res = Time().parse(date)
    for i in range(len(res)):
      print(res[i]['keyDate'][5:10] + ' ')
  except:
    print('日期不存在！')
