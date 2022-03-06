from twstock import Stock
import time

class get_stock_by_twstock:
    def __init__(self):
        pass

    def get_five_price(self, code):
        start = time.time()
        stock = Stock(str(code))
        ma_p = sum(stock.price[-5:])/5
        end = time.time()
        duration = end - start
        content = "股票代碼: {}\n".format(str(code))
        content += "股票五日均價: {}\n".format(str(ma_p))
        content += "計算時間: {}\n".format(str(duration))
        return content



