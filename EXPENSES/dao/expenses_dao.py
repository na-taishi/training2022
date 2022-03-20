from dataclasses import dataclass

from config import status_code
from dao.base_dao import DataAccess
from sql import expenses as sql_expenses

@dataclass
class ExpensesAccess(DataAccess):
    '''支出のアクセスクラス
    支出を操作する。
    '''

    @staticmethod
    def get_expenses(date_type,dt_parts):
        '''支出取得
        支出の取得先を選択する。
        Args:
            date_type(string):日次、月次、年次
            dt_parts(list):日付
        Returns:
            list:取得内容
        '''
        expenses = ExpensesAccess()
        if date_type == "日次":
            query = sql_expenses.daily_fetch_to_front
        elif date_type == "月次":
            query = sql_expenses.monthly_fetch_to_front
        elif date_type == "年次":
            query = sql_expenses.yearly_fetch_to_front
        result = expenses.select(query,*dt_parts)
        expenses.db.close()
        return result

    @staticmethod
    def add_expenses(values,dt_parts):
        '''支出追加
        支出を追加する。
        Args:
            values(list(tuple)):追加するデータ
            dt_parts(list):日付
        Returns:
            int:実行結果
        '''
        expenses = ExpensesAccess()
        if len(dt_parts) == 3:
            query = sql_expenses.daily_addition
        elif len(dt_parts) == 2:
            query = sql_expenses.monthly_addition
        elif len(dt_parts) == 1:
            query = sql_expenses.yearly_addition

        result = status_code.SUCCESS
        for value in values:
            print(value)
            result = expenses.insert(query,value)
            if result != status_code.SUCCESS:
                break

        if result == status_code.SUCCESS:
            expenses.db.comit()
        else:
            expenses.db.rollback()
        return result

    @staticmethod
    def update_expenses(values,dt_parts):
        '''支出更新
        支出を更新する。
        Args:
            values(list(tuple)):更新するデータ
            dt_parts(list):日付
        Returns:
            int:実行結果
        '''
        expenses = ExpensesAccess()
        if len(dt_parts) == 3:
            query = sql_expenses.daily_update
        elif len(dt_parts) == 2:
            query = sql_expenses.monthly_update
        elif len(dt_parts) == 1:
            query = sql_expenses.yearly_update

        result = status_code.SUCCESS
        for value in values:
            result = expenses.update(query,value)
            if result != status_code.SUCCESS:
                break

        if result == status_code.SUCCESS:
            expenses.db.comit()
        else:
            expenses.db.rollback()
        return result

    @staticmethod
    def delete_expenses(values,dt_parts):
        '''支出削除
        支出を削除する。
        Args:
            values(list(tuple)):削除するデータ
            dt_parts(list):日付
        Returns:
            int:実行結果
        '''
        expenses = ExpensesAccess()
        if len(dt_parts) == 3:
            query = sql_expenses.daily_delete
        elif len(dt_parts) == 2:
            query = sql_expenses.monthly_delete
        elif len(dt_parts) == 1:
            query = sql_expenses.yearly_delete

        result = status_code.SUCCESS
        for value in values:
            result = expenses.delete(query,value)
            if result != status_code.SUCCESS:
                break

        if result == status_code.SUCCESS:
            expenses.db.comit()
        else:
            expenses.db.rollback()
        return result