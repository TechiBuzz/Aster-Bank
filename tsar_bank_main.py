from settings import *
from gui.welcome_screen import WelcomeScreen
from gui.main_screen import MainScreen
from gui.login_screen import LoginScreen
from gui.sign_up_screen import SignUpScreen

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

        # User Data
        self.logged_in = False
        self.admin_user = False

        self.account = None

        # Screens
        self.gui_instances = {
            'WelcomeScreen': WelcomeScreen(self),
            'LoginScreen': LoginScreen(self),
            'SignUpScreen': SignUpScreen(self),
            'MainScreen': MainScreen(self)
        }

        # TODO -> change this back to LoginScreen !!!!
        self.show_window('LoginScreen', None)  # show login screen at start

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
    except mysql.connector.errors:
        connection = None
        print("Unable to connect to database!")
    return connection


def main():
    app = TsarBank()

    # Window Config
    app.title(WINDOW_TITLE)
    app.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
    app.resizable(False, False)

    app.iconbitmap(WINDOW_BITMAP_ICON_PATH)

    app.mainloop()


if __name__ == '__main__':
    main()
