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


def send_go_to_menu_button(reply_token):
    confirm_template = TemplateSendMessage(
        alt_text="Are you lost?",
        template=ConfirmTemplate(
            text="是否回去主選單呢？",
            actions=[
                MessageTemplateAction(
                    label="YES!",
                    text="Menu"
                ),
                MessageTemplateAction(
                    label="你沒得選",
                    text="Menu"
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, confirm_template)
    return "OK"


def send_beside_patient_button(reply_token):
    confirm_template = TemplateSendMessage(
        alt_text="beside patient?",
        template=ConfirmTemplate(
            text="請問您現在在患者身邊嗎？",
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


def send_call_button(reply_token):
    button_template = TemplateSendMessage(
        alt_text="call_119",
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='119急難求助專線',
            text='24小時全年無休協助救援連線',
            actions=[
                MessageAction(
                    label='撥打119緊急電話',
                    text='119'
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, button_template)

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

# send info 2


def send_info_2(reply_token, word, information, current, brand, series):
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
                                                       "label": series,
                                                       "text": series
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

# send menu


def send_Menu_button(reply_token):
    button_template = TemplateSendMessage(
        alt_text="Menu",
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='請問你需要什麽協助',
            text='別擔心，我會提供您完善的引導！',
            actions=[
                MessageAction(
                    label='有人暈倒了，我該怎麽...',
                    text='呼叫定位精靈'
                ),
                MessageAction(
                    label='最近的AED在哪裏？',
                    text='呼叫AED地圖'
                ),
                MessageAction(
                    label='我想學習急救知識~',
                    text='呼叫急救知識庫'
                ),
                MessageAction(
                    label='我想學習按壓指導',
                    text='按壓指導'
                ),
                '''MessageAction(
                    label='我想學習急救流程',
                    text='急救流程'
                ),'''
            ]
        )
    )
    line_bot_api.reply_message(reply_token, button_template)

    return "OK"

# 急救知識庫


def send_self_study_carousel(reply_token):
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
                            text="答案1是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="為何不能幫患者叫救護車就好，還需要做這麼多的急救步驟呢？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案2是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="什麽是CPR?",
                    thumbnail_image_url="https://i.imgur.com/cuTMVcx.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案3是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="什麽是ADE?",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案4是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="AED的具體步驟要怎麼操作呀？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案5是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="要怎麼做才是滿分的CPR呢？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案6是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="鄉土劇常看到執行「人工呼吸」的CPR，但為什麼現在的CPR步驟裡不用做人工呼吸呢？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案7是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="聽說CPR會壓斷肋骨，這是真的嗎？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案8是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="內衣的鋼圈會影響到CPR的施行和AED的電擊嗎？急救的時候需要解開嗎？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案9是什麽!"
                        ),
                    ]
                ),
                CarouselColumn(
                    text="新聞常報導「救人反被告」的案例，協助急救會有什麼法律責任嗎？",
                    thumbnail_image_url="https://i.imgur.com/6KZn20I.jpg",
                    actions=[
                        MessageTemplateAction(
                            label="點我看解答",
                            text="答案10是什麽!"
                        ),
                    ]
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, carousel_template)

    return "OK"

# 外部鏈接


def send_outsideLink_button(reply_token, word):
    send_text_message(reply_token, word)
    button_template = TemplateSendMessage(
        alt_text='outside_link',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='急救知識網站',
            text='還想了解更多的急救知識嗎？歡迎參考我們推薦的網站!',
            actions=[
                URITemplateAction(
                 label='安妮怎麼了',
                 text='https://www.anne.education/'
                ),
                URITemplateAction(
                    label='消防署資訊網',
                    uri='https://www.nfa.gov.tw/cht/index.php'
                ),
                URITemplateAction(
                    label='衛福部急救資訊網',
                    uri='https://tw-aed.mohw.gov.tw/index.jsp'
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, button_template)

    return "OK"


# rich menu的部分
# 急救流程


def send_rescue_carousel(reply_token):
    image_carousel = TemplateSendMessage(
        alt_text="rescue",
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://imgur.com/YcqdKvq.jpg',
                    action=PostbackTemplateAction(
                        label='Step1.叫',
                        text='查看步驟1要領',
                        data='action=buy&itemid=1'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://imgur.com/DuibZrm.jpg',
                    action=PostbackTemplateAction(
                        label='Step2.叫',
                        text='查看步驟2要領',
                        data='action=buy&itemid=2'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://imgur.com/TNjtoSZ.jpg',
                    action=PostbackTemplateAction(
                        label='Step3.壓',
                        text='查看步驟3要領',
                        data='action=buy&itemid=3'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://imgur.com/Z9LJhFT.jpg',
                    action=PostbackTemplateAction(
                        label='Step4.電',
                        text='查看步驟4要領',
                        data='action=buy&itemid=4'
                    )
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, image_carousel)

    return "OK"

# 按壓指導


'''def send_press_guide_button(reply_token):
    msg = []
    msg.append(ImageSendMessage(url='https://example.com/image.jpg'))
    msg.append(TextSendMessage(text=("掌心交叉，雙手打直")))
    msg.append(TextSendMessage(text=("掌根放置病患兩乳頭中點\n")))
    msg.append(TextSendMessage(text=("請問你想探索哪一類型的急救知識呢？")))
    line_bot_api.reply_message(reply_token, msg)

    return "OK"
    '''

# fsm


def send_fsm(reply_token):
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(
            original_content_url="https://i.imgur.com/zP486SZ.png",
            preview_image_url="https://i.imgur.com/zP486SZ.png",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=LocationAction(label='Go back to menu', text='Menu'))
                ]
            )
        )
    )
    return "OK"


def test(reply_token, word):
    line_bot_api.reply_message(
        reply_token,
        TemplateSendMessage(word=TextMessage(text=word),
                            alt_text='outside_link',
                            template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='急救知識網站',
            text='還想了解更多的急救知識嗎？歡迎參考我們推薦的網站!',
            actions=[
                URITemplateAction(
                 label='安妮怎麼了',
                 text='https://www.anne.education/'
                ),
                URITemplateAction(
                    label='消防署資訊網',
                    uri='https://www.nfa.gov.tw/cht/index.php'
                ),
                URITemplateAction(
                    label='衛福部急救資訊網',
                    uri='https://tw-aed.mohw.gov.tw/index.jsp'
                )
            ]
        )

        )
    )
    return "OK"
