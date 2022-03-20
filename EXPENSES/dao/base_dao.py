import sqlite3
from dataclasses import dataclass

from common.db import DataBase
from config import status_code
from config.db_conf import DB_PATH

@dataclass
class DataAccess:
    '''データアクセスの基本クラス
    各データアクセスの継承用。
    '''
    db:object = None

    def __post_init__(self):
        if self.db == None:
            self.db = DataBase(DB_PATH)

    def create_table(self,query):
        '''テーブル作成
        テーブル作成と実行結果を返す。
        Args:
            query(string):SQL文
        Returns:
            int:実行結果
        '''
        try:
            self.db.create_table(query)
            result = status_code.SUCCESS
        except sqlite3.OperationalError as e:
            result = status_code.ERROR_ALREADY_TABLE
            print(e)
        except Exception:
            result = status_code.ERROR_DB
        return result

    def insert(self,query,values):
        '''
        レコード追加と実行結果を返す。
        Args:
            query(string):SQL文
            values(tuple):挿入する値
        Returns:
            int:実行結果
        '''
        try:
            self.db.insert(query,values)
            result = status_code.SUCCESS
        except sqlite3.IntegrityError as e:
            result = status_code.ERROR_ALREADY_RECORD
        except sqlite3.OperationalError as e:
            result = status_code.ERROR_NO_TABLE
        except Exception as e:
            result = status_code.ERROR_DB
        return result

    def update(self,query,values):
        '''レコード更新
        レコード更新と実行結果を返す。
        Args:
            query(string):SQL文
            values(tuple):更新内容
        Returns:
            int:更新結果
        '''
        try:
            self.db.update(query,values)
            result = status_code.SUCCESS
        except sqlite3.OperationalError as e:
            result = status_code.ERROR_NO_RECORD
        except Exception as e:
            result = status_code.ERROR_DB
        return result

    def delete(self,query,value):
        '''レコード削除
        レコード削除と実行結果を返す。
        Args:
            query(string):SQL文
            value(tuple):削除対象
        Returns:
            int:削除結果
        '''
        try:
            self.db.delete(query,value)
            result = status_code.SUCCESS
        except sqlite3.OperationalError as e:
            result = status_code.ERROR_NO_RECORD
        except Exception as e:
            result = status_code.ERROR_DB
        return result

    def select(self,query,*values):
        '''レコード取得
        レコード取得と実行結果を返す。
        Args:
            query(string):SQL文
            values(tuple):取得対象(引数なしも可能)
        Returns:
            int or list:取得結果(エラー時はint型)
        '''
        try:
            if not values:
                result = self.db.select(query)
            else:
                result = self.db.select(query,*values)
            status = result
        except sqlite3.OperationalError as e:
            status = status_code.ERROR_NO_TABLE
        return status