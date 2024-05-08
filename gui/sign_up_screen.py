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
        self.name_fields_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='First Name', right_label_text='Last Name', left_entry_validation=('alphabets_only', 20), right_entry_validation=('alphabets_only', 20))
        self.gender_selection_frame = GenderSelectionFrame(self.scroll_frame)
        self.dob_selection_frame = DateOfBirthSelectionFrame(self.scroll_frame)
        self.address_field_frame = AddressDetailsFrame(self.scroll_frame)
        self.contact_info_frame = DoubleEntryFrame(self.scroll_frame, left_label_text='Email', right_label_text='Phone', left_entry_validation=('email', 30), right_entry_validation=('numbers_only', 10))

        # All entry fields of this class and subclasses
        self.entry_fields = [
            self.name_fields_frame.left_field,
            self.name_fields_frame.right_field,
            self.address_field_frame.text_entry,
            self.contact_info_frame.left_field,
            self.contact_info_frame.right_field
        ]

        # Warning Label
        self.warning_label = None

    def get_window_name(self) -> str:
        return 'SignUpScreen'


class DoubleEntryFrame(ctk.CTkFrame):
    def __init__(self, parent, left_label_text: str, right_label_text: str, left_entry_validation: tuple, right_entry_validation: tuple):
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
            self.left_field_var.trace('w', lambda *args: self.validate_field(self.left_field_var, left_entry_validation))
        if right_entry_validation:
            self.right_field_var.trace('w', lambda *args: self.validate_field(self.right_field_var, right_entry_validation))

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
