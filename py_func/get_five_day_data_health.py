import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import json
from collections import OrderedDict
import os
import csv
import twstock
import time

class get_five_day_data_health:
    def __init__(self):
        pass

    def check_four_point_content(self, code):
        print(code)
        content = ""
        get_stock = twstock.Stock(str(code))
        bfp = twstock.BestFourPoint(get_stock)
        buy = bfp.best_four_point_to_buy()
        sell = bfp.best_four_point_to_sell()
        content += "買點分析："
        if buy:
            content += f"{str(buy)}\n"
        else:
            content += "不適合買\n"
        content += "賣點分析："
        if sell:
            content += f"{str(sell)}\n"
        else:
            content += "不適合賣\n"
        return content

    def get_five_day_data_health(self):
        content = ""
        csv_path = os.path.join("daily_result","five_day_result.csv")
        if not os.path.isfile(csv_path):
            content = "請先查詢前一日收盤與五日均價差距Top15"
        else:
            with open("daily_result/five_day_result.csv", "r") as f:
                rows = csv.reader(f)
                for row in rows:
                    if row:
                        content += "No.{} {} {}\n".format(str(row[0]), str(row[1]), str(row[2]))
                        content += "收盤價: {}\n".format(str(row[3]))
                        content += "{}".format(self.check_four_point_content(str(row[1])))
                        time.sleep(3)
        return content