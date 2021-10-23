import os
import sys
import configparser

#
from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv

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


@app.route("/hello")
def haha():
    return "hi"

# 提供給 ESP32 傳遞資訊 的 接口，寫入
@app.route("/esp", methods=['POST', 'GET'])
def esp():
    if request.method == 'POST':
        print(f'POST Message : {request.get_data(as_text=True)}')
        return 'Succeed : POST'
    elif request.method == 'GET':
        print(request)
        return 'Succeed : GET'

    # 未被伺服器處理，
    abort(500)

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
