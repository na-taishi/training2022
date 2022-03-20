from dataclasses import dataclass

from dao.base_dao import DataAccess
from sql import category as sql_category

@dataclass
class CategoryAccess(DataAccess):
    '''費用種別テーブルのアクセスクラス
    費用種別テーブルを操作する。
    '''

    # 未使用
    def add_category(self,name):
        '''費用種別追加
        費用種別を追加する。
        Args:
            name(string):費用種別名
        Returns:
            int:実行結果
        '''
        query = sql_category.category_addition
        value = (name,)
        result = self.insert(query,value)
        return result

    # 未使用
    def get_id(self,name):
        '''ID取得
        IDを取得する。
        Args:
            name(string):費用種別名
        Returns:
            int:取得結果
        '''
        query = sql_category.id_fetch
        result = self.select(query,name)
        return result[0][0]

    @staticmethod
    def get_all_category():
        '''全取得
        全レコードを取得する。
        Returns:
            list:取得結果
        '''
        category = CategoryAccess()
        query = sql_category.all_name_fetch
        result = category.select(query)
        return result