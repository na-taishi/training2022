from dataclasses import dataclass,field

import PySimpleGUI as sg

from config import view_conf


@dataclass
class WindowBase:
    name:str
    size_x:int = view_conf.SIZE_X
    size_y:int = view_conf.SIZE_Y
    layout:list = field(default_factory=list)
    window = None
    location:tuple = view_conf.BOOT_POSITION
    sg.theme(view_conf.BACK_COLOR) 

    def __post_init__(self):
        self.window = sg.Window(self.name, self.layout,size=(self.size_x,self.size_y),location=self.location)

    def popup_success(self,text):
        sg.popup_ok(text,location=self.location,font=(view_conf.POPUP_FONT_X,view_conf.POPUP_FONT_Y))

    def popup_error(self,title,text):
        sg.popup(text,title=title,location=self.location,font=(view_conf.POPUP_FONT_X,view_conf.POPUP_FONT_Y))