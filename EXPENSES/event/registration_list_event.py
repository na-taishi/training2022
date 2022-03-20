import common
from logic import expenses_manager
from view import registration_list 


def call_registration_list(rows):
    '''登録一覧画面起動
    登録一覧画面を呼び出す。
    Args:
        rows(list(tuple)):表示するレコード
    '''
    registrations = registration_list.RegistrationList(rows=rows)
    registrations.open()

def search_bt(row):
    '''
    検索ボタン押下時の処理。
    Args:
        row(list):選択内容
    Returns:
        int:実行結果
    '''
    dt_parts = common.date.split_date_to_number(row)
    if len(dt_parts) == 3:
        date_type = "日次"
    elif len(dt_parts) == 2:
        date_type = "月次"
    elif len(dt_parts) == 1:
        date_type = "年次"
    status = expenses_manager.search_expenses(date_type,dt_parts)
    return status