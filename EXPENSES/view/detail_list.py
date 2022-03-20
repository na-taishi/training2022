from ctypes.wintypes import MSG
import datetime
from dataclasses import dataclass,field

import PySimpleGUI as sg

from view.base import WindowBase
from event import detail_list_event as event_list
from config import status_code
from config.message import MESSAGE as MSG
from config.message import POPUP as POP


@dataclass
class DetailList(WindowBase):
    '''詳細一覧画面クラス
    指定した日付画面を表示するクラス。
    Args:
        rows(list(list)):表示するデータ(DBから取得したレコードの列数は4つ)
    '''
    name:str = "LIST"
    dt_str:str =datetime.date.today().strftime("%Y年%m月%d日")
    rows:list =field(default_factory=list)
    header:list =field(default_factory=lambda:["名前","金額","種別"])
    typebox:list =field(default_factory=list)

    def __post_init__(self):
        self.layout = [
            [sg.Text((self.dt_str),size=(800,1),justification="center",font=(25))],
            [
            sg.Table(
            self.rows,
            headings=self.header,
            col_widths=[45,20,20],
            auto_size_columns=False,
            justification="left",
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            num_rows=None,
            text_color="#000000",
            background_color="#cccccc",
            alternating_row_color="#ffffff",
            header_text_color="#0000ff",
            header_background_color="#cccccc",
            key="table"
            )],
            [
                sg.Text(("更新内容："),size=(10,1)),
                sg.Input("",key="name",size=(20,1)),
                sg.Input("",key="payment",size=(10,1)),
                sg.Combo(self.typebox,default_value=self.typebox[0] ,size=(10,1),key="typebox"),
                sg.Button("変更"),
                sg.Button("追加"),
                sg.Button("削除")
            ],
            [sg.Button("保存"),sg.Button("戻る")
            ]
            ]
        self.window = sg.Window(self.name,self.layout,size=(self.size_x,self.size_y),location=self.location)
        

    def open(self):
        # 参照渡しを回避するため
        transaction_log = list(self.rows)
        # 追加、更新処理との衝突をさせないために、transaction_logと別にする
        delete_log = []
        while True:
            event,values = self.window.read()
            if event == sg.WIN_CLOSED or event == "戻る":
                break
            elif event == "保存":
                result = event_list.save_bt(self.window,transaction_log,delete_log,self.rows,self.dt_str)
                if result == status_code.SUCCESS:
                    self.popup_success(MSG[result])
                else:
                    self.popup_error(POP[result],MSG[result])
            elif event == "追加" and values["name"] and values["payment"].isdigit():
                event_list.add_bt(self.window,values,self.rows,transaction_log)
            elif values["table"]:
                selected = values["table"][0]
                if event == "変更" and values["payment"].isdigit():
                    event_list.update_bt(self.window,values,self.rows,selected,transaction_log)
                elif event == "削除":
                    event_list.delete_bt(self.window,self.rows,selected,transaction_log,delete_log)
        self.window.close()