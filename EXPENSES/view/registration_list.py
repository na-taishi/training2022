from dataclasses import dataclass,field

import PySimpleGUI as sg

from view.base import WindowBase
from event import registration_list_event as event_list


@dataclass
class RegistrationList(WindowBase):
    '''登録一覧画面クラス
    登録したデータの日付一覧画面を表示するクラス。
    Args:
        rows(list(list)):表示するデータ(DBから取得したレコードの列数は4つ)
    '''
    name:str = "RegistrationList"
    rows:list =field(default_factory=list)
    header:list =field(default_factory=lambda:["日付"])
    typebox:list =field(default_factory=list)

    def __post_init__(self):
        self.layout = [
            [
            sg.Table(
            self.rows,
            headings=self.header,
            col_widths=[50],
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
            [sg.Button("検索"),sg.Button("戻る")
            ]
            ]
        self.window = sg.Window(self.name,self.layout,size=(self.size_x,self.size_y),location=self.location)
        

    def open(self):
        while True:
            event,values = self.window.read()
            if event == sg.WIN_CLOSED or event == "戻る":
                break
            elif event == "検索":
                selected = values["table"][0]
                row = self.rows[selected]
                event_list.search_bt(row)
        self.window.close()