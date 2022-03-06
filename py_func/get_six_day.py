import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import json
from collections import OrderedDict
import os
import csv

class get_six_day:
    def __init__(self):
        pass

    def get_six_work_day(self):
        count = 0
        day_count = 1
        day_list = []
        while True:
            pre_day = datetime.date.today() - datetime.timedelta(day_count)
            if pre_day.weekday() >=0 and pre_day.weekday() <=4:
                count += 1
                pre_day = pre_day.strftime("%Y%m%d")
                day_list.append(pre_day)
                if count >=7:
                    break
            day_count += 1
        return (day_list)

    def get_six_day_csv(self):
        day = self.get_six_work_day()
        for each in day:
            print(each)
            if not os.path.isfile('daily_result/{}.json'.format(each)):
                url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?re'
                url += 'sponse=json&date=' + each + '&type=ALL'
                r = requests.post(url)
                result = r.json()
                with open('daily_result/{}.json'.format(each), 'w') as outfile:
                    json.dump(result, outfile)

if __name__ == '__main__':
    x = get_six_day()
    x.get_six_day_csv()
