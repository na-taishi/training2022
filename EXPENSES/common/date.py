import datetime
import re

def check_converting_date(*args):
    '''
    日付に変換できるか確認。
    Args:
        args(tuple):日付に変換する数値
    Returns:
        result(int):0(変換できる)、1(変換できない)を返す
    '''
    if len(args) == 1:
        args += (1,1)
    elif len(args) == 2:
        args += (1,)
    try:
        check_data = [int(arg) for arg in args ]
        datetime.date(*check_data)
        result = 0
    except Exception as e:
        result = 1
    return result

def split_date_to_number(date):
    '''
    日付(文字列)を数値に分割。
    Args:
        date(string):日付
    Returns:
        result(list):分割された数値
    '''
    parts = re.split("[年月日-]",date)
    result = [int(part) for part in parts if part != ""]
    return result

def make_date_string(dt_parts):
    '''
    日付(文字列)を作成する。
    Args:
        dt_parts(list):日付の部品
    Returns:
        dt_str(string):作成した日付
    '''
    if len(dt_parts) == 3:
        dt_str = "{}年{}月{}日".format(*dt_parts)
    elif len(dt_parts) == 2:
        dt_str = "{}年{}月".format(*dt_parts)
    elif len(dt_parts) == 1:
        dt_str = "{}年".format(*dt_parts)
    return dt_str