from dataclasses import dataclass


@dataclass
class RegistrationList:
    '''支出テーブルの変換クラス(年次、月次、日次)
    データを変換する。
    '''
    year:int = None
    month:int = None
    day:int = None
    

    def convert_view(self):
        '''フロント表示データ変換
        支出データをフロント表示データに変換する。
        Returns:
            string:変換後レコード
        '''
        if self.day:
            result = str(self.year) + "年" + str(self.month) + "月" + str(self.day) + "日"
        elif self.month:
            result = str(self.year) + "年" + str(self.month)
        elif self.year:
            result = str(self.year) + "年"
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
            registration = RegistrationList(*row)
            result.append(registration.convert_view())
        return result