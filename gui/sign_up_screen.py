import datetime

from settings import *
from tkcalendar import Calendar
from gui.back_button import BackButton

import customtkinter as ctk


class SignUpScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        # Get main window instance (used for back button)
        self.MAIN_WINDOW_INSTANCE = parent

        # Existing Account Numbers
        self.db_connection = parent.db_connection
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('SELECT ID FROM accounts')

            self.accounts_list = cursor.fetchall()
            cursor.close()

        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.scroll_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        # Widgets
        self.back_button = BackButton(self, 'LoginScreen', 0.04, 0.04)
        self.name_fields_frame = NameFieldsFrame(self.scroll_frame)
        self.gender_selection_frame = GenderSelectionFrame(self.scroll_frame)
        self.dob_selection_frame = DateOfBirthSelectionFrame(self.scroll_frame)
        self.address_field_frame = AddressDetailsFrame(self.scroll_frame)

        # All entry fields of this class and subclasses
        self.entry_fields = [
            self.name_fields_frame.first_name_field,
            self.name_fields_frame.last_name_field
        ]

        # Warning Label
        self.warning_label = None

    def get_window_name(self) -> str:
        return 'SignUpScreen'


class NameFieldsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)

        # Layout
        self.rowconfigure((0, 1), weight=1, uniform='H')
        self.columnconfigure((0, 1), weight=1, uniform='H')

        # Widgets
        self.first_name_label = ctk.CTkLabel(self, text='First Name', font=SIGNUP_SCREEN_LABEL_FONT)
        self.first_name_label.grid(row=0, column=0, sticky='nsew', padx=12, pady=12)

        self.first_name_field_var = ctk.StringVar()
        self.first_name_field_var.trace('w', lambda *args: self.validate_name_field('f_name'))

        self.first_name_field = ctk.CTkEntry(self, width=450, height=70, textvariable=self.first_name_field_var,
                                             corner_radius=COMMON_ENTRY_CORNER_RADIUS,
                                             font=SIGNUP_SCREEN_FIELD_ENTRY_FONT, justify='center')
        self.first_name_field.grid(row=1, column=0, padx=12, pady=12)

        self.last_name_label = ctk.CTkLabel(self, text='Last Name', font=SIGNUP_SCREEN_LABEL_FONT)
        self.last_name_label.grid(row=0, column=1, sticky='nsew', padx=12, pady=12)

        self.last_name_field_var = ctk.StringVar()
        self.last_name_field_var.trace('w', lambda *args: self.validate_name_field('l_name'))

        self.last_name_field = ctk.CTkEntry(self, width=450, height=70, textvariable=self.last_name_field_var,
                                            corner_radius=COMMON_ENTRY_CORNER_RADIUS,
                                            font=SIGNUP_SCREEN_FIELD_ENTRY_FONT, justify='center')
        self.last_name_field.grid(row=1, column=1, padx=12, pady=12)

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)

    def validate_name_field(self, field_type: str):
        field_var = self.first_name_field_var if field_type == 'f_name' else self.last_name_field_var

        max_char_length = 20

        new_value = ''.join(char for char in field_var.get() if char.isalpha())[:max_char_length]
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

        self.calendar_container = ctk.CTkFrame(self)
        self.calendar_container.pack(expand=True, fill='both', side='bottom', ipady=125, padx=12, pady=12)

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

    def validate_date(self, date_var, is_year=False, *args):
        field_var = date_var
        max_char_length = 4 if is_year else 2

        new_value = ''.join(char for char in field_var.get() if char.isdigit())[:max_char_length]
        field_var.set(new_value)


class AddressDetailsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Widgets
        self.header_label = ctk.CTkLabel(self, text='Address', font=SIGNUP_SCREEN_LABEL_FONT)
        self.header_label.pack(expand=True, fill='both', side='top', padx=12, pady=12)

        self.text_container = ctk.CTkFrame(self)
        self.text_container.pack(expand=True, fill='both', side='bottom', ipady=12, padx=12, pady=12)

        self.text_entry_var = ctk.StringVar()
        self.text_entry_var.trace('w', lambda *args: print(self.text_entry_var.get()))

        self.text_entry = ctk.CTkTextbox(self.text_container)
        self.text_entry.pack(expand=True, fill='both', side='bottom', ipady=12, padx=12, pady=12)

        # Place
        self.pack(expand=True, fill='x', padx=12, pady=12)
