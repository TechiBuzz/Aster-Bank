from PIL import Image
from settings import *
from gui.util_widgets.warning_label_widget import WarningLabel
from gui.util_widgets.obfuscate_entry_widget import ObfuscateEntryWidget

import hashlib
import customtkinter as ctk

'''
INSTANCE OF MAIN WINDOW
'''
MAIN_WINDOW_INSTANCE = None
WARNING_LABEL = None


def successful_login(user_data):
    # Update client details in main window
    MAIN_WINDOW_INSTANCE.logged_in = True
    MAIN_WINDOW_INSTANCE.admin_user = True if user_data[-1] else False  # user_data[-1] is admin column of accounts table

    MAIN_WINDOW_INSTANCE.account = {
        'ACCOUNT_ID': user_data[0],
        'USERNAME': user_data[1],  # password details omitted for safety
        'FIRST_NAME': user_data[3],
        'LAST_NAME': user_data[4],
        'DATE_OF_BIRTH': user_data[5],
        'GENDER': user_data[6],
        'ADDRESS': user_data[7],
        'EMAIL_ID': user_data[8],
        'PHONE_NO': user_data[9],
        'BALANCE': user_data[10]  # admin detail also omitted as it is previously stored in a var
    }

    # Change window
    MAIN_WINDOW_INSTANCE.show_window(window_to_show='MainScreen', window_to_clear='LoginScreen')


def login(central_frame) -> None:
    username: str = central_frame.entry_fields_frame.username_entry.get()

    password_field = central_frame.entry_fields_frame.password_entry
    password = hashlib.sha256(password_field.get().encode()).hexdigest()

    if len(username) != 0 and len(password_field.get()) != 0:  # non-blank username and password
        db_cnx = MAIN_WINDOW_INSTANCE.db_connection

        if db_cnx:  # database connected
            cursor = db_cnx.cursor()

            validation_query = "SELECT * FROM accounts WHERE USERNAME = %s AND PASSWORD = %s"
            cursor.execute(validation_query, (username, password))
            result = cursor.fetchone()
            cursor.close()

            successful_login(result) if result else WARNING_LABEL.raise_warning(2)  # credentials match
        else:
            WARNING_LABEL.raise_warning(1)

    else:
        WARNING_LABEL.raise_warning(0)


def signup() -> None:
    if MAIN_WINDOW_INSTANCE.db_connection:
        MAIN_WINDOW_INSTANCE.show_window(window_to_show='SignUpScreen', window_to_clear='LoginScreen')
    else:
        WARNING_LABEL.raise_warning(1)


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Get main window instance
        global MAIN_WINDOW_INSTANCE
        MAIN_WINDOW_INSTANCE = parent

        # Database
        self.db_connection = parent.db_connection

        # Widgets
        self.central_frame = CentralFrame(self)
        self.db_connection_frame = DBConnectionFrame(self, self.db_connection)

        # All entry fields of this class and subclasses
        self.entry_fields = [
            self.central_frame.entry_fields_frame.username_entry,
            self.central_frame.entry_fields_frame.password_entry
        ]

        # Warning Label
        self.warning_label = WarningLabel(self.central_frame, LOGIN_ERRORS)
        self.warning_label.place(relx=0.5, rely=0.65, relwidth=0.7, relheight=0.1, anchor='center')

        global WARNING_LABEL
        WARNING_LABEL = self.warning_label

class CentralFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=15)

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=2)

        # Widgets
        user_icon = Image.open(USER_ICON_PATH)
        user_icon = ctk.CTkImage(light_image=user_icon, dark_image=user_icon, size=(150, 150))
        ctk.CTkLabel(master=self, text='', image=user_icon).grid(column=0, row=0, pady=12)  # User Icon

        self.entry_fields_frame = self.EntryFieldsFrame(self)  # Stored in var to access fields from buttons

        self.obfuscate_password = ObfuscateEntryWidget(parent=self, obfuscate_entry=self.entry_fields_frame.password_entry)
        self.obfuscate_password.place(relx=0.89, rely=0.493)

        self.LoginButtonsFrame(self)

        # Place
        self.place(relx=0.5, rely=0.5, relheight=0.85, relwidth=0.90, anchor='center')

    class EntryFieldsFrame(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(master=parent, fg_color='transparent')

            # Layout
            self.rowconfigure((0, 1), weight=1, uniform='Z')
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=2)

            # Widgets
            self.username_label = ctk.CTkLabel(self, text=' Username',
                                               font=LOGIN_SCREEN_FIELD_LABEl_FONT, justify='left')
            self.username_label.grid(row=0, column=0, sticky='nsew')

            self.username_entry_var = ctk.StringVar()
            self.username_entry_var.trace('w', lambda *args: self.validate_entry(is_password_entry=False))

            self.username_entry = ctk.CTkEntry(
                master=self,
                height=70,
                corner_radius=COMMON_ENTRY_CORNER_RADIUS,
                font=LOGIN_SCREEN_FIELD_ENTRY_FONT,
                textvariable=self.username_entry_var
            )
            self.username_entry.grid(row=0, column=1, sticky='ew', padx=40)

            self.password_label = ctk.CTkLabel(self, text='Password',
                                               font=LOGIN_SCREEN_FIELD_LABEl_FONT, justify='left')
            self.password_label.grid(row=1, column=0, sticky='nsew')

            self.password_entry_var = ctk.StringVar()
            self.password_entry_var.trace('w', lambda *args: self.validate_entry(is_password_entry=True))

            self.password_entry = ctk.CTkEntry(
                master=self,
                height=70,
                corner_radius=COMMON_ENTRY_CORNER_RADIUS,
                font=LOGIN_SCREEN_FIELD_ENTRY_FONT,
                textvariable=self.password_entry_var,
                show='*'
            )
            self.password_entry.grid(row=1, column=1, sticky='ew', padx=40)

            # Execute login on pressing 'Enter' on keyboard
            self.username_entry.bind('<Return>', lambda *args: login(parent))
            self.password_entry.bind('<Return>', lambda *args: login(parent))

            # Place
            self.grid(column=0, row=1, sticky='nsew', padx=10, pady=10)

        def validate_entry(self, is_password_entry: bool, *args):
            max_char_length = 20

            if is_password_entry:
                current_value = self.password_entry_var.get()
                new_value = ''.join(char for char in current_value if char != ' ')[:max_char_length]  # Remove numbers
                self.password_entry_var.set(new_value)
            else:
                current_value = self.username_entry_var.get()
                new_value = ''.join(char for char in current_value if char.isalnum())[
                            :max_char_length]  # Remove spaces and numbers
                self.username_entry_var.set(new_value)  # Update variable with modified value

    class LoginButtonsFrame(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(master=parent, fg_color='transparent')

            # Widgets
            self.login_button = ctk.CTkButton(  # Login Button
                master=self,
                width=LOGIN_SCREEN_BOTTOM_BUTTON_WIDTH,
                height=LOGIN_SCREEN_BOTTOM_BUTTON_HEIGHT,
                text='Login',
                font=LOGIN_SCREEN_BOTTOM_BUTTON_FONT,
                corner_radius=LOGIN_SCREEN_BOTTOM_BUTTON_CORNER_RADIUS,
                command=lambda: login(parent)
            )
            self.login_button.place(relx=0.08, rely=0.5, anchor='w')

            self.signup_button = ctk.CTkButton(  # Sign-Up Button
                master=self,
                width=LOGIN_SCREEN_BOTTOM_BUTTON_WIDTH,
                height=LOGIN_SCREEN_BOTTOM_BUTTON_HEIGHT,
                text='Sign-Up',
                font=LOGIN_SCREEN_BOTTOM_BUTTON_FONT,
                corner_radius=LOGIN_SCREEN_BOTTOM_BUTTON_CORNER_RADIUS,
                command=signup
            )
            self.signup_button.place(relx=0.56, rely=0.5, anchor='w')

            # Place
            self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)


class DBConnectionFrame(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(master=parent)

        # Configuration
        self.configure(
            corner_radius=15,
            bg_color='transparent'
        )

        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='A')

        # Small DB Icon
        db_icon = Image.open(SMALL_DB_ICON_PATH)
        db_status_font = LOGIN_SCREEN_DB_STATUS_FONT

        self.db_icon = ctk.CTkLabel(
            master=self,
            image=ctk.CTkImage(light_image=db_icon, dark_image=db_icon, size=(28, 28)),
            compound='left',
            text='   Database Status:',
            text_color='#d7dddd',
            font=db_status_font
        )
        self.db_icon.grid(row=0, column=0, columnspan=2, padx=4, pady=4)

        # Connection Status Text
        self.connection_status_var = ctk.StringVar(value='')
        self.after(500, lambda: self.set_db_status(db_connection))

        self.status_text = ctk.CTkLabel(
            master=self,
            text='',
            text_color='#ef233c',
            textvariable=self.connection_status_var,
            font=db_status_font,
            justify='left'
        )
        self.status_text.grid(row=0, column=2, columnspan=3, padx=4, pady=4, sticky='w')

        # Place
        self.place(relx=0.5, rely=0.96, anchor='center', relwidth=0.3, relheight=0.05)

    def set_db_status(self, db_connection) -> None:
        if db_connection:
            self.connection_status_var.set('Connected')
            self.status_text.configure(text_color='#006d77')
        else:
            self.connection_status_var.set('Disconnected')
            self.status_text.configure(text_color='#ef233c')
