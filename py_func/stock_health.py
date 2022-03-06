import twstock
import time

class stock_health:
    def __init__(self):
        pass

    def check_four_point_content(self, code):
        content = ""
        try:
            get_stock = twstock.Stock(str(code))
            bfp = twstock.BestFourPoint(get_stock)
            buy = bfp.best_four_point_to_buy()
            sell = bfp.best_four_point_to_sell()
            content += "買點分析：\n"
            if buy:
                content += f"{str(buy)}\n"
            else:
                content += "不適合買\n"
            content += "\n"
            content += "賣點分析：\n"
            if sell:
                content += f"{str(sell)}\n"
            else:
                content += "不適合賣\n"
        except Exception as e:
            print(str(e))
            content = "請輸入正確的股票代碼！"
        return content