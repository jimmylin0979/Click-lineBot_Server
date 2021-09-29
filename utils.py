import os
import json

from linebot import LineBotApi, WebhookParser
from linebot.models import *


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(str(channel_access_token))


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_beside_patient(reply_token):
    confirm_template = TemplateSendMessage(
        alt_text="Are you lost?",
        template=ConfirmTemplate(
            text="請問你現在在患者身邊嗎？",
            actions=[
                MessageTemplateAction(
                    label="否",
                    text="我現在不在患者身邊"
                ),
                MessageTemplateAction(
                    label="是",
                    text="呼叫119"
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, confirm_template)
    return "OK"

# send video


def send_video(reply_token, vid_url, image):
    video_message = VideoSendMessage(
        original_content_url=vid_url,
        preview_image_url=image
    )

    line_bot_api.reply_message(reply_token, video_message)

    return "OK"

# send info


def send_info(reply_token, word, information, current, brand):
    line_bot_api.reply_message(reply_token,
                               FlexSendMessage(
                                   "Information",
                                   {
                                       "type": "bubble",
                                       "body": {
                                           "type": "box",
                                           "layout": "vertical",
                                           "contents": [
                                               {
                                                   "type": "text",
                                                   "text": word,
                                                   "weight": "bold",
                                                   "size": "xxl",
                                                   "margin": "md"
                                               },
                                               {
                                                   "type": "separator",
                                                   "margin": "xl"
                                               },
                                               {
                                                   "type": "box",
                                                   "layout": "vertical",
                                                   "contents": [
                                                       {
                                                           "type": "text",
                                                           "text": information,
                                                           "wrap": True,
                                                       },
                                                   ],
                                                   "spacing": "sm",
                                                   "margin": "xxl"
                                               },
                                               {
                                                   "type": "separator",
                                                   "margin": "xxl"
                                               },
                                               {
                                                   "type": "text",
                                                   "text": "Where do you want to go?",
                                                   "size": "sm",
                                                   "wrap": True,
                                                   "margin": "xxl"
                                               },
                                               {
                                                   "type": "button",
                                                   "action": {
                                                       "type": "message",
                                                       "label": "Menu",
                                                       "text": "Menu"
                                                   },
                                                   "height": "sm"
                                               },
                                               {
                                                   "type": "button",
                                                   "action": {
                                                       "type": "message",
                                                       "label": brand,
                                                       "text": brand
                                                   },
                                                   "height": "sm"
                                               },
                                               {
                                                   "type": "button",
                                                   "action": {
                                                       "type": "message",
                                                       "label": current,
                                                       "text": current
                                                   },
                                                   "height": "sm"
                                               },
                                           ]
                                       },
                                       "styles": {
                                           "footer": {
                                               "separator": True
                                           }
                                       }
                                   }
                               )
                               )
    return "OK"


def send_place_carousel(reply_token):
    carousel_template = TemplateSendMessage(
        alt_text="knowledges",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    text="什麼樣的情況需要施行CPR及AED呢？",
                    thumbnail_image_url="https://i.imgur.com/abO5djB.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="為何不能幫患者叫救護車就好，還需要做這麼多的急救步驟呢？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="什麽是CPR?",
                    thumbnail_image_url="https://i.imgur.com/cuTMVcx.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="什麽是ADE?",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="AED的具體步驟要怎麼操作呀？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="要怎麼做才是滿分的CPR呢？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="鄉土劇常看到執行「人工呼吸」的CPR，但為什麼現在的CPR步驟裡不用做人工呼吸呢？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="聽說CPR會壓斷肋骨，這是真的嗎？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="內衣的鋼圈會影響到CPR的施行和AED的電擊嗎？急救的時候需要解開嗎？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="新聞常報導「救人反被告」的案例，協助急救會有什麼法律責任嗎？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案是什麽"
                        ),
                    ]
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, carousel_template)

    return "OK"
