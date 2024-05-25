from util.database import db
from PIL import Image
from util.profile_picture import image_to_bytes, bytes_to_ctk_image
from customtkinter import CTkImage


class DataManager:
    def __init__(self):
        self.account = dict()

    def get_profile_pic(self) -> CTkImage | None:
        if self.account['IMAGE']:
            return bytes_to_ctk_image(self.account['IMAGE'])
        else:
            return None

    def set_profile_pic(self, image: Image) -> None:
        self.account['IMAGE'] = image_to_bytes(image)

    def get_username(self) -> str:
        return self.account['USERNAME']

    def get_full_name(self) -> str:
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
