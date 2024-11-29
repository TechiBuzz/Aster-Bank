from settings import *
from util.database import db
from util.account_manager import account_manager
from util.image_util import open_image
from gui.screens.transition import TransitionScreen
from gui.util_widgets.warning_label import WarningLabel
from gui.util_widgets.obfuscate_entry import ObfuscateEntryWidget

import bcrypt
import customtkinter as ctk


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # App instance
        self.app_instance = parent

        # Widgets
        self.central_frame = ctk.CTkFrame(self, corner_radius=15)
        self.central_frame.login_screen_instance = self
        self.central_frame.place(relx=0.5, rely=0.05, relheight=0.85, relwidth=0.935, anchor='n')

        self.user_icon = ctk.CTkLabel(self.central_frame, text='', image=open_image(USER_ICON, (140, 140)))
        self.user_icon.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.3, anchor='w')

        self.username_entry = LabelledEntry(self.central_frame, 0.4, 'Username', ('alphanumeric', 25), False)
        self.password_entry = LabelledEntry(self.central_frame, 0.6, 'Password', ('any', 15), True)

        self.warning_label = WarningLabel(self.central_frame, LOGIN_ERRORS)
        self.warning_label.place(relx=0, rely=0.75, relwidth=1, relheight=0.1, anchor='w')

        self.login_buttons = LoginButtonsFrame(self.central_frame)

        self.db_connection_frame = DBConnectionFrame(self)

        '''
        REMOVE AFTER TESTING
        '''

        helpful_button = ctk.CTkButton(self.central_frame, text='FILL INFO', command=lambda: [self.username_entry.entry_var.set('AbuE7026'), self.password_entry.entry_var.set('AMAN@2007!')])
        helpful_button.place(relx=0.1, rely=0.7, relheight=0.1)

    def successful_login(self, user_data) -> None:
        account = {
            'ID': user_data[0],
            'USERNAME': user_data[1],  # password details omitted for safety
            'FIRST_NAME': user_data[3],
            'LAST_NAME': user_data[4],
            'GENDER': user_data[5],
            'DATE_OF_BIRTH': user_data[6],
            'ADDRESS': user_data[7],
            'EMAIL_ID': user_data[8],
            'PHONE_NO': user_data[9],
            'BALANCE': user_data[10],
            'ADMIN': user_data[11],
            'IMAGE': user_data[12]
        }

        # Update account details
        account_manager.set_account(account)

        for screen in ('MainScreen', 'ProfileScreen', 'DepositScreen', 'TransferScreen', 'WithdrawScreen',
                       'EStatementScreen', 'FDCalculatorScreen', 'TransactionsScreen'):
            try:
                self.app_instance.gui_instances[screen].update_info()
            except AttributeError:
                pass

        # Change from transition screen after 1 second
        TransitionScreen(self, 'MainScreen', 'Logging In...', 'Logged In!', 1000)

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
            if not db.connection:
                self.warning_label.raise_warning(2)
                return False
            return True

        def fetch_login_result() -> tuple | None:
            result = None

            validation_query = 'SELECT PASSWORD FROM accounts WHERE USERNAME = %s'
            retrieved_pass = db.fetch_result(validation_query, (username,))

            if retrieved_pass:
                retrieved_pass = retrieved_pass[0][0]
                if bcrypt.checkpw(password_field.get().encode('utf-8'), retrieved_pass.encode('utf-8')):
                    result = db.fetch_result('SELECT * FROM accounts WHERE USERNAME = %s', (username,))

            return result

        if non_empty_fields() and database_connected():
            login_result = fetch_login_result()

            if login_result:
                self.successful_login(login_result[0])
            else:
                self.warning_label.raise_warning(3)

    def signup(self) -> None:
        if db.connection:
            self.app_instance.show_window('SignUpScreen', self)
        else:
            self.warning_label.raise_warning(2)

    def clear_screen(self) -> None:
        # Reset entry fields
        for field in [self.username_entry.entry, self.password_entry.entry]:
            field.delete(0, 'end')

        # Reset warnings
        self.warning_label.clear_warning()


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
            textvariable=self.entry_var,
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
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=15, bg_color='transparent')

        # Small DB Icon
        db_status_font = LOGIN_SCREEN_DB_STATUS_FONT

        self.db_icon = ctk.CTkLabel(
            master=self,
            image=open_image(SMALL_DB_ICON, (28, 22)),
            compound='left',
            text='   Database Status:',
            text_color='#d7dddd',
            font=db_status_font
        )
        self.db_icon.pack(expand=True, pady=12, side='left')

        # Connection Status Text
        self.connection_status_var = ctk.StringVar(value='')
        self.after(500, self.set_db_status)

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

    def set_db_status(self) -> None:
        if db.connection:
            self.connection_status_var.set('Connected')
            self.status_text.configure(text_color='#006d77')
        else:
            self.connection_status_var.set('Disconnected')
            self.status_text.configure(text_color='#ef233c')
