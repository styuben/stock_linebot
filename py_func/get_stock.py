import requests
import random

class get_stock:
    def __init__(self):
        pass

    def extract_time(self, json):
        try:
            if json['PEratio']:
                return float(json['PEratio'])
            else:
                return 0
        except KeyError:
            return 0

    def get_low_eps(self):
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_ALL")
        result = res.json()
        result.sort(key=self.extract_time, reverse=False)
        count = 0
        content = "查詢前一日本益比 Top10:\n"
        for each in result:
            if count >= 10:
                break
            if each['PEratio']:
                count += 1
                content += "No.{}\n".format(str(count))
                content += "股票名稱: {}\n".format(each['Name'])
                content += "股票代碼: {}\n".format(each['Code'])
                content += "本益比: {}\n".format(each['PEratio'])
                content += "殖利率: {}\n".format(each['DividendYield'])
                content += "股價淨值比: {}\n".format(each['PBratio'])
                if count < 10:
                    content += "---------\n"
        return content

    def get_most_trade(self):
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/MI_INDEX20")
        result = res.json()
        count = 0
        content = "查詢前一日交易量 Top10: \n"
        for each in result:
            if count >= 10:
                break
            if each['Rank']:
                count += 1
                content += "No.{}\n".format(str(count))
                content += "股票名稱: {}\n".format(each['Name'])
                content += "股票代碼: {}\n".format(each['Code'])
                content += "交易量: {}\n".format(each['TradeVolume'])
                content += "收盤價: {}\n".format(each['ClosingPrice'])
                if count < 10:
                    content += "---------\n"
        return content

    def extract_price_and_month(self, json):
        try:
            if json['ClosingPrice'] and json['MonthlyAveragePrice']:
                price = (float(json['MonthlyAveragePrice']) - float(json['ClosingPrice'])) / float(json['ClosingPrice'])
                return price
            else:
                return 0
        except KeyError:
            return 0

    def get_price_and_month(self):
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL")
        result = res.json()
        result.sort(key=self.extract_price_and_month, reverse=False)
        count = 0
        content = "查詢前一日收盤與月均差距(比例) Top10: \n"
        for each in result:
            if count >= 10:
                break
            if len(each['Code']) > 4:
                continue
            else:
                count += 1
                content += "No.{}\n".format(str(count))
                content += "股票名稱: {}\n".format(each['Name'])
                content += "股票代碼: {}\n".format(each['Code'])
                content += "收盤價: {}\n".format(each['ClosingPrice'])
                content += "月均價: {}\n".format(each['MonthlyAveragePrice'])
                if count < 10:
                    content += "---------\n"
        return content

    def get_random_stock(self):
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL")
        result = res.json()
        res2 = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_ALL")
        result2 = res2.json()
        new_dict = []
        for each in result:
            if len(each['Code']) != 4:
                continue
            else:
                new_dict.append(each)
        this_stock = random.choice(new_dict)
        this_PEratio = ""
        this_DividendYield = ""
        this_PBratio = ""
        for each in result2:
            if each['Code'] == this_stock['Code']:
                this_PEratio = each['PEratio']
                this_DividendYield = each['DividendYield']
                this_PBratio = each['PBratio']
                break
        content = "股票名稱: {}\n".format(this_stock['Name'])
        content += "股票代碼: {}\n".format(this_stock['Code'])
        content += "收盤價: {}\n".format(this_stock['ClosingPrice'])
        content += "本益比: {}\n".format(this_PEratio)
        content += "殖利率: {}\n".format(this_DividendYield)
        content += "股價淨值比: {}\n".format(this_PBratio)
        return content

if __name__ == '__main__':
    x = get_stock()
    # x.get_stock_five_day_avg()
    # x.get_stock_by_date_code("0050")
    # day = x.get_five_work_day()
    # x.get_five_day_data()
    content = x.get_random_stock()
    print(content)
