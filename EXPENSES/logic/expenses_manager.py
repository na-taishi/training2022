from config import status_code
from dao.startup_dao import Startup
from dao.category_dao import CategoryAccess
from dao.expenses_dao import ExpensesAccess
from dao.aggregate_dao import AggregateAccess
from dao.registration_dao import RegistrationAccess
from dto.expenses_dto import Expenses
from dto.aggregate_dto import Aggregate
from dto.registration_list_dto import RegistrationList
import event
import common

def start():
    '''初期化処理
    起動時に実行する。
    Returns:
        int:実行結果
    '''
    result = Startup.initialize()
    event.top_event.call_top(result)

def ready_categoory():
    '''費用種類取得処理
    費用種類を取得する。
    Returns:
        list:取得結果
    '''
    result = CategoryAccess.get_all_category()
    return result

def search_expenses(date_type,dt_parts):
    '''支出処理
    支出のデータを取得して、画面を表示。
    Args:
        date_type(string):年次、月次、日次
        dt_parts(list):年、月、日
    '''
    result = ExpensesAccess.get_expenses(date_type,dt_parts)
    rows = Expenses.pass_to_view(result)
    event.detail_list_event.call_detail_list(rows,dt_parts)

def search_aggregate(date_type,dt_parts):
    '''集計処理
    集計のデータを取得して、画面を表示。
    Args:
        date_type(string):年次、月次、日次
        dt_parts(list):年、月、日
    '''
    result = AggregateAccess.get_aggregate(date_type,dt_parts)
    rows = Aggregate.pass_to_view(result)
    event.aggregate_event.call_aggregate(rows,dt_parts)

def reload_expenses(dt_str):
    '''支出画面再読み込み処理
    支出データを取得する。
    Args:
        dt_str(string):日付
    Returns:
        list(list):実行結果
    '''
    dt_parts = common.date.split_date_to_number(dt_str)
    if len(dt_parts) == 1:
        date_type = "年次"
    elif len(dt_parts) == 2:
        date_type = "月次"
    elif len(dt_parts) == 3:
        date_type = "日次"
    rows = ExpensesAccess.get_expenses(date_type,dt_parts)
    if rows == status_code.RECORD_NOT_FOUND:
        result = []
    else:
        result = Expenses.pass_to_view(rows)
    return result

def add_expenses(add_list,dt_str):
    '''支出テーブルへデータ追加
    支出テーブルへデータを追加する。
    Args:
        add_list(list(tuple)):追加データ
        dt_str(string):日付
    Returns:
        int:実行結果
    '''
    dt_parts = common.date.split_date_to_number(dt_str)
    values = Expenses.pass_to_additional_db(add_list,dt_str)
    result = ExpensesAccess.add_expenses(values,dt_parts)
    return result

def update_expenses(update_list,dt_str):
    '''支出テーブルのデータ更新
    支出テーブルへデータを更新する。
    Args:
        update_list(list):更新データ
        dt_str(string):日付
    Returns:
        int:実行結果
    '''
    dt_parts = common.date.split_date_to_number(dt_str)
    result = ExpensesAccess.update_expenses(update_list,dt_parts)
    return result

def delete_expenses(delete_list,dt_str):
    '''支出テーブルへデータを追加
    支出テーブルへデータを追加。
    Args:
        aggregate(string):個別、集計
        date_type(string):年次、月次、日次
        dt_parts(list):年、月、日
    Returns:
        int:実行結果
    '''
    dt_parts = common.date.split_date_to_number(dt_str)
    result = ExpensesAccess.delete_expenses(delete_list,dt_parts)
    return result

def search_registration(date_type):
    '''登録一覧処理
    登録一覧のデータを取得して、画面を表示。
    Args:
        date_type(string):年次、月次、日次
    '''
    result = RegistrationAccess.get_registration(date_type)
    rows = RegistrationList.pass_to_view(result)
    print(rows)
    event.registration_list_event.call_registration_list(rows)