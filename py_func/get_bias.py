import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import json
from collections import OrderedDict
import os
import csv
import subprocess


class get_bias:
    def __init__(self):
        pass

    def pre_download_data(self):
        command = "python3 py_func/get_six_day.py &"
        subprocess.Popen(command, shell=True)

    def get_stock_list(self):
        stock_list = {}
        for each in os.listdir("daily_result"):
            if "json" in each:
                json_name = os.path.join("daily_result", each)
                with open(json_name) as json_file:
                    result = json.load(json_file)
                    for x in result['data9']:
                        stock_list[x[0]] = x[1]
                break
        return stock_list

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

    def get_six_bias(self):
        stock_list = self.get_stock_list()
        day = self.get_six_work_day()
        result_dict = {}
        flag = 0
        for each in day:
            print(each)
            json_name = 'daily_result/{}.json'.format(each)
            if not os.path.isfile(json_name):
                return False
            with open(json_name) as json_file:
                result = json.load(json_file)
            if flag == 0:
                flag = 1
                for stock in result['data9']:
                    if len(str(stock[0])) == 4:
                        result_dict[stock[0]] = []
                        result_dict[stock[0]].append(stock[8])
            else:
                for stock in result['data9']:
                    if len(str(stock[0])) == 4:
                        try:
                            result_dict[stock[0]].append(stock[8])
                        except Exception:
                            pass
        new_dict = {}
        for each in result_dict:
            six_avg = self.count_list_six_sum(result_dict[each])
            three_avg = self.count_list_three_sum(result_dict[each])
            if six_avg and three_avg:
                tmp = (three_avg - six_avg)/float(result_dict[each][0])
                new_dict[each] = {"six_avg": six_avg,
                                  "three_avg": three_avg,
                                  "count": tmp,
                                  "value": float(result_dict[each][0])}
        x = sorted(new_dict.items(), key=lambda e: (float(e[1]['count'])), reverse=True)
        count = 0
        content = ""
        for each in x:
            if count >= 15:
                break
            if each:
                count += 1
                try:
                    stock_name = stock_list[each[0]]
                except Exception:
                    stock_name = ""
                content += "No.{}\n".format(str(count))
                content += "股票代碼: {}\n".format(each[0])
                content += "股票名稱: {}\n".format(stock_name)
                content += "三日平均: {}\n".format(round(each[1]['three_avg'],2))
                content += "六日平均: {}\n".format(round(each[1]['six_avg'],2))
                content += "收盤價: {}\n".format(round(each[1]['value'],2))
                if count < 15:
                    content += "---------\n"
        return content

    def count_list_six_sum(self, this_list):
        try:
            tmp_result = list(map(float, this_list))
        except Exception:
            return False
        return sum(tmp_result[:6])/6

    def count_list_three_sum(self, this_list):
        try:
            tmp_result = list(map(float, this_list))
        except Exception:
            return False
        return sum(tmp_result[:3])/3

if __name__ == '__main__':
    x = get_bias()
    x.pre_download_data()

