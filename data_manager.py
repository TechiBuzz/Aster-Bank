from database import db


class DataManager:
    def __init__(self):
        self.account = dict()

    def get_username(self):
        return self.account['USERNAME']

    def get_full_name(self):
        return self.account['FIRST_NAME'] + ' ' + self.account['LAST_NAME']

    def get_balance(self) -> float:
        return self.account['BALANCE']

    def update_balance(self, new_balance) -> None:
        self.account['BALANCE'] = new_balance
        db.execute_query('UPDATE accounts SET BALANCE = %s WHERE ID = %s',
                         (self.account['BALANCE'], self.account['ACCOUNT_ID']))

    def set_account(self, account) -> None:
        self.account = account


data_manager = DataManager()
