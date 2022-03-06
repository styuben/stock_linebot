
class get_drink_info:
    def __init__(self):
        self.drink_list = ["可不可熟成紅茶",
                           "麻古茶坊",
                           "龜記",
                           "迷客夏",
                           "清原",
                           "50嵐",
                           "五桐號",
                           "不要對我尖叫",
                           "茶乃士多"]

    def get_drink_list(self):
        return self.drink_list

    def get_drink_url(self, msg):
        original_content_url = []
        if msg == "可不可熟成紅茶":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/kbk.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/kbk.jpg'
        if msg == "麻古茶坊":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/ma.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/ma.jpg'
        if msg == "龜記":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/tur.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/tur.jpg'
        if msg == "迷客夏":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/milk.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/milk.jpg'
        if msg == "50嵐":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/50.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/50.jpg'
        if msg == "五桐號":
            original_content_url.append('https://www.wootea.com/upload/menu_b/ALL_menu_21I17_e5w7rh8j6e.png')
            # original_content_url='https://www.wootea.com/upload/menu_b/ALL_menu_21I17_e5w7rh8j6e.png'
        if msg == "不要對我尖叫":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/donot.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/donot.jpg'
        if msg == "茶乃士多":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/cha.jpg')
            # original_content_url='https://raw.githubusercontent.com/styuben/linebot/master/image/cha.jpg'
        if msg == "清原":
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/cir1.PNG')
            original_content_url.append('https://raw.githubusercontent.com/styuben/linebot/master/image/cir2.PNG')
        return original_content_url