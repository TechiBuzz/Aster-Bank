from PIL import Image

from util.database import db
from util.image_util import image_to_bytes


class AccountManager:
    def __init__(self):
        self.account = dict()

    def get(self, value: str):
        try:
            return self.account[value]
        except KeyError:
            return None

    def get_profile_pic(self) -> bytes | None:
        try:
            if self.account['IMAGE'] is not None:
                return self.account['IMAGE']
        except KeyError:
            return None

    def set_profile_pic(self, image: Image) -> None:
        self.account['IMAGE'] = image_to_bytes(image) if image else None

    def get_username(self) -> str | None:
        try:
            return self.account['USERNAME']
        except KeyError:
            return None

    def get_full_name(self) -> str | None:
        try:
            return self.account['FIRST_NAME'] + ' ' + self.account['LAST_NAME']
        except KeyError:
            return None

    def get_balance(self) -> float | None:
        try:
            return self.account['BALANCE']
        except KeyError:
            return None

    def update_balance(self, new_balance) -> None:
        self.account['BALANCE'] = new_balance
        db.execute_query('UPDATE accounts SET BALANCE = %s WHERE ID = %s',
                         (self.account['BALANCE'], self.account['ID']))

    def set_account(self, account) -> None:
        self.account = account

account_manager = AccountManager()
