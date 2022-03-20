import common
import logic
from config import status_code
from view.top import Top


def call_top(status):
    '''費用種類用意
    費用種類を用意する。
    Args:
        status(int):初期化処理の成否
    '''   
    if status == status_code.SUCCESS:
        top = Top()
        top.open()

def search_bt(values):
    '''
    TOP画面の検索ボタン押下時の処理。
    Args:
        values(dict):入力内容
    Returns:
        int:実行結果
    '''
    # 入力チェック
    status = status_code.SUCCESS
    if values["date_type"] == "日次":
        dt_parts = (int(values["year"]),int(values["month"]),int(values["day"]))
    elif values["date_type"] == "月次":
        dt_parts = (int(values["year"]),int(values["month"]))
    elif values["date_type"] == "年次":
        dt_parts = (int(values["year"]),)   
    if status == status_code.SUCCESS:
        input_flg = common.date.check_converting_date(*dt_parts)
    # 画面呼び出し
    if input_flg == status_code.SUCCESS:
        if values["aggregate"] == "個別":
            status = logic.expenses_manager.search_expenses(values["date_type"],dt_parts)
        elif values["aggregate"] == "集計":
            status = logic.expenses_manager.search_aggregate(values["date_type"],dt_parts)
    else:
        status = status_code.ERROR_INPUT_VALUE
    return status

def registration_list_bt(values):
    '''
    登録一覧ボタン押下時の処理。
    Args:
        values(dict):入力内容
    Returns:
        int:実行結果
    '''
    if values["date_type"] == "日次":
        dt_parts = (int(values["year"]),int(values["month"]),int(values["day"]))
    elif values["date_type"] == "月次":
        dt_parts = (int(values["year"]),int(values["month"]))
    elif values["date_type"] == "年次":
        dt_parts = (int(values["year"]),) 
    status = logic.expenses_manager.search_registration(values["date_type"])
    return status