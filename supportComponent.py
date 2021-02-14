from datetime import datetime
import time

def changeTime(date, time):
    if date == '今天':
        outdate = datetime.date.today()
    if date == '明天':
        outdate = yesterday = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')
    if date == '后天':
        outdate = yesterday = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%Y%m%d')
    try:
        