from dataclasses import dataclass

from dao.base_dao import DataAccess
from sql import registration_list as sql_registration

@dataclass
class RegistrationAccess(DataAccess):
    '''登録一覧のアクセスクラス
    登録一覧を操作する。
    '''

    @staticmethod
    def get_registration(date_type):
        '''登録一覧取得
        登録一覧を選択する。
        Args:
            date_type(string):日次、月次、年次
        Returns:
            list:取得内容
        '''
        registration = RegistrationAccess()
        if date_type == "日次":
            query = sql_registration.date_list_daily
        elif date_type == "月次":
            query = sql_registration.date_list_monthly
        elif date_type == "年次":
            query = sql_registration.date_list_yearly
        result = registration.select(query)
        registration.db.close()
        return result