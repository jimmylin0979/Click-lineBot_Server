from transitions.extensions import GraphMachine

from app import *  # send_text_message, send_IP12_carousel, send_fsm, send_go_to_menu_button,send_Apple_carousel, send_Menu_carousel, send_info, send_IP12_Pro_carousel, send_IP12_Mini_carousel, send_IP12_Pro_Max_carousel

import requests
from urllib.request import urlopen as uReq
#from bs4 import BeautifulSoup as soup


class TocMachine(GraphMachine):
    def __init__(self):
        self.machine = GraphMachine(
            model=self,
            **{
                "states": [
                    'start',
                    'Menu',
                    'user_location',
                    'self_study',

                    # user location 有人昏迷了！我該怎麼辦
                    'beside_patient',
                    'call_119',
                    'no_beside'

                    # 急救流程
                    'step1_call',
                    'step2-119',
                    'step3_press',
                    'step4_electric',

                    # 按壓指導
                    'press_tutorial'

                    # 最近的AED在哪裏
                    # AED地圖
                    'ade_map'

                    # self_study 急救知識庫
                    'knowledge_menu',
                    'cpr_aed_condition',
                    'why_first_aid_important',
                    'what_is_cpr',
                    'what_is_aed',
                    'aed_steps',
                    'cpr_steps',
                    'respiration',
                    'cpr_break_bone',
                    'underwear',
                    'law'

                    # 急救知識網站
                    'link_help_menu'
                    'link_anny',
                    'link_fire_agency',
                    'link_healthcare',


                ],
                "transitions": [
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
                    # 最近的AED在哪裏
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'aed_map',
                        'conditions': 'is_going_to_aed_location'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'self_study',
                        'conditions': 'is_going_to_self_study'
                    },

                    # 有人暈倒了我該怎麽辦
                    {
                        'trigger': 'advance',
                        'source': 'user_location',
                        'dest': 'beside_patient',
                        'conditions': 'is_going_to_beside_patient'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'user_location',
                        'dest': 'call_119',
                        'conditions': 'is_going_to_call_119'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'user_location',
                        'dest': 'no_beside',
                        'conditions': 'is_going_to_no_beside'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'Menu',
                        'dest': 'aed_map',
                        'conditions': 'is_going_to_aed_map'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'themepark',
                        'dest': 'legoland',
                        'conditions': 'is_going_to_legoland'
                    },

                    # 我想學習急救知識
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
                        'conditions': 'is_going_to_whats_is_aed'
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

                    # 急救知識網站
                    {
                        'trigger': 'advance',
                        'source': 'law',
                        'dest': 'link_help_menu',
                        'conditions': 'is_going_to_link_help_menu'
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

    # menu_place
