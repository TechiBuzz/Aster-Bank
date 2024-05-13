from settings import *
from gui.screens.welcome_screen import WelcomeScreen
from gui.screens.main_screen import MainScreen
from gui.screens.login_screen import LoginScreen
from gui.screens.sign_up_screen import SignUpScreen
from gui.screens.account_management.profile_management import ProfileManagementScreen
from gui.screens.account_management.fund_management_screen import FundManagementScreen
from gui.screens.account_management.transfer_screen import TransferMoneyScreen
from gui.screens.account_management.request_money_screen import RequestMoneyScreen
from gui.screens.account_management.bills_screen import BillManagementScreen
from gui.screens.account_management.fd_calculator_screen import FDCalculatorScreen
from gui.screens.account_management.transaction_history_screen import TransactionHistoryScreen

import mysql.connector
import customtkinter as ctk

# Color Theme Of App
try:
    ctk.set_default_color_theme(APP_COLOR_THEME)
except:
    pass


class TsarBank(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Database Connection
        self.db_connection = get_db_connection()

        # Screens
        self.gui_instances = {
            'WelcomeScreen': WelcomeScreen(self),
            'LoginScreen': LoginScreen(self),
            'SignUpScreen': SignUpScreen(self),
            'MainScreen': MainScreen(self),
            'ProfileManagementScreen': ProfileManagementScreen(self),
            'FundManagementScreen': FundManagementScreen(self),
            'TransferMoneyScreen': TransferMoneyScreen(self),
            'RequestMoneyScreen': RequestMoneyScreen(self),
            'BillManagementScreen': BillManagementScreen(self),
            'FDCalculatorScreen': FDCalculatorScreen(self),
            'TransactionHistoryScreen': TransactionHistoryScreen(self)
        }

        # TODO -> change back to WelcomeScreen after testing!!!!!!!!!!!!
        self.show_window('MainScreen')  # show login screen at start

    def show_window(self, window_to_show: str, window_to_clear: str = None):
        window_to_show = self.gui_instances[window_to_show]
        window_to_show.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        window_to_show.tkraise()

        if window_to_clear:
            window_to_clear = self.gui_instances[window_to_clear]

            # Clear all entry fields
            for field in window_to_clear.entry_fields:
                if field.widgetName == 'TextBox':
                    field.delete('0.0', 'end')
                else:
                    field.delete(0, 'end')

            # Clear warning label
            if window_to_clear.warning_label:
                window_to_clear.warning_label.clear_warning()

            # Place forget frame
            window_to_clear.place_forget()


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB['HOST'],
            database=DB['DATABASE'],
            port=DB['PORT'],
            user=DB['USER'],
            password=DB['PASSWORD']
        )
    except:
        connection = None
        print("Unable to connect to database!")
    return connection


def main():
    app = TsarBank()

    # Window Config
    app.title(WINDOW_TITLE)

    app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
    app.minsize(1100, 700)

    app.iconbitmap(WINDOW_BITMAP_ICON_PATH)

    app.mainloop()


if __name__ == '__main__':
    main()
