import datetime
from dataclasses import dataclass,field

import PySimpleGUI as sg

from view.base import WindowBase
from event import top_event as event_top
from config.message import MESSAGE as MSG
from config.message import POPUP as POP
from config import status_code



@dataclass
class Top(WindowBase):
    '''検索画面クラス
    日付検索画面を表示するクラス。
    '''
    name:str = "TOP"
    aggbox = ["個別","集計"]
    datebox = ["日次","月次","年次"]
    today = datetime.date.today()
    layout:list = field(default_factory=lambda:[
                [sg.Text(("集計:"),size=(15,1)),sg.Combo(Top.aggbox,default_value=Top.aggbox[0] ,size=(4,1),key="aggregate")],
                [sg.Text(("絞り込み条件:"),size=(15,1)),sg.Combo(Top.datebox,default_value=Top.datebox[0] ,size=(4,1),key="date_type")],
                [sg.Text(("日付:"),size=(15,1)),sg.Input((Top.today.year),key="year",size=(4,1)),sg.Text(("年")),sg.Input((Top.today.month),key="month",size=(2,1)),sg.Text(("月")),sg.Input((Top.today.day),key="day",size=(2,1)),sg.Text(("日")) ],
                [sg.Button("検索"), sg.Button("登録一覧"), sg.Button('キャンセル')]
                ]
    )

    def open(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'キャンセル':
                break
            elif event == "検索":
                result = event_top.search_bt(values)
                if result == status_code.ERROR_NO_TABLE:
                    self.popup_error(POP[result],MSG[result])
            elif event == "登録一覧":
                result = event_top.registration_list_bt(values)
        self.window.close()
