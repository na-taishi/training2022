import sqlite3
from dataclasses import dataclass 


@dataclass
class DataBase:
    '''DBクラス
    DBを操作するクラス。
    Args:
        path(string):DBファイルパス
    '''
    path:str

    def __post_init__(self):
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def comit(self):
        self.conn.commit()
        self.close()

    def rollback(self):
        self.conn.rollback()
        self.close()

    def create_table(self,query):
        '''
        テーブル作成。
        Args:
            query(string):SQL文
        '''
        self.cur.execute(query)

    def insert(self,query,values):
        '''
        レコードを追加。
        Args:
            query(string):SQL文
            values(tuple):挿入する値
        '''
        self.cur.execute(query,values)

    def update(self,query,values):
        '''
        レコードの更新。
        Args:
            query(string):SQL文
            values(tuple):更新内容
        '''
        self.cur.execute(query,values)

    def delete(self,query,values):
        '''
        レコードの削除。
        Args:
            query(string):SQL文
            values(tuple):削除対象
        '''
        self.cur.execute(query,values)

    def select(self,query,*values):
        '''
        レコードの取得。
        Args:
            query(string):SQL文
            values(tuple):取得対象(引数なしも可能)
        Returns:
            list:取得結果
        '''
        result = []
        if not values:
            self.cur.execute(query)
        else:
            self.cur.execute(query,values)
        for row in self.cur:
            result.append(row)
        return result