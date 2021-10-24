import os
import sys
import configparser
from random import randrange, randint

#
from flask import Flask, jsonify, request, abort, send_file, render_template
from dotenv import load_dotenv
import json

#
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

#
from fsm import TocMachine
from utils import send_text_message, send_Menu_button, send_go_to_menu_button

#
import libs.AEDMap.AEDMap as AEDMap

app = Flask(__name__, static_url_path="")

#########################################################################################
### Configuration Here ###

############################
# 讀取 Config.ini 設置檔
config = configparser.ConfigParser()
config.read('config.ini')

############################
# Flask 網站設定

# LINE 聊天機器人的基本資料
# 向 config.ini 讀取 channel_secret 及 channel_access_token
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
parser = WebhookParser(config.get('line-bot', 'channel_secret'))

# # get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
# channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
# if channel_secret is None:
#     print("Specify LINE_CHANNEL_SECRET as environment variable.")
#     sys.exit(1)
# if channel_access_token is None:
#     print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
#     sys.exit(1)
# line_bot_api = LineBotApi(channel_access_token)
# parser = WebhookParser(channel_secret)

# LineBot 拒絕對話與回應的 黑名單，如官方罐頭訊息等
blackList = ['Udeadbeefdeadbeefdeadbeefdeadbeef']

############################
# AED 地圖，路徑規劃 與 可互動式地圖
# Create a AEDMap object
fmap = AEDMap.AEDMap()

############################
# Click 機台編號紀錄
machine = {}

############################
# HTML 更新變數
HtmlVar_CPR_Depth = 0
HtmlVar_CPR_Freq = 0
HtmlVar_Breath_Freq = 0
HtmlVar_HeartRate = 0

#########################################################################################

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        user_id = event.source.user_id
        if user_id not in machine:
            machine[user_id] = TocMachine()

        print(f"\nFSM STATE: {machine[user_id].state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine[user_id].advance(event)
        if response == False:
            send_go_to_menu_button(event.reply_token)

    return "OK"

#########################################################################################

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Gauge

############################
# 線性圖

# 歷史趨勢圖 基底
def LineChart_Prototype() -> Line:
    line = (
        Line()
        .add_xaxis([0])
        .add_yaxis(
            series_name="",
            y_axis=[0],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line

# 對 data_page.html 進行變數更新，如心律、呼吸狀態
@app.route('/data_page', methods=['GET', 'POST'])
def data_page():
    # print(HtmlVar_Breath_Freq)
    # print(HtmlVar_HeartRate)
    # TODO : 改以 Ajax 動態更新網頁，update html without refresh
    return render_template('data_page.html', HtmlVar_Breath_Freq=HtmlVar_Breath_Freq, HtmlVar_HeartRate=HtmlVar_HeartRate)

# 資料點由 1 開始，原點 (0, 0)
idx = 1

# 
@app.route("/lineChart")
def get_line_chart():
    c = LineChart_Prototype()
    return c.dump_options_with_quotes()

############################
# 儀表板

# 儀表板 基底
def GaugeChart_Prototype() -> Gauge:
    gauge = (
        Gauge()
        .add("", [("", 66.6)], 
            min_=60, max_= 160, radius="80%", 
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.4, "#67e0e3"), (0.6, "#37a2da"), (1, "#fd666d")], width=30
                )),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
            legend_opts=opts.LegendOpts(is_show=True),
            # visualmap_opts=opts.VisualMapOpts(
            #     pieces=[
            #         {"min":60, "max":100}, 
            #         {"min":100, "max":120}, 
            #         {"min":120, "max":160}, 
            #     ]
            # )
        )
    )
    return gauge

# 
@app.route("/gaugeChart")
def get_gauge_chart():
    c = GaugeChart_Prototype()
    return c.dump_options_with_quotes()

############################
# 深度 Bar

def BarChart_Prototype() -> Bar:
    bar = (
        Bar()
            .add_xaxis(["深度"])
            .add_yaxis("A", [randint(10, 100)])
            .set_global_opts(title_opts=opts.TitleOpts(title="", subtitle=""))
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(y=50, name="yAxis=50")]
                ))
    )
    return bar

@app.route("/barChart")
def get_bar_chart():
    c = BarChart_Prototype()
    return c.dump_options_with_quotes()

############################
# 以 Ajax 動態更新 網頁內容
@app.route("/getDynamicData")
def update_line_data():
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "Breath_Freq": 2, "HeartRate": 1, "CPR_Depth": randrange(50, 80), "CPR_Freq": randrange(100, 120)})

#########################################################################################

# 提供給 ESP32 傳遞資訊 的 接口，寫入
@app.route("/esp", methods=['POST'])
def esp():
    if request.method == 'POST':
        '''
        POST should receive json in this format
        {
            "CPR_Depth": 2,
            "CPR_Freq": 1,
            "Breath_Freq": 1,
            "HeartRate": 120
        }
        '''
        # 
        recv = request.get_data(as_text=True)
        recv = json.loads(recv)
        print(f'{recv}')
        
        # 
        global HtmlVar_CPR_Depth, HtmlVar_CPR_Freq, HtmlVar_Breath_Freq, HtmlVar_HeartRate
        HtmlVar_CPR_Depth = recv['CPR_Depth']
        HtmlVar_CPR_Freq = recv['CPR_Freq']
        HtmlVar_Breath_Freq = recv['Breath_Freq']
        HtmlVar_HeartRate = recv['HeartRate']

        return 'Succeed : POST'

    # elif request.method == 'GET':
    #     print(f'{type(request)} : {request}')
    #     return 'Succeed : GET'

    # 未被伺服器處理，
    abort(500)

#########################################################################################

# 提供 AED 查看地圖
@app.route("/AEDMap", methods=['POST', 'GET'])
def get_AEDMap():

    # TODO : 將 frm, des 由發送的之訊息獲得，如 LocationMessage
    # set the from & destination
    user_location = [22.6, 120.3]

    # roting from user_location to shortest AED place
    des = fmap.get_Nearby_AEDLocation(user_location)[0]

    # and draw a map in html
    return fmap.get_Routing_Map(user_location, des.pos)

# @app.route("/show-fsm", methods=["GET"])
# def show_fsm():
#     machine = TocMachine().machine
#     machine.get_graph().draw("fsm.png", prog="dot", format="png")
#     return send_file("fsm.png", mimetype="image/png")

#########################################################################################

if __name__ == "__main__":
    # TocMachine().machine.get_graph().draw("fsm.png", prog="dot", format="png")
    # port = os.environ.get("PORT", 5000)

    # 獲取 本地端 port 接口、 DEBUG 模式
    PORT = config.get('flask-server', 'server_port')
    HOST = config.get('flask-server', 'server_host')

    app.run(host=HOST, port=PORT, debug=True, threaded=True)
