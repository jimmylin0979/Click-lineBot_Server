from transitions.extensions import GraphMachine

from utils import *  # send_text_message, send_IP12_carousel, send_fsm, send_go_to_menu_button,send_Apple_carousel, send_Menu_carousel, send_info, send_IP12_Pro_carousel, send_IP12_Mini_carousel, send_IP12_Pro_Max_carousel

import requests
from urllib.request import urlopen as uReq
# from bs4 import BeautifulSoup as soup


class TocMachine(GraphMachine):
    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            **{
                "states": [
                    'start',
                    'Menu',
                    'user_location',
                    'aed_location',
                    'self_study',

                    'not_beside_patient',
                    'call_119',

                    # aed_location
                    'return_aed_location_website',

                    # self_study 急救知識庫
                    'cpr_aed_condition',
                    'why_first_aid_important',
                    'what_is_cpr',
                    'what_is_aed',
                    'aed_steps',
                    'cpr_steps',
                    'respiration',
                    'cpr_break_bone',
                    'underwear',
                    'law',

                    'fsm',


                    # rich menu
                    # 急救流程
                    'rescue',
                    'step1',
                    'step2',
                    'step3',
                    'step4',

                    # 按壓指導
                    'press_guide',

                    'outside_link'
                    'fsm'
                ],
                "transitions": [
                    {
                        'trigger': 'advance',
                        'source': '*',
                        'dest': 'fsm',
                        'conditions': 'is_going_to_fsm'
                    },
                    {
                        'trigger': 'advance',
                        'source': '*',
                        'dest': 'Menu',
                        'conditions': 'is_going_to_Menu'
                    },

                    # menu
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'user_location',
                        'conditions': 'is_going_to_user_location'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'aed_location',
                        'conditions': 'is_going_to_aed_location'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'self_study',
                        'conditions': 'is_going_to_self_study'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'rescue',
                        'conditions': 'is_going_to_rescue'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'press_guide',
                        'conditions': 'is_going_to_press_guide'
                    },

                    # aed_location
                    {
                        'trigger': 'outside',
                        'source': 'aed_location',
                        'dest': 'return_aed_location_website',
                        'conditions': 'is_return_aed_location_website'
                    },

                    # user_location
                    {
                        'trigger': 'advance',
                        'source': 'user_location',
                        'dest': 'call_119',
                        'conditions': 'is_going_to_call_119'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'user_location',
                        'dest': 'not_beside_patient',
                        'conditions': 'is_going_to_not_beside_patient'
                    },

                    # 急救知識庫内容
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'cpr_aed_condition',
                        'conditions': 'is_going_to_cpr_aed_condition'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'why_first_aid_important',
                        'conditions': 'is_going_to_why_first_aid_important'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'what_is_cpr',
                        'conditions': 'is_going_to_what_is_cpr'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'what_is_aed',
                        'conditions': 'is_going_to_what_is_aed'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'cpr_steps',
                        'conditions': 'is_going_to_cpr_steps'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'aed_steps',
                        'conditions': 'is_going_to_aed_steps'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'respiration',
                        'conditions': 'is_going_to_respiration'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'cpe_break_bone',
                        'conditions': 'is_going_to_cpr_break_bone'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'underwear',
                        'conditions': 'is_going_to_underwear'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'self_study',
                        'dest': 'law',
                        'conditions': 'is_going_to_law'
                    },
                    {
                        'trigger': 'go_back',
                        'source': 'law',
                        'dest': 'Menu',
                        'conditions': 'is_going_to_Menu'
                    },

                    # outside_link


                    # rich menu實作部分
                    # 急救流程
                    {
                        'trigger': 'advance',
                        'source': 'rescue',
                        'dest': 'step1',
                        'conditions': 'is_going_to_step1'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'rescue',
                        'dest': 'step2',
                        'conditions': 'is_going_to_step2'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'rescue',
                        'dest': 'step3',
                        'conditions': 'is_going_to_step3'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'rescue',
                        'dest': 'step4',
                        'conditions': 'is_going_to_step4'
                    },
                ],
                "initial": 'start',
                "auto_transitions": False,
                "show_conditions": True,
            },
        )

    def is_going_to_Menu(self, event):
        text = event.message.text
        return "Menu" in text or "menu" in text

    def go_back_Menu(self, event):
        text = event.message.text
        return "Menu" in text or "menu" in text

    # menu_user_location
    def is_going_to_user_location(self, event):
        text = event.message.text
        return '呼叫定位精靈' in text

    def on_enter_user_location(self, event):
        print("I'm entering user_location")
        reply_token = event.reply_token
        send_beside_patient_button(reply_token)

    def go_back_place(self, event):
        text = event.message.text
        return "呼叫定位精靈" in text

    # 是否在患者身邊？
    def is_going_to_call_119(self, event):
        text = event.message.text
        return "呼叫119" in text

    def on_enter_call_119(self, event):
        print("I'm entering call_119")
        reply_token = event.reply_token
        send_call_button(reply_token)

    def is_going_to_not_beside_patient(self, event):
        text = event.message.text
        return "我現在不在患者身邊" in text

    def on_enter_not_beside_patient(self, event):
        print("I'm entering not_beside_patient")
        reply_token = event.reply_token
        msg = []
        msg.append(TextSendMessage(text="若你準備急救，請移動至患者身旁，再按下撥打119按鈕"))
        msg.append(TextSendMessage(text="若你準備協助取AED，請按下AED地圖按鈕"))
        line_bot_api.reply_message(reply_token, msg)

    # menu_ade_location
    def is_going_to_aed_location(self, event):
        text = event.message.text
        return "呼叫AED地圖" in text

    def is_return_aed_location_website(self, event):
        # TODO check whether the message type is LocationMessage
        return True

    def on_enter_aed_location(self, event):
        print("I'm entering aed_location")
        reply_token = event.reply_token
        msg = TextSendMessage(text="我將帶你前往最近的AED機台位置～",
                                        quick_reply=QuickReply(items=[QuickReplyButton(action=LocationAction(label="定位"))]))
        line_bot_api.reply_message(reply_token, msg)
    
    def on_enter_return_aed_location_website(self, event):
        print("I'm entering return_aed_location_website")
        '''
        {   "destination":"Uad88eda563b9e7358d5943e199951c11",
            "events":[
                {"type":"message",
                "message":{"type":"location","id":"14972484585233","latitude":24.790973,"longitude":120.995567,"address":"183、, 東區新竹市台灣 300"},
                "timestamp":1635161650017,
                "source":{"type":"user","userId":"Ubecfd1045aa5b3db8110b425bc095c33"},
                "replyToken":"153b289c957a4a1f8d1dcd23eb67e7bd","mode":"active"}]}
        '''
        reply_token = event.reply_token
        msg = TextSendMessage(text=f"https://click-server-on-heroku.herokuapp.com/AEDMap?lat={event.message.latitude}&lng={event.message.longitude}")
        line_bot_api.reply_message(reply_token, msg)

    def go_back_themepark(self, event):
        text = event.message.text
        return "呼叫AED地圖" in text

    # menu_self_study
    def is_going_to_self_study(self, event):
        text = event.message.text
        return "呼叫急救知識" in text

    def on_enter_self_study(self, event):
        print("I'm entering self_study")
        reply_token = event.reply_token
        send_self_study_carousel(reply_token)

    # 急救知識庫 -- 問題集
    def is_going_to_cpr_aed_condition(self, event):
        text = event.message.text
        return "答案1是什麽!" in text

    def on_enter_cpr_aed_condition(self, event):
        num = 1
        reply_token = event.reply_token
        word = "當你發現一個人「無意識、沒有正常呼吸、沒有脈搏」，也就是心肺功能停止時，就應該施行CPR及AED。\n\n然而評估脈搏這件事，對於沒接受過專業訓練的民眾來說並不容易，因此美國心臟醫學會建議，一般民眾只要判斷患者是否符合「無意識、沒有正常呼吸」兩個條件即可。"
        send_outsideLink_button(reply_token, word)

    def is_going_to_why_first_aid_important(self, event):
        text = event.message.text
        return "答案2是什麽!" in text

    def on_enter_why_first_aid_important(self, event):
        print("I'm entering why_first_aid_important")
        reply_token = event.reply_token
        test(reply_token, "當一個人失去心臟、肺臟的功能時，血液就無法流動，肺臟也無法進行氧氣交換，這時大腦便無法獲得血液運送的氧氣，僅存的氧氣僅能供給4-6分鐘，耗盡後大腦組織便開始壞死，超過10分鐘腦細胞將全部壞死。\n\n病患倒下的瞬間，存活率每分鐘會下降10%，唯有把握黃金的4-6分鐘，盡早進行CPR、使用AED，才有機會救活一個人，因此在救護車到達前的急救，是無可取代的。")
        #Wsend_text_message(reply_token, "當一個人失去心臟、肺臟的功能時，血液就無法流動，肺臟也無法進行氧氣交換，這時大腦便無法獲得血液運送的氧氣，僅存的氧氣僅能供給4-6分鐘，耗盡後大腦組織便開始壞死，超過10分鐘腦細胞將全部壞死。\n\n病患倒下的瞬間，存活率每分鐘會下降10%，唯有把握黃金的4-6分鐘，盡早進行CPR、使用AED，才有機會救活一個人，因此在救護車到達前的急救，是無可取代的。")

    def is_going_to_what_is_cpr(self, event):
        text = event.message.text
        return "答案3是什麽!" in text

    def on_enter_what_is_cpr(self, event):
        print("I'm entering what_is_cpr")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "一位心肺功能停止的人，心臟就沒辦法再運輸血液。操作CPR是為了取代部分的心臟功能，透過壓縮胸腔，間接的壓縮心臟，使血液可以流動，供給大腦及心臟使用，減緩腦細胞損壞。")

    def is_going_to_what_is_aed(self, event):
        text = event.message.text
        return "答案4是什麽!" in text

    def on_enter_what_is_aed(self, event):
        print("I'm entering what_is_aed")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "AED（自動體外去顫器）是一個能自動判斷心臟是否正在亂跳或顫抖的機器，如果是便會電擊，將心臟「電停」，使它重新開機，如此一來心臟有機會恢復其正常的跳動，然而若心臟已經停止跳動，或出現其他的狀況，一律不電擊。")

    def is_going_to_aed_steps(self, event):
        text = event.message.text
        return "答案5是什麽!" in text

    def on_enter_aed_steps(self, event):
        print("I'm entering aed_steps")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "AED使用主要有兩個步驟：\n1. 開啟開關\n2. 貼上貼片\n3. 插上插頭（若該AED貼片未連結機台）\n\n開機後AED會透過語音引導使用者拿出貼片，貼片上也有圖示告訴使用者，應貼在病患何處（一片貼在右側鎖骨下方皮膚，一片貼在左側乳頭側下方皮膚）及如何使用，因此不須特別記憶，依照指示就行。")

    def is_going_to_cpr_steps(self, event):
        text = event.message.text
        return "答案6是什麽!" in text

    def on_enter_cpr_steps(self, event):
        print("I'm entering cpr_steps")
        reply_token = event.reply_token
        send_text_message(reply_token, "用力壓：壓胸深度5公分以上。\n2. 快快壓：壓胸速度每分鐘100-120下（約每秒2下）。\n3. 胸回彈：每次下壓後，要使患者胸部回彈至原本厚度。\n4. 莫中斷：除非AED需進行分析，應避免CPR中斷。\n\n高品質的CPR大約可達到正常心臟的三成功能，足夠讓氧氣運送至腦部，減緩腦細胞損壞，相較沒有進行CPR的情況，存活率從每分鐘下降10%可提升至每分鐘下降3-4%。")

    def is_going_to_respiration(self, event):
        text = event.message.text
        return "答案7是什麽!" in text

    def on_enter_respiration(self, event):
        print("I'm entering respiration")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "早期民眾版CPR的確包含口對口人工呼吸的步驟，不過為了增加民眾的急救意願，及剛倒下的人腦中還有庫存的氧氣，所以目前民眾版成人CPR僅提倡胸外按壓，不強調口對口人工呼吸，但對於溺水或噎到這類呼吸道問題，或者兒童、嬰兒仍建議可以做完整的CPR，以30次胸外按壓配合兩次人工呼吸。")

    def is_going_to_cpr_break_bone(self, event):
        text = event.message.text
        return "答案8是什麽!" in text

    def on_enter_cpr_break_bone(self, event):
        print("I'm entering cpr_break_bone")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "有時候會的，不過我們的肋骨是走在一個軌道中，即便斷掉了也不會亂跑，刺傷內臟的機率也很低，而且肋骨骨折的病患大多都不需要進行手術，讓它自然癒合即可。\n\n進行CPR通常不會造成嚴重的身體傷害，然而若因猶豫而沒有施行CPR，病患存活的機率將在幾分鐘內大幅降低，因此，面對心肺功能停止的病患，積極進行CPR、提供血液循環還是當務之急。")

    def is_going_to_underwear(self, event):
        text = event.message.text
        return "答案9是什麽!" in text

    def on_enter_underwear(self, event):
        print("I'm entering underwear")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "內衣鋼圈不影響急救流程，因此也不需解開病患內衣。\n\n施行CPR可以直接隔著上衣進行按壓，而要進行AED電擊時，則建議將上衣拉起來，將AED貼片貼在皮膚，不壓到衣物即可，內衣鋼圈並不影響急救，也沒有任何狀況需要解除內衣。")

    def is_going_to_law(self, event):
        text = event.message.text
        return "答案10是什麽!" in text

    def on_enter_law(self, event):
        print("I'm entering law")
        reply_token = event.reply_token
        send_text_message(
            reply_token, "緊急醫療救護法第14-2條有提到：「救護人員以外之人，為免除他人生命之急迫危險，使用緊急救護設備或施予急救措施者，適用民法、刑法緊急避難免責之規定。救護人員於非值勤期間，前項規定亦適用之。」，也就是當有人有生命危險時，像是心肺功能停止，只要你是出於善意協助而採取一般人常識下的急救措施，可以適用緊急避難的法律而免責。")
        self.go_back(event)

    # from here to paste
    # outside_link

    def is_going_to_outside_link(self, event):
        text = event.message.text
        return "" in text

    def on_enter_outside_link(self, event):
        print("I'm entering outside_link")
        reply_token = event.reply_token
        send_outsideLink_button(reply_token)

    # rich menu 實作部分
    # 急救流程
    def is_going_to_rescue(self, event):
        text = event.message.text
        return "急救流程" in text

    def on_enter_rescue(self, event):
        print("I'm entering rescue")
        reply_token = event.reply_token
        send_rescue_carousel(reply_token)

    def is_going_to_step1(self, event):
        text = event.message.text
        return "查看步驟1要領" in text

    def on_enter_step1(self, event):
        print("I'm entering step1")
        reply_token = event.reply_token
        msg = []
        msg.append(TextSendMessage(text="雙手拍打病患雙肩，確認其是否有意識"))
        msg.append(TextSendMessage(text="若病患眼神無法注視著你，或發不出聲音，即為無意識，請進行下一步驟"))
        line_bot_api.reply_message(reply_token, msg)

    def is_going_to_step2(self, event):
        text = event.message.text
        return "查看步驟2要領" in text

    def on_enter_step2(self, event):
        print("I'm entering step2")
        reply_token = event.reply_token
        msg = []
        msg.append(TextSendMessage(text="撥打119求救，並請人去拿AED"))
        msg.append(TextSendMessage(text="並且配合119派遣員確認病患是否有正常呼吸"))
        msg.append(TextSendMessage(
            text="評估是否有正常呼吸可以透過觀察或用手去感受病患的胸腹部間有沒有起伏，評估時間不要超過10秒鐘"))
        msg.append(TextSendMessage(
            text="若發現胸腹部間沒有明顯的起伏，或是呼吸很緩慢不正常，即是沒有正常呼吸，請進行下一步驟"))
        line_bot_api.reply_message(reply_token, msg)

    def is_going_to_step3(self, event):
        text = event.message.text
        return "查看步驟3要領" in text

    def on_enter_step3(self, event):
        print("I'm entering step3")
        reply_token = event.reply_token
        msg = []
        msg.append(TextSendMessage(text="開始CPR"))
        msg.append(TextSendMessage(text="將掌心交疊、雙手打直，掌根放置病患兩乳頭中點"))
        msg.append(TextSendMessage(text="除非要使用AED，否則直至救護車抵達前請持續按壓"))
        line_bot_api.reply_message(reply_token, msg)

    def is_going_to_step4(self, event):
        text = event.message.text
        return "查看步驟4要領" in text

    def on_enter_step4(self, event):
        print("I'm entering step4")
        reply_token = event.reply_token
        msg = []
        msg.append(TextSendMessage(text="將AED開機，並依圖片指示把貼片貼在病患皮膚上"))
        msg.append(TextSendMessage(text="接著聽從AED的語音引導持續急救"))
        line_bot_api.reply_message(reply_token, msg)

    # 按壓指導

    def is_going_to_press_guide(self, event):
        text = event.message.text
        return "按壓指導" in text

    def on_enter_press_guide(self, event):
        print("I'm entering press_guide")
        reply_token = event.reply_token
        msg = []
        msg.append(ImageSendMessage(original_content_url='https://imgur.com/fLQQfgt.jpg',
                                    preview_image_url='https://imgur.com/fLQQfgt.jpg'))
        msg.append(TextSendMessage(text=("掌心交叉，雙手打直")))
        msg.append(TextSendMessage(text=("掌根放置病患兩乳頭中點\n")))
        msg.append(TextSendMessage(text=("請問你想探索哪一類型的急救知識呢？")))
        line_bot_api.reply_message(reply_token, msg)

    # fsm

    def is_going_to_fsm(self, event):
        text = event.message.text
        return "fsm" in str(text).lower()


    # on enter
    def on_enter_Menu(self, event):
        print("I'm entering menu")
        reply_token = event.reply_token
        send_Menu_button(reply_token)

    # place 他是屬於menu的部分，不需要back

    # FSM

    def on_enter_fsm(self, event):
        print("I'm entering fsm")
        reply_token = event.reply_token
        send_fsm(reply_token)
