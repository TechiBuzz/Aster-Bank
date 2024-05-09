import hashlib

from settings import *
from tkcalendar import Calendar
from gui.util_widgets.back_button import BackButton
from tkinter.messagebox import askokcancel
from gui.util_widgets.warning_label_widget import WarningLabel
from gui.util_widgets.obfuscate_entry_widget import ObfuscateEntryWidget

import re
import random
import datetime
import customtkinter as ctk

SIGNUP_SCREEN_INSTANCE = None
WARNING_LABEL = None


def update_db(first_name: str, last_name: str, gender: str, dob: datetime.date, address: str, email: str, phone: str, password: str):
    db_connection = SIGNUP_SCREEN_INSTANCE.db_connection
    cursor = db_connection.cursor()

    # Generate a new account number
    cursor.execute('SELECT ID FROM accounts')
    current_ids = cursor.fetchall()

    account_id = random.randint(10000, 99999)
    while account_id in current_ids:
        account_id = random.randint(10000, 99999)

    # Generate a new username
    '''
    Generate a formatted username
    Example:
        First Name: Mickey
        Last Name: Mouse
        DOB: 1928-11-18
        
    -> Output: MickeyM111828 (format = first_name + last_name's first character + dob_month + dob_day + dob_year)
    '''
    split_dob = str(dob).split('-')
    username = f'{first_name.lower().capitalize()}{last_name.upper()[0]}{split_dob[1]}{split_dob[2]}{split_dob[0][2:]}'

    # Update
    # query = f'INSERT INTO accounts VALUES ({account_id}, \'{username}\', \'{password}\', \'{first_name.lower().capitalize()}\', \'{last_name.lower().capitalize()}\', \'{gender}\', \'{str(dob)}\', \'{address}\', \'{email}\', \'{phone}\')'
    query = 'INSERT INTO accounts (ID, USERNAME, PASSWORD, FIRST_NAME, LAST_NAME, GENDER, DATE_OF_BIRTH, ADDRESS, EMAIL_ID, PHONE_NO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    values = (account_id, username, password, first_name.lower().capitalize(), last_name.lower().capitalize(), gender, dob, address, email, phone)
     
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()


def valid_credentials(first_name: str, last_name: str, gender: str, dob: datetime.date, address: str, email: str, phone: str, password: str, cnf_password: str) -> bool:
    # Emptiness check
    def no_empty_fields():
        if first_name.isspace():
            WARNING_LABEL.raise_warning(0)
            return False
        elif last_name.isspace():
            WARNING_LABEL.raise_warning(1)
            return False
        elif address.isspace():
            WARNING_LABEL.raise_warning(2)
            return False
        elif email.isspace():
            WARNING_LABEL.raise_warning(3)
            return False
        elif phone.isspace():
            WARNING_LABEL.raise_warning(4)
            return False
        elif password.isspace():
            WARNING_LABEL.raise_warning(5)
            return False
        elif cnf_password.isspace():
            WARNING_LABEL.raise_warning(6)
            return False
        else:
            return True

    # Length check
    def valid_character_lengths():
        if len(first_name) < 3:
            WARNING_LABEL.raise_warning(7)
            return False
        elif len(last_name) < 1:
            WARNING_LABEL.raise_warning(8)
            return False
        elif len(address) < 20 or len(address) > 255:
            WARNING_LABEL.raise_warning(9)
            return False
        elif len(phone) < 10:
            WARNING_LABEL.raise_warning(10)
            return False
        elif len(password) < 8:
            WARNING_LABEL.raise_warning(11)
            return False
        else:
            return True

    # Gender check
    def valid_gender():
        if gender == 'NULL':
            WARNING_LABEL.raise_warning(12)
            return False
        else:
            return True

    # Age check
    def valid_age():
        dob_year = int(dob[:4])
        current_year = int(str(datetime.date.today())[:4])

        if not dob_year < (current_year - 15):  # Min age = 15 (set current_year - {min_age})
            WARNING_LABEL.raise_warning(13)
            return False
        else:
            return True

    # Email check
    def valid_email():
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'  # stole from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
        if not re.fullmatch(regex, email):
            WARNING_LABEL.raise_warning(14)
            return False
        else:
            return True

    # Password check
    def valid_password():
        special_chars = 0
        uppercase = 0
        numbers = 0
        for char in password:
            if not char.isalnum(): special_chars += 1
            if char.isupper(): uppercase += 1
            if char.isdigit(): numbers += 1

        if special_chars < 2:
            WARNING_LABEL.raise_warning(15)
            return False
        if uppercase < 2:
            WARNING_LABEL.raise_warning(16)
            return False
        if numbers < 3:
            WARNING_LABEL.raise_warning(17)
            return False

        if not password == cnf_password:
            WARNING_LABEL.raise_warning(18)
            return False

        return True

    return True if no_empty_fields() and valid_character_lengths() and valid_gender() and valid_age() and valid_email() and valid_password() else False


def submit_info():
    user_decision = askokcancel('Submit Info', message='Submit all credentials? This cannot be undone!')

    if user_decision:

        first_name = SIGNUP_SCREEN_INSTANCE.name_fields_frame.left_field.get()
        last_name = SIGNUP_SCREEN_INSTANCE.name_fields_frame.right_field.get()
        gender = 'M' if SIGNUP_SCREEN_INSTANCE.gender_selection_frame.radio_var.get() == 1 else 'F' if SIGNUP_SCREEN_INSTANCE.gender_selection_frame.radio_var.get() == 2 else 'O' if SIGNUP_SCREEN_INSTANCE.gender_selection_frame.radio_var.get() == 3 else 'NULL'
        dob = SIGNUP_SCREEN_INSTANCE.dob_selection_frame.cal.get_date()
        address = SIGNUP_SCREEN_INSTANCE.address_field_frame.text_entry.get('0.0', 'end').replace('\n', ' ')
        email = SIGNUP_SCREEN_INSTANCE.contact_info_frame.left_field.get()
        phone = SIGNUP_SCREEN_INSTANCE.contact_info_frame.right_field.get()

        password = SIGNUP_SCREEN_INSTANCE.password_entry_frame.left_field.get()  # raw password
        cnf_password = SIGNUP_SCREEN_INSTANCE.password_entry_frame.right_field.get()

        if valid_credentials(first_name, last_name, gender, dob, address, email, phone, password, cnf_password):
            if SIGNUP_SCREEN_INSTANCE.db_connection:  # database connected (this is just a 2nd level ensurance as database must already be connected in order to get to sign-up screen)
                hashed_password = hashlib.sha256(password.encode()).hexdigest()  # encrypt the password
                update_db(first_name, last_name, gender, dob, address, email, phone, hashed_password)
                SIGNUP_SCREEN_INSTANCE.MAIN_WINDOW_INSTANCE.show_window('LoginScreen', 'SignUpScreen')
            else:
                WARNING_LABEL.raise_warning(19)


def clear_info():
    user_decision = askokcancel('Clear Info', message='Clear all entry fields? This cannot be undone!')

    if user_decision:
        for field in SIGNUP_SCREEN_INSTANCE.entry_fields:
            if field.widgetName == 'TextBox':
                field.delete('0.0', 'end')
            else:
                field.delete(0, 'end')
        SIGNUP_SCREEN_INSTANCE.gender_selection_frame.radio_var.set(-1)  # reset radio buttons
        WARNING_LABEL.clear_warning()

class SignUpScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        global SIGNUP_SCREEN_INSTANCE
        SIGNUP_SCREEN_INSTANCE = self

        # Get main window instance (used for back button)
        self.MAIN_WINDOW_INSTANCE = parent

        # Database connection
        self.db_connection = parent.db_connection

        # Widgets
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.scroll_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        self.back_button = BackButton(self, 'LoginScreen', 0.04, 0.04)
        self.name_fields_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='First Name',
                                                  right_label_text='Last Name',
                                                  left_entry_validation=('alphabets_only', 20),
                                                  right_entry_validation=('alphabets_only', 20))
        self.gender_selection_frame = GenderSelectionFrame(self.scroll_frame)
        self.dob_selection_frame = DateOfBirthSelectionFrame(self.scroll_frame)
        self.address_field_frame = AddressDetailsFrame(self.scroll_frame)
        self.contact_info_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='Email', right_label_text='Phone',
                                                   left_entry_validation=('email', 30),
                                                   right_entry_validation=('numbers_only', 10))
        self.password_entry_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='Password', right_label_text='Confirm Password',
                                                     left_entry_validation=('any', 15), right_entry_validation=('any', 15))
        self.password_entry_frame.left_field.configure(show='*')
        self.password_entry_frame.right_field.configure(show='*')

        self.obfuscate_pass_entry = ObfuscateEntryWidget(parent=self.password_entry_frame.left_field, obfuscate_entry=self.password_entry_frame.left_field)
        self.obfuscate_pass_entry.place(relx=0.87, rely=0.5, anchor='w')

        self.obfuscate_cnf_pass_entry = ObfuscateEntryWidget(parent=self.password_entry_frame.right_field, obfuscate_entry=self.password_entry_frame.right_field)
        self.obfuscate_cnf_pass_entry.place(relx=0.87, rely=0.5, anchor='w')

        self.warning_label_container = ctk.CTkFrame(self.scroll_frame, corner_radius=15)
        self.warning_label_container.pack(expand=True, fill='x', ipady=12, padx=12, pady=12)

        self.warning_label = WarningLabel(self.warning_label_container, SIGN_UP_ERRORS)
        self.warning_label.pack(expand=True, fill='both', padx=12, pady=12)

        self.operation_buttons_frame = OperationButtonsFrame(self.scroll_frame)

        # All entry fields of this class and subclasses
        self.entry_fields = [
            self.name_fields_frame.left_field,
            self.name_fields_frame.right_field,
            self.address_field_frame.text_entry,
            self.contact_info_frame.left_field,
            self.contact_info_frame.right_field,
            self.password_entry_frame.left_field,
            self.password_entry_frame.right_field
        ]

        # Make warning label global
        global WARNING_LABEL
        WARNING_LABEL = self.warning_label

    def get_window_name(self) -> str:
        return 'SignUpScreen'


class DoubleEntryFrame(ctk.CTkFrame):
    def __init__(self, parent, left_label_text: str, right_label_text: str, left_entry_validation: tuple = None,
                 right_entry_validation: tuple = None):
        super().__init__(parent, corner_radius=15)

        # Layout
        self.rowconfigure((0, 1), weight=1, uniform='H')
        self.columnconfigure((0, 1), weight=1, uniform='H')

        # Widgets
        self.left_label = ctk.CTkLabel(self, text=left_label_text, font=SIGNUP_SCREEN_LABEL_FONT)
        self.left_label.grid(row=0, column=0, sticky='nsew', padx=12, pady=12)

        self.left_field_var = ctk.StringVar()
        self.left_field = ctk.CTkEntry(self, width=450, height=70, textvariable=self.left_field_var,
                                       corner_radius=COMMON_ENTRY_CORNER_RADIUS,
                                       font=SIGNUP_SCREEN_FIELD_ENTRY_FONT, justify='center')
        self.left_field.grid(row=1, column=0, padx=12, pady=12)

        self.right_label = ctk.CTkLabel(self, text=right_label_text, font=SIGNUP_SCREEN_LABEL_FONT)
        self.right_label.grid(row=0, column=1, sticky='nsew', padx=12, pady=12)

        self.right_field_var = ctk.StringVar()
        self.right_field = ctk.CTkEntry(self, width=450, height=70, textvariable=self.right_field_var,
                                        corner_radius=COMMON_ENTRY_CORNER_RADIUS,
                                        font=SIGNUP_SCREEN_FIELD_ENTRY_FONT, justify='center')
        self.right_field.grid(row=1, column=1, padx=12, pady=12)

        # Entry Validation
        if left_entry_validation:
            self.left_field_var.trace('w',
                                      lambda *args: self.validate_field(self.left_field_var, left_entry_validation))
        if right_entry_validation:
            self.right_field_var.trace('w',
                                       lambda *args: self.validate_field(self.right_field_var, right_entry_validation))

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)

    def validate_field(self, field_var, key: tuple):
        max_char_length = key[1]

        new_value = field_var.get()
        if key[0] == 'numbers_only':
            new_value = ''.join(char for char in field_var.get() if char.isdigit())[:max_char_length]
        elif key[0] == 'alphabets_only':
            new_value = ''.join(char for char in field_var.get() if char.isalpha())[:max_char_length]
        elif key[0] == 'email':
            new_value = ''.join(char for char in field_var.get() if (char.isalnum() or char == '@' or char == '.'))[:max_char_length]
        elif key[0] == 'any':
            new_value = ''.join(char for char in field_var.get())[:max_char_length]  # only limit max chars

        field_var.set(new_value)


class GenderSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        # Widgets
        self.header_label = ctk.CTkLabel(self, text='Gender', font=SIGNUP_SCREEN_LABEL_FONT)
        self.header_label.pack(expand=True, fill='both', side='top', padx=12, pady=12)

        self.radio_container = ctk.CTkFrame(self)

        self.radio_container.rowconfigure(0, weight=1)
        self.radio_container.columnconfigure((0, 1, 2), weight=1, uniform='G')

        self.radio_container.pack(expand=True, fill='both', side='bottom', ipady=12, padx=12, pady=12)

        self.radio_var = ctk.IntVar(value=0)
        self.radio_button_male = ctk.CTkRadioButton(self.radio_container, text='Male',
                                                    font=SIGNUP_SCREEN_RADIO_BUTTON_FONT, variable=self.radio_var,
                                                    value=1)
        self.radio_button_male.grid(row=0, column=0)

        self.radio_button_female = ctk.CTkRadioButton(self.radio_container, text='Female',
                                                      font=SIGNUP_SCREEN_RADIO_BUTTON_FONT, variable=self.radio_var,
                                                      value=2)
        self.radio_button_female.grid(row=0, column=1)

        self.radio_button_other = ctk.CTkRadioButton(self.radio_container, text='Other',
                                                     font=SIGNUP_SCREEN_RADIO_BUTTON_FONT, variable=self.radio_var,
                                                     value=3)
        self.radio_button_other.grid(row=0, column=2)

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)


class DateOfBirthSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        # Widgets
        self.header_label = ctk.CTkLabel(self, text='Date of Birth', font=SIGNUP_SCREEN_LABEL_FONT)
        self.header_label.pack(expand=True, fill='both', side='top', padx=12, pady=12)

        self.calendar_container = ctk.CTkFrame(self, corner_radius=15)
        self.calendar_container.pack(expand=True, fill='both', side='bottom', ipady=125, padx=14, pady=14)

        self.cal = Calendar(
            self.calendar_container,
            selectmode='day',
            locale='en_US',
            disabledforeground='red',
            cursor="hand2",
            date_pattern='yyyy-mm-dd',
            mindate=datetime.date(year=1947, month=1, day=1),
            maxdate=datetime.date.today(),
            background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
            selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1]
        )
        self.cal.pack(expand=True, fill='both', padx=12, pady=12)

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)


class AddressDetailsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        # Widgets
        self.header_label = ctk.CTkLabel(self, text='Address', font=SIGNUP_SCREEN_LABEL_FONT)
        self.header_label.pack(expand=True, fill='both', side='top', padx=12, pady=12)

        self.text_entry_container = ctk.CTkFrame(self, corner_radius=15)
        self.text_entry_container.pack(expand=True, fill='both', side='bottom', ipady=12, padx=12, pady=12)

        self.text_entry = ctk.CTkTextbox(self.text_entry_container, font=SIGNUP_SCREEN_ADDRESS_FONT, border_spacing=15,
                                         corner_radius=15)
        self.text_entry.pack(expand=True, fill='both', padx=12, pady=12)

        self.text_entry.widgetName = 'TextBox'  # required to clear field in main instance

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)


class OperationButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        # # Layout
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure((0, 1), weight=1, uniform='T')

        # Widgets
        self.submit_button = ctk.CTkButton(
            self,
            text='Submit',
            font=SIGNUP_SCREEN_OPERATION_BUTTON_FONT,
            corner_radius=100,
            command=submit_info
        )
        self.submit_button.pack(expand=True, fill='both', ipady=10, padx=12, pady=12, side='left')

        self.clear_button = ctk.CTkButton(
            self,
            text='Clear',
            font=SIGNUP_SCREEN_OPERATION_BUTTON_FONT,
            corner_radius=100,
            command=clear_info
        )
        self.clear_button.pack(expand=True, fill='both', ipady=10, padx=12, pady=12, side='left')

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)
