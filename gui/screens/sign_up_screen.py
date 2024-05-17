import bcrypt

from settings import *
from tkcalendar import Calendar
from random import randint, choice
from tkinter.messagebox import askokcancel
from gui.screens.transition_screen import TransitionScreen
from gui.util_widgets.back_button import BackButton
from gui.util_widgets.warning_label_widget import WarningLabel
from gui.util_widgets.obfuscate_entry_widget import ObfuscateEntryWidget

import re
import string
import datetime
import customtkinter as ctk


class SignUpScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # App instance
        self.app_instance = parent

        # Database connection
        self.db_connection = parent.db_connection

        # Widgets
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.signup_screen_instance = self
        self.scroll_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        self.name_fields_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='First Name',
                                                  right_label_text='Last Name',
                                                  left_entry_validation=('alphabets_only', 16),
                                                  right_entry_validation=('alphabets_only', 16))
        self.back_button = (BackButton(self.name_fields_frame, 'SignUpScreen', 'LoginScreen', self.app_instance))
        self.back_button.place(relx=0.04, rely=0.15, anchor='nw')  # clunky but works

        self.gender_selection_frame = GenderSelectionFrame(self.scroll_frame)
        self.dob_selection_frame = DateOfBirthSelectionFrame(self.scroll_frame)
        self.address_field_frame = AddressDetailsFrame(self.scroll_frame)
        self.contact_info_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='Email', right_label_text='Phone',
                                                   left_entry_validation=('email', 30),
                                                   right_entry_validation=('numbers_only', 10))
        self.password_entry_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='Password',
                                                     right_label_text='Confirm Password',
                                                     left_entry_validation=('any', 15),
                                                     right_entry_validation=('any', 15))
        self.password_entry_frame.left_field.configure(show='*')
        self.password_entry_frame.right_field.configure(show='*')

        self.obfuscate_pass_entry = ObfuscateEntryWidget(parent=self.password_entry_frame.left_field)

        self.obfuscate_cnf_pass_entry = ObfuscateEntryWidget(parent=self.password_entry_frame.right_field)
        self.warning_label_container = ctk.CTkFrame(self.scroll_frame, corner_radius=15)
        self.warning_label_container.pack(expand=True, fill='x', ipady=12, padx=12, pady=12)

        self.warning_label = WarningLabel(self.warning_label_container, SIGN_UP_ERRORS)
        self.warning_label.pack(expand=True, fill='both', padx=12, pady=12)

        self.operation_buttons_frame = OperationButtonsFrame(self.scroll_frame)

        # All entry fields of this page
        self.entry_fields = [
            self.name_fields_frame.left_field,
            self.name_fields_frame.right_field,
            self.address_field_frame.text_entry,
            self.contact_info_frame.left_field,
            self.contact_info_frame.right_field,
            self.password_entry_frame.left_field,
            self.password_entry_frame.right_field
        ]

        # All radio buttons of this page
        self.radio_buttons = [
            self.gender_selection_frame.radio_button_male,
            self.gender_selection_frame.radio_button_female
        ]

    def update_db(self, first_name: str, last_name: str, gender: str, dob: datetime.date, address: str, email: str,
                  phone: str,
                  password: bytes):
        db_connection = self.db_connection
        cursor = db_connection.cursor()

        # Generate a new username
        cursor.execute('SELECT USERNAME FROM accounts')
        current_usernames = cursor.fetchall()

        chars = string.digits
        random_number_suffix = ''.join(choice(chars) for _ in range(4))

        username = f'{first_name.lower().capitalize()}{last_name.upper()[0]}{random_number_suffix}'
        while username in current_usernames:
            random_number_suffix = ''.join(choice(chars) for _ in range(4))
            username = f'{first_name.lower().capitalize()}{last_name.upper()[0]}{random_number_suffix}'

        # Update
        query = 'INSERT INTO accounts (USERNAME, PASSWORD, FIRST_NAME, LAST_NAME, GENDER, DATE_OF_BIRTH, ADDRESS, EMAIL_ID, PHONE_NO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = (
            username, password, first_name.lower().capitalize(), last_name.lower().capitalize(), gender,
            dob,
            address, email, phone)

        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()

    def valid_credentials(self, first_name: str, last_name: str, gender: str, dob: datetime.date, address: str,
                          email: str,
                          phone: str, password: str, cnf_password: str) -> bool:
        # Emptiness check
        def no_empty_fields():
            if first_name.isspace():
                self.warning_label.raise_warning(0)
                return
            if last_name.isspace():
                self.warning_label.raise_warning(1)
                return
            if address.isspace():
                self.warning_label.raise_warning(2)
                return
            if email.isspace():
                self.warning_label.raise_warning(3)
                return
            if phone.isspace():
                self.warning_label.raise_warning(4)
                return
            if password.isspace():
                self.warning_label.raise_warning(5)
                return
            if cnf_password.isspace():
                self.warning_label.raise_warning(6)
                return

            # All checks passed
            return True

        # Length check
        def valid_character_lengths():
            if len(first_name) < 3:
                self.warning_label.raise_warning(7)
                return
            if len(last_name) < 1:
                self.warning_label.raise_warning(8)
                return
            if len(address) < 20 or len(address) > 255:
                self.warning_label.raise_warning(9)
                return
            if len(phone) < 10:
                self.warning_label.raise_warning(10)
                return
            if len(password) < 8:
                self.warning_label.raise_warning(11)
                return

            # All checks passed
            return True

        # Gender check
        def valid_gender():
            if gender == 'NULL':
                self.warning_label.raise_warning(12)
                return

            # Check passed
            return True

        # Age check
        def valid_age():
            dob_year = int(dob[:4])
            current_year = int(str(datetime.date.today())[:4])

            if not dob_year < (current_year - 15):  # Min age = 15 (set current_year - {min_age})
                self.warning_label.raise_warning(13)
                return

            # Check passed
            return True

        # Email check
        def valid_email():
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'  # stole from https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
            if not re.fullmatch(regex, email):
                self.warning_label.raise_warning(14)
                return

            # Check passed
            return True

        # Password check
        def valid_password():
            special_chars = 0
            uppercase = 0
            numbers = 0
            for char in password:
                if char in string.punctuation: special_chars += 1
                if char.isupper(): uppercase += 1
                if char.isdigit(): numbers += 1

            if special_chars < 2:
                self.warning_label.raise_warning(15)
                return
            if uppercase < 2:
                self.warning_label.raise_warning(16)
                return
            if numbers < 2:
                self.warning_label.raise_warning(17)
                return

            if not password == cnf_password:
                self.warning_label.raise_warning(18)
                return

            # All checks passed
            return True

        return True if no_empty_fields() and valid_character_lengths() and valid_gender() and valid_email() and valid_password() and valid_age() else False

    def submit_info(self):
        user_decision = askokcancel('Submit Info', message='Submit all credentials? This cannot be undone!')

        if user_decision:

            first_name = self.name_fields_frame.left_field.get()
            last_name = self.name_fields_frame.right_field.get()
            gender = 'M' if self.gender_selection_frame.radio_var.get() == 1 else 'F' if self.gender_selection_frame.radio_var.get() == 2 else 'NULL'
            dob = self.dob_selection_frame.cal.get_date()
            address = self.address_field_frame.text_entry.get('0.0', 'end').replace('\n', ' ')
            email = self.contact_info_frame.left_field.get()
            phone = self.contact_info_frame.right_field.get()

            password = self.password_entry_frame.left_field.get()  # raw password
            cnf_password = self.password_entry_frame.right_field.get()

            if self.valid_credentials(first_name, last_name, gender, dob, address, email, phone, password,
                                      cnf_password):
                if self.db_connection:  # database connected

                    # Hash password
                    pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                    self.update_db(first_name, last_name, gender, dob, address, email, phone, pass_hash)

                    # Change from transition screen after 4 seconds
                    self.after(4000, lambda: self.app_instance.show_window('LoginScreen', 'SignUpScreen'))
                    TransitionScreen(self, 'Signing Up...', 'Signed Up!', 3500, 2500)

                else:
                    self.warning_label.raise_warning(19)

    def clear_info(self):
        user_decision = askokcancel('Clear Info', message='Clear all entry fields? This cannot be undone!')

        if user_decision:
            for field in self.entry_fields:
                if field.widgetName == 'TextBox':
                    field.delete('0.0', 'end')
                else:
                    field.delete(0, 'end')
            self.gender_selection_frame.radio_var.set(-1)  # reset radio buttons
            self.dob_selection_frame.cal.selection_set('2000-01-01')  # reset calendar
            self.warning_label.clear_warning()  # reset warnings


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
            new_value = ''.join(char for char in field_var.get() if (char.isalnum() or char == '@' or char == '.'))[
                        :max_char_length]
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
        self.radio_container.columnconfigure((0, 1), weight=1, uniform='G')

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
            year=2000,
            month=1,
            day=1,
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

        # Widgets
        self.submit_button = ctk.CTkButton(
            self,
            text='Submit',
            font=SIGNUP_SCREEN_OPERATION_BUTTON_FONT,
            corner_radius=100,
            command=parent.signup_screen_instance.submit_info
        )
        self.submit_button.pack(expand=True, fill='both', ipady=10, padx=12, pady=12, side='left')

        self.clear_button = ctk.CTkButton(
            self,
            text='Clear',
            font=SIGNUP_SCREEN_OPERATION_BUTTON_FONT,
            corner_radius=100,
            command=parent.signup_screen_instance.clear_info
        )
        self.clear_button.pack(expand=True, fill='both', ipady=10, padx=12, pady=12, side='left')

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)
