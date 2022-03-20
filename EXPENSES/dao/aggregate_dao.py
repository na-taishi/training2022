from dataclasses import dataclass

from dao.base_dao import DataAccess
from sql import aggregate as sql_aggregate

@dataclass
class AggregateAccess(DataAccess):
    '''集計のアクセスクラス
    集計を操作する。
    '''

    @staticmethod
    def get_aggregate(date_type,dt_parts):
        '''集計取得
        集計の取得先を選択する。
        Args:
            date_type(string):日次、月次、年次
            dt_parts(tuple):日付
        Returns:
            list:取得内容
        '''
        aggregate = AggregateAccess()
        if date_type == "日次":
            query = sql_aggregate.daily_fetch_to_front
        elif date_type == "月次":
            query = sql_aggregate.monthly_fetch_to_front
        elif date_type == "年次":
            query = sql_aggregate.yearly_fetch_to_front
        result = aggregate.select(query,*dt_parts)
        aggregate.db.close()
        return result