from dataclasses import dataclass


import common

@dataclass
class Expenses:
    '''支出テーブルの変換クラス(年次、月次、日次)
    データを変換する。
    '''
    expenses_name:str
    payment:str
    expenses_id:int = None
    category_id:int = None
    category_name:str = None
    year:int = None
    month:int = None
    day:int = None
    

    def convert_view(self):
        '''フロント表示データ変換
        支出データをフロント表示データに変換する。
        Returns:
            list:変換後レコード
        '''
        result = [self.expenses_name,self.payment,self.category_name,self.expenses_id]
        return result

    def convert_insert(self):
        '''インサートデータ変換
        支出データをインサート処理時に使うデータに変換する。
        Returns:
            tuple:変換後レコード
        '''
        if self.day != None:
            result = (self.expenses_name,self.payment,self.year,self.month,self.day,self.category_name)
        elif self.month != None:
            result = (self.expenses_name,self.payment,self.year,self.month,self.category_name)
        else:
            result = (self.expenses_name,self.payment,self.year,self.category_name)
        return result

    @staticmethod
    def pass_to_view(rows):
        '''フロント表示データ変換
        DB取得データをフロント表示データに変換する。
        Args:
            rows(list(tuple)):取得データ
        Returns:
            list(list):変換後取得データ
        '''
        result = []
        for row in rows:
            expenses = Expenses(expenses_id = row[0],expenses_name = row[1],payment = row[2],category_name = row[3])
            result.append(expenses.convert_view())
        return result
        
    @staticmethod
    def pass_to_additional_db(rows,dt_str):
        '''db追加データ変換
        view追加データをDB登録用データに変換する。
        Args:
            rows(list(tuple)):追加データ
        Returns:
            list(list):変換後データ
        '''
        dt_parts = common.date.split_date_to_number(dt_str)
        result = []
        for row in rows:
            if len(dt_parts) == 3:
                expenses = Expenses(expenses_name = row[0],payment = row[1],category_name = row[2],year = dt_parts[0],month = dt_parts[1],day = dt_parts[2])
            elif len(dt_parts) == 2:
                expenses = Expenses(expenses_name = row[0],payment = row[1],category_name = row[2],year = dt_parts[0],month = dt_parts[1])
            elif len(dt_parts) == 1:
                expenses = Expenses(expenses_name = row[0],payment = row[1],category_name = row[2],year = dt_parts[0])
            result.append(expenses.convert_insert())
        return result