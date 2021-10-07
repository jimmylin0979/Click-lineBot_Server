import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_Menu_button, send_go_to_menu_button

load_dotenv()
machine = {}

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


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


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine = TocMachine().machine
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    TocMachine().machine.get_graph().draw("fsm.png", prog="dot", format="png")
    port = os.environ.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port, debug=True)
