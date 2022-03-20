from dataclasses import dataclass


import common

@dataclass
class Aggregate:
    '''支出テーブル(集計)の変換クラス(年次、月次、日次)
    データを変換する。
    '''
    category_name:str
    total:int
    
    def convert_view(self):
        '''フロント表示データ変換
        支出データをフロント表示データに変換する。
        Returns:
            list:変換後レコード
        '''
        result = [self.category_name,self.total]
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
            aggregate = Aggregate(category_name = row[0],total = row[1])
            result.append(aggregate.convert_view())
        return result
        