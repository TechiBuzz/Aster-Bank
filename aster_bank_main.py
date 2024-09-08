from settings import *
from util.database import db
from gui.screens.welcome import WelcomeScreen
from gui.screens.main import MainScreen
from gui.screens.login import LoginScreen
from gui.screens.sign_up import SignUpScreen
from gui.screens.sign_up import PostSignUpScreen
from gui.screens.feature_panels import ProfileScreen
from gui.screens.feature_panels import FundManagementScreen
from gui.screens.feature_panels import TransferMoneyScreen
from gui.screens.feature_panels import RequestMoneyScreen
from gui.screens.feature_panels import BillManagementScreen
from gui.screens.feature_panels import FDCalculatorScreen
from gui.screens.feature_panels import TransactionHistoryScreen

import customtkinter as ctk

# Theme Of App
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')


class AsterBank(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Screens
        self.gui_instances = {
            'WelcomeScreen': WelcomeScreen(self),
            'LoginScreen': LoginScreen(self),
            'SignUpScreen': SignUpScreen(self),
            'PostSignUpScreen': PostSignUpScreen(self),
            'MainScreen': MainScreen(self),
            'ProfileManagementScreen': ProfileScreen(self),
            'FundManagementScreen': FundManagementScreen(self),
            'TransferMoneyScreen': TransferMoneyScreen(self),
            'RequestMoneyScreen': RequestMoneyScreen(self),
            'BillManagementScreen': BillManagementScreen(self),
            'FDCalculatorScreen': FDCalculatorScreen(self),
            'TransactionHistoryScreen': TransactionHistoryScreen(self)
        }

        # TODO -> change back to WelcomeScreen after testing!!!!!!!!!!!!
        self.show_window('MainScreen')

    def show_window(self, window_to_show: str, window_to_clear=None):
        window_to_show = self.gui_instances[window_to_show]

        window_to_show.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        window_to_show.tkraise()

        if window_to_clear:
            try:
                window_to_clear.clear_screen()
            except AttributeError:
                pass


def main():
    app = AsterBank()

    # Window Config
    app.title(WINDOW_TITLE)

    app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
    app.minsize(1100, 700)
    app.iconbitmap(WINDOW_ICON)

    # Start GUI mainloop
    app.mainloop()

    # Close database connection after app is closed
    db.close_connection()


if __name__ == '__main__':
    main()
