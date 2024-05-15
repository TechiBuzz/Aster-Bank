# APP
WINDOW_TITLE = 'Tsar Bank 2.0'
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1100

# ASSETS
WINDOW_BITMAP_ICON_PATH = 'assets\\icon\\tsar_bank_icon.ico'

SMALL_DB_ICON_PATH = 'assets\\ui\\login_screen\\db_icon.png'
LOGIN_SCREEN_USER_ICON_PATH = 'assets\\ui\\login_screen\\user_icon.png'
MAIN_SCREEN_USER_ICON_PATH = 'assets\\ui\\main_screen\\user_icon.png'

BACK_ARROW_ICON_PATH = 'assets/ui/back_button.png'
WARNING_ICON_PATH = 'assets/ui/warning_icon.png'
SHOW_PASSWORD_ICON_PATH = 'assets/ui/obfuscate_widget/show_password.png'
HIDE_PASSWORD_ICON_PATH = 'assets/ui/obfuscate_widget/hide_password.png'


# FONT
WELCOME_SCREEN_WELCOME_LABEL_FONT = ('Congenial Black', 70, 'bold')
WELCOME_SCREEN_BUTTON_FONT = ('Congenial Black', 40, 'bold')

LOGIN_SCREEN_DB_STATUS_FONT = ('Calibri', 18, 'bold')

LOGIN_SCREEN_FIELD_LABEl_FONT = ('Calibri', 60, 'bold')
LOGIN_SCREEN_FIELD_ENTRY_FONT = ('Calibri', 40)
LOGIN_SCREEN_BOTTOM_BUTTON_FONT = ('Calibri', 45, 'bold')

LOGIN_SCREEN_WARNING_LABEL_FONT = ('Calibri', 22, 'bold')

SIGNUP_SCREEN_LABEL_FONT = ('Calibri', 50, 'bold')
SIGNUP_SCREEN_FIELD_ENTRY_FONT = ('Calibri', 38)
SIGNUP_SCREEN_RADIO_BUTTON_FONT = ('Calibri', 25, 'bold')
SIGNUP_SCREEN_ADDRESS_FONT = ('Calibri', 32)
SIGNUP_SCREEN_OPERATION_BUTTON_FONT =('Calibri', 30, 'bold')

MAIN_SCREEN_HEADER_FONT = ('Calibri', 50, 'bold')
MAIN_SCREEN_PANEL_FONT = ('Calibri', 40, 'bold')

# DIMENSIONS
SIDE_PANEL_BUTTON_DIMENSION = 100
SIDE_PANEL_BUTTON_CORNER_RADIUS = 18

COMMON_ENTRY_CORNER_RADIUS = 40

LOGIN_SCREEN_BOTTOM_BUTTON_WIDTH = 380
LOGIN_SCREEN_BOTTOM_BUTTON_HEIGHT = 80
LOGIN_SCREEN_BOTTOM_BUTTON_CORNER_RADIUS = 100

# COLORS
APP_COLOR_THEME = 'green'  # Available -> ['blue', 'dark-blue', 'green']

# ERRORS
LOGIN_ERRORS = {
    0: '   Username field cannot be empty!',
    1: '   Password field cannot be empty!',
    2: '   Unable to connect to the database!',
    3: '   Invalid Username or Password! Please ensure valid credentials!'
}

SIGN_UP_ERRORS = {
    0: '   First Name field cannot be empty!',
    1: '   Last Name field cannot be empty!',
    2: '   Address field cannot be empty!',
    3: '   Email field cannot be empty!',
    4: '   Phone Number field cannot be empty!',
    5: '   Password field cannot be empty!',
    6: '   Confirm Password field cannot be empty!',
    7: '   First Name must be a minimum of 3 characters!',
    8: '   Last Name must be a minimum of 1 character!',
    9: '   Address must be between 20 and 255 characters!',
    10: '   Invalid Phone Number! Please enter a 10-Digit Phone Number!',
    11: '   Password must be a minimum of 8 characters!',
    12: '   Please select a Gender option!',
    13: '   Sorry! Users under the age of 15 cannot sign up for an account!',
    14: '   Invalid Email! Please provide a valid email address!',
    15: '   Password must contain a minimum of 2 special characters!',
    16: '   Password must contain a minimum of 2 uppercase characters!',
    17: '   Password must contain a minimum of 2 numeric characters!',
    18: '   Password fields must match!',
    19: '   Unable to connect to database!',
}

# DATABASE
DB = {"HOST": "sql6.freesqldatabase.com", "DATABASE": "sql6698638", "PORT": 3306, "USER": "sql6698638", "PASSWORD": "fMqmcIIyBu"}
# FOR cmd line mysql -h sql6.freesqldatabase.com -u sql6698638 -p