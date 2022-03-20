from dataclasses import dataclass

from dao.base_dao import DataAccess
from sql import creation_table as creation
from sql import category
from config import status_code
from config.db_conf import CATEGORY_CONF


@dataclass
class Startup(DataAccess):
    '''起動クラス
    アプリを起動時に実行する。
    '''

    def create_tables(self):
        '''テーブル作成
        テーブルを作成する。
        Returns:
            int:実行結果
        '''
        query_list = [
            creation.category,
            creation.expenses_daily,
            creation.expenses_monthly,
            creation.expenses_yearly
        ]
        for query in query_list:
            result = self.create_table(query)
            if result == status_code.ERROR_DB:
                break
        return result

    def prepare_category(self):
        '''費用種類用意
        費用種類を用意する。
        Returns:
            int:実行結果
        '''      
        for name in CATEGORY_CONF:
            query = category.category_addition
            value = (name,)
            result = self.insert(query,value)
            if result == status_code.ERROR_DB or result == status_code.ERROR_NO_TABLE:
                result = status_code.ERROR_DB
                break
        return result
    
    @staticmethod
    def initialize():
        '''初期化処理
        アプリに必要なデータを用意する。
        Returns:
            int:実行結果
        '''   
        startup = Startup()
        table_result = startup.create_tables()
        result = status_code.BOOT_FAILURE
        if table_result == status_code.SUCCESS or table_result == status_code.ERROR_ALREADY_TABLE:
            category_result = startup.prepare_category()
            if category_result == status_code.SUCCESS or category_result == status_code.ERROR_ALREADY_RECORD:
                result = status_code.SUCCESS
                startup.db.comit()
        if result != status_code.SUCCESS:
            startup.db.rollback()
        return result
