import pandas as pd
import requests

class get_eps:
    def __init__(self):
        pass

    def get_eps_result(self):
        filename = "./csv/eps_202103new.csv"
        user_config = pd.read_csv(filename)
        stock_list = self.get_stock_list()
        eps_dict = {}
        for each in stock_list:
            try:
                raw = user_config.loc[user_config["公司代號"] == int(each)]
                eps = raw['Q3_EPS'].values[0]
                eps_dict[each] = eps
            except Exception as e:
                pass
        result_dict = {}
        for each in eps_dict:
            try:
                tmp = []
                result = float(eps_dict[each]) * 15 * 4 - float(stock_list[each][1])
                result = round(result, 2)
                tmp = [stock_list[each][0],stock_list[each][1],eps_dict[each],result]
                result_dict[each] = tmp
            except Exception as e:
                pass
        x = sorted(result_dict.items(), key=lambda e: (float(e[1][3])), reverse=True)
        count = 0
        content = "查詢 EPS*15*4-收盤 Top30\n---------\n"
        for each in x:
            if count >= 30:
                break
            if each:
                count += 1
                content += "No.{} ".format(str(count))
                content += "{} ".format(each[1][0])
                content += "{} \n".format(each[0])
                content += "收盤價: {}\n".format(str(each[1][1]))
                content += "EPS: {}\n".format(str(each[1][2]))
                var = round(each[1][3], 2)
                var = "%.2f" % var
                content += "公式值: {}\n".format(str(var))
                if count < 30:
                    content += "---------\n"
        content = content.rsplit("\n", 1)[0]
        return content

    def get_stock_list(self):
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_AVG_ALL")
        result = res.json()
        stock_list = {}
        for each in result:
            if len(each['Code']) == 4:
                stock_list[each['Code']] = [each['Name'],each['ClosingPrice']]
        return stock_list

if __name__ == '__main__':
    x = get_eps()
    x.get_eps_result()
