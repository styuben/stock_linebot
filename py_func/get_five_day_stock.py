import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import json
from collections import OrderedDict
import os
import csv
# import twstock

class get_five_day_stock:
    def __init__(self):
        pass

    def get_stock_list(self):
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL")
        result = res.json()
        stock_list = {}
        for each in result:
            stock_list[each['Code']] = each['Name']
        return stock_list

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

    def get_five_day_data_top30(self):
        content = ""
        count = 0
        if not os.path.isfile("daily_result/five_day_result.txt"):
            content = "請先查詢前一日收盤與五日均價差距Top15"
        x = json.load(open("daily_result/five_day_result.txt"))
        stock_list = self.get_stock_list()
        for each in x:
            if count >= 30:
                break
            if each:
                count += 1
                content += "No.{} ".format(str(count))
                content += "{} ".format(each[0])
                content += "{}\n".format(stock_list[each[0]])
                content += "收盤價: {}\n".format(each[1]['now_price'])
                if count < 30:
                    content += "---------\n"
        return content

    def get_five_day_data_health(self):
        content = ""
        if not os.path.isfile("daily_result/five_day_result.csv"):
            content = "請先查詢前一日收盤與五日均價差距Top15"
        else:
            with open("daily_result/five_day_result.csv", "r") as f:
                rows = csv.reader(f)
                for row in rows:
                    if row:
                        content += "No.{} {} {}\n".format(str(row[0]), str(row[1]), str(row[2]))
                        content += "收盤價: {}\n".format(str(row[3]))
                        # content += "{}".format(self.check_four_point_content(str(row[1])))
        return content

    def get_five_day_data(self):
        day = self.get_five_work_day()
        flag = 0
        result_dict = {}
        for each in day:
            print(each)
            if not os.path.isfile('daily_result/{}.json'.format(each)):
                url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?re'
                url += 'sponse=json&date=' + each + '&type=ALL'
                r = requests.post(url)
                result = r.json()
                with open('daily_result/{}.json'.format(each), 'w') as outfile:
                    json.dump(result, outfile)
            else:
                result = ""
                with open('daily_result/{}.json'.format(each)) as json_file:
                    result = json.load(json_file)
            if flag == 0:
                flag = 1
                for stock in result['data9']:
                    result_dict[stock[0]] = []
                    result_dict[stock[0]].append(stock[8])
            else:
                for stock in result['data9']:
                    try:
                        result_dict[stock[0]].append(stock[8])
                    except Exception:
                        pass
        new_dict = {}
        for each in result_dict:
            if len(each) != 4:
                continue
            if len(result_dict[each]) == 5:
                try:
                    tmp_result = list(map(float, result_dict[each]))
                except Exception:
                    continue
                new_dict[each] = {}
                avg = sum(tmp_result)/5
                new_dict[each]["now_price"] = result_dict[each][0]
                new_dict[each]["five_avg_price"] = str(avg)
                new_dict[each]["target"] = \
                    (float(result_dict[each][0]) - float(avg)) / float(result_dict[each][0])
        # json_object.sort(key=self.extract_price, reverse=False)
        x = sorted(new_dict.items(), key=lambda e: (float(e[1]['target'])), reverse=True)
        json.dump(x, open("daily_result/five_day_result.txt",'w'))
        count = 0
        content = ""
        stock_list = self.get_stock_list()
        csv_content = ""
        for each in x:
            if count >= 15:
                break
            if each:
                count += 1
                content += "No.{}\n".format(str(count))
                content += "股票代碼: {}\n".format(each[0])
                content += "股票名稱: {}\n".format(stock_list[each[0]])
                content += "收盤價: {}\n".format(each[1]['now_price'])
                five_day_avg = float(each[1]['five_avg_price'])
                five_day_avg = str(round(five_day_avg, 2))
                content += "前五日均價: {}\n".format(five_day_avg)
                csv_content += "{},{},{},{},{}\n".format(count,
                                              each[0],
                                              stock_list[each[0]],
                                              each[1]['now_price'],
                                              five_day_avg)
                if count < 15:
                    content += "---------\n"
        with open("daily_result/five_day_result.csv", "w") as f:
            f.write(csv_content)
        return content

    def extract_price(self, json):
        try:
            if json['now_price'] and json['five_avg_price']:
                price = (float(json['five_avg_price']) - float(json['now_price'])) / float(json['now_price'])
                return price
            else:
                return 0
        except KeyError:
            return 0

    def get_five_work_day(self):
        count = 0
        day_count = 1
        day_list = []
        while True:
            pre_day = datetime.date.today() - datetime.timedelta(day_count)
            if pre_day.weekday() >=0 and pre_day.weekday() <=4:
                count += 1
                pre_day = pre_day.strftime("%Y%m%d")
                # trans_day = str(int(str(pre_day)[0:4])-1911)
                # trans_day +=  str(pre_day)[4:]
                day_list.append(pre_day)
                if count >=5:
                    break
            day_count += 1
        return (day_list)

if __name__ == '__main__':
    x = get_five_day_stock()
    # x.get_stock_five_day_avg()
    # x.get_stock_by_date_code("0050")
    # day = x.get_five_work_day()
    x.get_five_day_data()
    content = x.get_five_day_data_top30()
    print(content)
