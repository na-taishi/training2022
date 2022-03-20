from dataclasses import dataclass,field

import PySimpleGUI as sg

from view.base import WindowBase


@dataclass
class Aggregate(WindowBase):
    '''集計画面クラス
    指定した日付の集計画面を表示するクラス。
    Args:
        rows(list(list)):表示するデータ
    '''
    name:str = "Aggregate"
    dt_str:str =None
    rows:list =field(default_factory=list)
    header:list =field(default_factory=lambda:["種別","金額"])

    # インスタンス生成時に画面を作成
    def __post_init__(self):
        self.layout = [
            [sg.Text((self.dt_str),size=(800,1),justification="center",font=(25))],
            [
            sg.Table(
            self.rows,
            headings=self.header,
            col_widths=[90,20],
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
            [sg.Button("戻る")]
            ]
        self.window = sg.Window(self.name,self.layout,size=(self.size_x,self.size_y),location=self.location)
        
    def open(self):
        while True:
            event,values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "戻る":
                self.window.close()
        self.window.close()