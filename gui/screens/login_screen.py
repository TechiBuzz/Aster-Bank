from typing import Any

from PIL import Image
from settings import *
from gui.screens.transition_screen import TransitionScreen
from gui.util_widgets.warning_label_widget import WarningLabel
from gui.util_widgets.obfuscate_entry_widget import ObfuscateEntryWidget

import bcrypt
import customtkinter as ctk


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # App instance
        self.app_instance = parent

        # Database
        self.db_connection = parent.db_connection

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.login_screen_instance = self
        self.central_frame.place(relx=0.5, rely=0.05, relheight=0.85, relwidth=0.935, anchor='n')

        user_icon_img = ctk.CTkImage(light_image=Image.open(LOGIN_SCREEN_USER_ICON),
                                     dark_image=Image.open(LOGIN_SCREEN_USER_ICON),
                                     size=(140, 140))
        self.user_icon = ctk.CTkLabel(self.central_frame, text='', image=user_icon_img)
        self.user_icon.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.3, anchor='w')

        self.username_entry = LabelledEntry(self.central_frame, 0.4, 'Username', ('alphanumeric', 25), False)
        self.password_entry = LabelledEntry(self.central_frame, 0.6, 'Password', ('any', 15), True)

        self.warning_label = WarningLabel(self.central_frame, LOGIN_ERRORS)
        self.warning_label.place(relx=0, rely=0.75, relwidth=1, relheight=0.1, anchor='w')

        self.login_buttons = LoginButtonsFrame(self.central_frame)

        self.db_connection_frame = DBConnectionFrame(self, self.db_connection)

    def successful_login(self, user_data) -> None:
        account = {
            'ACCOUNT_ID': user_data[0],
            'USERNAME': user_data[1],  # password details omitted for safety
            'FIRST_NAME': user_data[3],
            'LAST_NAME': user_data[4],
            'DATE_OF_BIRTH': user_data[5],
            'GENDER': user_data[6],
            'ADDRESS': user_data[7],
            'EMAIL_ID': user_data[8],
            'PHONE_NO': user_data[9],
            'BALANCE': user_data[10],
            'ADMIN': user_data[11]
        }

        # Update account details
        main_screen = self.app_instance.gui_instances['MainScreen']
        main_screen.user_details_frame.name.configure(text=f'{account['FIRST_NAME']} {account['LAST_NAME']}')
        main_screen.balance_details_frame.balance_var.set(str(account['BALANCE']))

        for screen in ('ProfileManagementScreen', 'FundManagementScreen', 'TransferMoneyScreen', 'RequestMoneyScreen',
                       'BillManagementScreen', 'FDCalculatorScreen', 'TransactionHistoryScreen'):
            self.app_instance.gui_instances[screen].account = account

        # Change from transition screen after 4 seconds
        TransitionScreen(self, 'LoginScreen', 'MainScreen', 'Logging In...', 'Logged In!', 4000)

    def login(self) -> None:
        username: str = self.username_entry.entry.get()
        password_field = self.password_entry.entry

        def non_empty_fields():
            if len(username) == 0:
                self.warning_label.raise_warning(0)
                return
            if len(password_field.get()) == 0:
                self.warning_label.raise_warning(1)
                return

            # All checks passed
            return True

        def database_connected() -> bool:
            db_cnx = self.app_instance.db_connection
            if not db_cnx:
                self.warning_label.raise_warning(2)
                return False
            return True

        def fetch_login_result() -> tuple | None:
            result = None

            cursor = self.app_instance.db_connection.cursor()

            validation_query = 'SELECT PASSWORD FROM accounts WHERE USERNAME = %s'
            cursor.execute(validation_query, (username,))

            # Retrieve stored password from database
            try:
                stored_pass = cursor.fetchone()[0]
            except TypeError:
                return None

            # Check if password valid
            pass_good = bcrypt.checkpw(password_field.get().encode('utf-8'), stored_pass.encode('utf-8'))

            if pass_good:
                # Retrieve entire account if valid password
                cursor.execute('SELECT * FROM accounts WHERE USERNAME = %s', (username,))
                result = cursor.fetchone()

            cursor.close()

            return result

        if non_empty_fields() and database_connected():
            login_result = fetch_login_result()

            if login_result:
                self.successful_login(login_result)
            else:
                self.warning_label.raise_warning(3)

    def signup(self) -> None:
        if self.app_instance.db_connection:
            self.app_instance.show_window(window_to_show='SignUpScreen', window_to_clear='LoginScreen')
        else:
            self.warning_label.raise_warning(2)

    def clear_screen(self) -> None:
        # Reset entry fields
        for field in [self.username_entry.entry, self.password_entry.entry]:
            field.delete(0, 'end')

        # Reset warnings
        self.warning_label.clear_warning()

        self.place_forget()


class LabelledEntry(ctk.CTkFrame):
    def __init__(self, parent, place_rely, label_text: str, entry_validation: tuple, obfuscated_entry: bool = None):
        super().__init__(master=parent, fg_color='transparent')

        self.label = ctk.CTkLabel(self, text=label_text, font=LOGIN_SCREEN_FIELD_LABEl_FONT, justify='left')
        self.label.place(relx=0.06, rely=0.5, relheight=1, relwidth=0.34, anchor='w')

        self.entry_var = ctk.StringVar()
        self.entry_var.trace('w', lambda *args: self.validate_entry(entry_validation))

        self.entry = ctk.CTkEntry(
            master=self,
            height=70,
            corner_radius=40,
            font=LOGIN_SCREEN_FIELD_ENTRY_FONT,
            textvariable=self.entry_var
        )
        self.entry.place(relx=0.43, rely=0.5, relheight=0.7, relwidth=0.5, anchor='w')

        if obfuscated_entry:
            self.entry.configure(show='*')
            self.obfuscator = ObfuscateEntryWidget(self.entry)

        # Place
        self.place(relx=0, rely=place_rely, relwidth=1, relheight=0.2, anchor='w')

    def validate_entry(self, key: tuple):
        max_char_length = key[1]
        entry_var = self.entry_var

        new_value = entry_var.get()
        if key[0] == 'alphanumeric':
            new_value = ''.join(char for char in self.entry_var.get() if (char.isalnum()))[:max_char_length]
        elif key[0] == 'any':
            new_value = ''.join(char for char in self.entry_var.get())[:max_char_length]  # only limit max chars

        self.entry_var.set(new_value)


class LoginButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')

        # Widgets
        self.login_button = ctk.CTkButton(  # Login Button
            master=self,
            width=380,
            height=80,
            text='Login',
            font=LOGIN_SCREEN_BOTTOM_BUTTON_FONT,
            corner_radius=100,
            command=parent.login_screen_instance.login
        )
        self.login_button.place(relx=0.067, rely=0.4, relheight=0.65, relwidth=0.40, anchor='w')

        self.signup_button = ctk.CTkButton(  # Sign-Up Button
            master=self,
            width=380,
            height=80,
            text='Sign-Up',
            font=LOGIN_SCREEN_BOTTOM_BUTTON_FONT,
            corner_radius=100,
            command=parent.login_screen_instance.signup
        )
        self.signup_button.place(relx=0.534, rely=0.4, relheight=0.65, relwidth=0.40, anchor='w')

        # Place
        self.place(relx=0.01, rely=0.9, relwidth=0.98, relheight=0.2, anchor='w')


class DBConnectionFrame(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(master=parent, corner_radius=15, bg_color='transparent')

        # Small DB Icon
        db_icon = Image.open(SMALL_DB_ICON)
        db_status_font = LOGIN_SCREEN_DB_STATUS_FONT

        self.db_icon = ctk.CTkLabel(
            master=self,
            image=ctk.CTkImage(light_image=db_icon, dark_image=db_icon, size=(28, 22)),
            compound='left',
            text='   Database Status:',
            text_color='#d7dddd',
            font=db_status_font
        )
        self.db_icon.pack(expand=True, pady=12, side='left')

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
        self.status_text.pack(expand=True, fill='both', pady=12, side='left')

        # Place
        self.place(relx=0.5, rely=0.947, anchor='center', relwidth=0.3, relheight=0.07)

    def set_db_status(self, db_connection) -> None:
        if db_connection:
            self.connection_status_var.set('Connected')
            self.status_text.configure(text_color='#006d77')
        else:
            self.connection_status_var.set('Disconnected')
            self.status_text.configure(text_color='#ef233c')
