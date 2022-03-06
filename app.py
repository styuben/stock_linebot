import os
from datetime import datetime
import re
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import py_func.get_stock as get_stock
import py_func.stock_health as stock_health
import py_func.get_eps as get_eps
import py_func.get_five_day_stock as get_five_day_stock
import py_func.get_bias as get_bias
import time
app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    print("got msg: {}".format(get_message))

    # Send To Line
    # reply = TextSendMessage(text=f"{get_message}")
    # line_bot_api.reply_message(event.reply_token, reply)
    if re.match('查股票',get_message):
        Carousel_template = TemplateSendMessage(
            alt_text='查股票',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/styuben/linebot/master/image/title.png',
                        title='Menu',
                        text='請選擇功能',
                        actions=[
                            MessageTemplateAction(
                                label='查詢前一日本益比Top10',
                                text='查詢前一日本益比Top10'
                            ),
                            MessageTemplateAction(
                                label='查詢前一日交易量Top10',
                                text='查詢前一日交易量Top10'
                            ),
                            MessageTemplateAction(
                                label='查詢EPS與收盤計算Top30',
                                text='查詢EPS與收盤計算Top30'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/styuben/linebot/master/image/title.png',
                        title='Menu',
                        text='請選擇功能',
                        actions=[
                            MessageTemplateAction(
                                label='預抓資料',
                                text='預抓資料'
                            ),
                            MessageTemplateAction(
                                label='收盤與五日均價差Top15',
                                text='查詢前一日收盤與五日均價差距Top15-先點預抓資料不然會timeout'
                            ),
                            MessageTemplateAction(
                                label='Top30五日均價差',
                                text='Top30五日均價差-先點預抓資料不然會timeout'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://raw.githubusercontent.com/styuben/linebot/master/image/title.png',
                        title='Menu',
                        text='請選擇功能',
                        actions=[
                            MessageTemplateAction(
                                label='3-6日均價差距Top15',
                                text='3-6日均價差距Top15'
                            ),
                            MessageTemplateAction(
                                label='查詢前一日收盤與月均差距Top10',
                                text='查詢前一日收盤與月均差距Top10'
                            ),
                            MessageTemplateAction(
                                label='隨便來一檔',
                                text='隨便來一檔'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, Carousel_template)
    else:
        if event.message.text == "3-6日均價差距Top15":
            test = get_bias.get_bias()
            content = test.get_six_bias()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if event.message.text == "預抓資料":
            test = get_bias.get_bias()
            test.pre_download_data()
            content = "請稍後約1分鐘後再執行其他功能"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if event.message.text == "查詢前一日本益比Top10":
            test = get_stock.get_stock()
            content = test.get_low_eps()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if event.message.text == "查詢前一日交易量Top10":
            test = get_stock.get_stock()
            content = test.get_most_trade()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if event.message.text == "查詢前一日收盤與月均差距Top10":
            test = get_stock.get_stock()
            content = test.get_price_and_month()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if "查詢前一日收盤與五日均價差距Top15" in event.message.text:
            test = get_five_day_stock.get_five_day_stock()
            try:
                start = time.time()
                content = test.get_five_day_data()
                end = time.time()
                duration = end - start
                duration = round(duration, 2)
                content += "\n\n 計算時間: {}\n".format(str(duration))
            except Exception as e:
                print(str(e))
                content = "發生異常，請稍後再試一次！"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if "Top30五日均價差" in event.message.text:
            test = get_five_day_stock.get_five_day_stock()
            try:
                content = test.get_five_day_data_top30()
            except Exception as e:
                print(str(e))
                content = "發生異常，請稍後再試一次！"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if event.message.text == "隨便來一檔":
            test = get_stock.get_stock()
            content = test.get_random_stock()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
        if event.message.text == "查詢EPS與收盤計算Top30":
            test = get_eps.get_eps()
            content = test.get_eps_result()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )
    if "查指令" in event.message.text:
        msg = "目前可用指令有：\n 1.查股票"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    if "查個股" in event.message.text:
        code = event.message.text.split("查個股")[-1]
        if len(code) != 4:
            msg = "請輸入正確的股票代碼！"
        else:
            x = stock_health.stock_health()
            msg = x.check_four_point_content(code)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
