import common
from view.aggregate import Aggregate

def call_aggregate(rows,dt_parts):
    '''集計画面起動
    集計画面を呼び出す。
    Args:
        rows(list(tuple)):表示するレコード
        dt_parts(list):日付の部品
    '''
    dt_str = common.date.make_date_string(dt_parts)
    aggregate = Aggregate(rows=rows,dt_str=dt_str)
    aggregate.open()