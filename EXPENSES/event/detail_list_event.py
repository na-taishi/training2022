import logic
import common
from config import status_code
from view import detail_list 
from logic import expenses_manager

def call_detail_list(rows,dt_parts):
    '''支出画面起動
    支出画面を呼び出す。
    Args:
        rows(list(tuple)):表示するレコード
        dt_parts(list):日付の部品
    '''
    category_list  = expenses_manager.ready_categoory()
    dt_str = common.date.make_date_string(dt_parts)
    detail = detail_list.DetailList(rows=rows,typebox=category_list,dt_str=dt_str)
    detail.open()


def save_bt(window,transaction_log,delete_log,rows,dt_str):
    '''保存ボタン
    更新内容をDBに保存して、画面をリロードする処理
    Args:
        window(object):画面オブジェクト
        transaction_log(list(dict)):更新履歴を入れる
        delete_log(list):削除履歴
        rows(list(list)):画面に表示する内容
        dt_str(string):日付
    Returns:
        list:取得結果
    '''
    # DBに保存する処理
    for log in delete_log:
        transaction_log.append(log)
    for row in rows:
        if row in transaction_log:
            transaction_log.remove(row)
    add_list = []
    update_list = []
    delete_list = []
    for dic in transaction_log:
        for key,value in dic.items():
            print(value)
            if key == "add":
                add_list.append(value)
            elif key == "update":
                update_list.append(value)
            elif key == "delete":
                delete_list.append(value)
    addition_status = logic.expenses_manager.add_expenses(add_list,dt_str)
    update_status = logic.expenses_manager.update_expenses(update_list,dt_str)
    delete_status = logic.expenses_manager.delete_expenses(delete_list,dt_str)
    if addition_status != status_code.SUCCESS:
        result = addition_status
    elif update_status != status_code.SUCCESS:
        result = update_status
    elif delete_status != status_code.SUCCESS:
        result = delete_status
    else:
        result = status_code.SUCCESS
    if transaction_log:
        transaction_log.clear()
        delete_log.clear()
    # 表示画面の更新
    rows = expenses_manager.reload_expenses(dt_str)
    window["table"].update(values=rows)
    return result

def add_bt(window,values,rows,transaction_log):
    '''追加ボタン
    画面にデータを追加する処理。
    Args:
        window(object):画面オブジェクト
        values(dict):画面に入力した内容
        rows(list(list)):画面に表示する内容
        transaction_log(list(dict)):更新履歴
    '''
    add_data = (values["name"],values["payment"],values["typebox"][0])
    rows.append(add_data)
    window["table"].update(values=rows)
    transaction_log.append({"add":add_data})

def update_bt(window,values,rows,selected,transaction_log):
    '''変更ボタン
    画面の表示データを変更する処理。
    Args:
        window(object):画面オブジェクト
        values(dict):画面に入力した内容
        rows(list(list)):画面に表示する内容
        selected(int):選択した行番号(0スタート)
        transaction_log(list(dict)):更新履歴
    '''
    if len(rows[selected]) > 3:
        # DBに存在するデータの変更
        id = rows[selected][3]
        update_data = (values["name"],values["payment"],values["typebox"][0],id)
        transaction_log[selected] = {"update":update_data}
    else:
        # DBに存在しないデータの変更
        update_data = (values["name"],values["payment"],values["typebox"][0])
        if len(transaction_log) >= selected:
            transaction_log[selected] = {"add":update_data}
    rows[selected] = update_data
    window["table"].update(values=rows)

def delete_bt(window,rows,selected,transaction_log,delete_log):
    '''削除ボタン
    画面の表示データを削除する処理。
    Args:
        window(object):画面オブジェクト
        rows(list(list)):画面に表示する内容
        selected(int):選択した行番号(0スタート)
        transaction_log(list(dict)):更新履歴を入れる
        delete_log(list):削除履歴
    '''
    # DBに登録されていないデータは追加しない
    if len(rows[selected]) > 3:
        delete_data = (rows[selected][3],)
        delete_log.append({"delete":delete_data})
    if len(transaction_log) >= selected:
        del transaction_log[selected]
    del rows[selected]
    window["table"].update(values=rows)