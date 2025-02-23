import re
import bcrypt
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from kivymd.app import MDApp
import sqlite3

from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from dashboard import DashScreen
import anvil.server
from kivymd.uix.spinner import MDSpinner
from kivy.animation import Animation
from kivymd.uix.label import MDLabel

from login import LoginScreen

anvil.server.connect("server_VRGEXX5AO24374UMBBQ24XN6-ZAWBX57M6ZDN6TBV")

KV = """
<WindowManager>:
    SignupScreen:

<SignupScreen>:
    canvas.before:
        Color:
            rgba:  1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: "vertical"
        padding: dp(45)
        spacing: dp(5)

        MDLabel:
            id: label1
            text: 'SIGN UP'
            font_size:dp(30)
            halign: 'center'
            bold: True

        MDTextField:
            id: name
            hint_text: 'Enter full name'
            multiline: False
            helper_text: 'Enter a valid name'
            helper_text_mode: 'on_focus'
            icon_left: 'account'
            font_name: "Roboto-Bold"
            pos_hint: {'center_y': 0.1}

        MDTextField:
            id: mobile
            hint_text: 'Enter mobile number'
            multiline: False
            helper_text: 'Enter a valid number'
            helper_text_mode: 'on_focus'
            icon_left: 'cellphone'
            font_name: "Roboto-Bold"
            input_type: 'number'  
            on_touch_down: root.on_mobile_number_touch_down()

        MDTextField:
            id: email
            hint_text: 'Enter your email'
            multiline: False
            helper_text: 'Enter a valid email'
            helper_text_mode: 'on_focus'
            icon_left: 'email'
            font_name: "Roboto-Bold"

        MDTextField:
            id: password
            hint_text: "Enter Your Password"
            icon_left: 'lock-outline'
            helper_text_mode: 'on_focus'
            multiline: False
            helper_text: "Password must be greater than 8 characters"
            password: True
            font_name: "Roboto-Bold"

        MDTextField:
            id: password2
            hint_text: "Re-Enter Your Password"
            helper_text: "Password does not match"
            helper_text_mode: 'on_focus'
            icon_left: 'lock-outline'
            password: True
            font_name: "Roboto-Bold"

        BoxLayout:
            orientation: 'horizontal'
            width: "260dp"
            height: "10dp"
            MDCheckbox:
                id: terms_checkbox
                size_hint_x: None
                width: "20dp"
            MDLabel:
                text: "Terms and Conditions"
                theme_text_color: 'Custom'
                text_color: 6/255, 143/255, 236/255, 1
                halign: 'left'
                font_size: dp(10)
                valign: 'center'
                on_touch_down: app.root.get_screen("SignupScreen").show_terms_dialog() if self.collide_point(*args[1].pos) else None

        BoxLayout:
            orientation: 'horizontal'
            width: "260dp"
            height: "10dp"
            MDCheckbox:
                id: kyc_checkbox
                size_hint_x: None
                width: "20dp"
            MDLabel:
                text: "I authorize the company to fetch my KYC details via the Central KYC(CKYC) Registry"
                theme_text_color: 'Primary'
                font_size: dp(10)
                halign: 'left'
                valign: 'center'


        GridLayout:
            cols: 2
            spacing: dp(20)
            padding: dp(20)
            pos_hint: {'center_x': 0.50, 'center_y': 0.5}
            size_hint: 1, None
            height: "50dp"

            MDRaisedButton:
                text: "Back"
                on_release: app.root.get_screen("MainScreen").manager.current = 'MainScreen'
                md_bg_color:0.043, 0.145, 0.278, 1
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint: 1, None
                height: "50dp"
                font_name: "Roboto-Bold"

            MDRaisedButton:
                text: "Signup"
                on_release: root.go_to_login()
                md_bg_color: 0.043, 0.145, 0.278, 1
                pos_hint: {'right': 1, 'y': 0.5}
                size_hint: 1, None
                height: "50dp"
                font_name: "Roboto-Bold"

"""

# Connect to the SQLite database
conn = sqlite3.connect("fin_user_profile.db")
cursor = conn.cursor()

# Create a table named 'fin_users'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fin_users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT,
        mobile_number TEXT,
        password TEXT,
        confirm_password TEXT,
        accept_terms TEXT,  -- Column for the "Terms and Conditions" checkbox
        authorize_kyc TEXT,   -- Column for the "Authorize KYC" checkbox
        customer_status TEXT
    )
''')

# Commit the changes and close the connection
cursor.execute(''' CREATE TABLE IF NOT EXISTS fin_registration_table (
                                    customer_id INT PRIME NUMBER NOT NULL,
                                    name TEXT,
                                    gender TEXT ,
                                    date_of_birth DATE,
                                    mobile_number INT ,
                                    alternate_mobile_number TEXT,
                                    alternate_email TEXT ,
                                    profile_file TEXT,
                                    aadhar_number INT,
                                    pan_number TEXT,
                                    aadhar_file TEXT ,
                                    pan_file TEXT, 
                                    highest_qualification TEXT,
                                    tenth_certificate TEXT,
                                    inter_certificate TEXT ,
                                    bachelors_certificate TEXT ,
                                    masters_certificate TEXT,
                                    phd_certificate TEXT,
                                    street_name TEXT ,
                                    city_name TEXT,
                                    zip_code TEXT,
                                    state_name TEXT,
                                    country_name TEXT,
                                    father_name TEXT, 
                                    father_age TEXT, 
                                    father_occupation TEXT, 
                                    father_ph_no TEXT,
                                    mother_name TEXT, 
                                    mother_age TEXT, 
                                    mother_occupation TEXT, 
                                    mother_ph_no TEXT,
                                    proficient_type TEXT,
                                    college_id INT,
                                    collage_name TEXT,
                                    college_address TEXT,
                                    collage_id_file TEXT,
                                    loan_type TEXT,
                                    investment INT,
                                    lending_period TEXT,
                                    employment_type TEXT,
                                    company_name TEXT,
                                    organization_type TEXT,
                                    company_address TEXT,
                                    company_pincode TEXT,
                                    company_country TEXT,
                                    landmark TEXT,
                                    business_number INT,
                                    annual_salary INT,
                                    designation TEXT,
                                    employee_id_file TEXT,
                                    six_months_bank_statement_file TEXT,
                                    account_holder_name TEXT,
                                    account_type TEXT,
                                    account_number INT,
                                    bank_name TEXT,
                                    bank_id TEXT,
                                    salary_id TEXT,
                                    branch_name TEXT,
                                    business_name TEXT,
                                    business_location TEXT,
                                    business_address TEXT,
                                    business_branch_name TEXT,
                                    business_type TEXT,
                                    nearest_location TEXT,
                                    no_of_employees_working TEXT,
                                    year_of_estd INT,
                                    industry_type TEXT,
                                    last_six_months_turnover TEXT,
                                    last_six_months_turnover_file TEXT,
                                    director_name TEXT,
                                    director_mobile_number INT,
                                    DIN TEXT,
                                    CIN TEXT,
                                    registered_office_address TEXT,
                                    proof_of_verification_file TEXT,
                                    marital_status TEXT,
                                    spouse_name TEXT, 
                                    spouse_date_textfield DATE, 
                                    spouse_mobile TEXT, 
                                    spouse_profession TEXT,
                                    spouse_company_name TEXT,
                                    spouse_company_address TEXT, 
                                    spouse_annual_salary TEXT,
                                    spouse_office_no TEXT,
                                    user_type TEXT,
                                    customer_status TEXT
                                    )
                                ''')

# Commit the changes and close the connection
conn.commit()


class SignupScreen(Screen):
    Builder.load_string(KV)

    def on_mobile_number_touch_down(self):
        # Change keyboard mode to numeric when the mobile number text input is touched
        self.ids.mobile.input_type = 'number'

    def save_to_database(self):

        try:
            # Connect to the SQLite database
            conn = sqlite3.connect("fin_user_profile.db")
            cursor = conn.cursor()

            cursor.execute('SELECT user_id FROM fin_users ORDER BY user_id DESC LIMIT 1')
            latest_user_id = cursor.fetchone()

            c_id = anvil.server.call('profile')

            id_c = []
            for i in c_id:
                id_c.append(i['customer_id'])

            if len(id_c) >= 1:
                user_id = id_c[-1] + 1
            else:
                user_id = 1000

            if latest_user_id is not None:
                next_user_id = latest_user_id[0] + 1
            else:
                next_user_id = 1000

            hash_pashword = bcrypt.hashpw(self.ids.password.text.encode('utf-8'), bcrypt.gensalt())
            hash_pashword = hash_pashword.decode('utf-8')

            cursor.execute('''
                INSERT INTO fin_users (
                    user_id, fullname, email, mobile_number, password, confirm_password,
                    accept_terms, authorize_kyc
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                next_user_id,
                self.ids.name.text, self.ids.email.text, self.ids.mobile.text,
                hash_pashword, hash_pashword,
                "Accepted" if self.ids.terms_checkbox.active else "Rejected",
                "Accepted" if self.ids.kyc_checkbox.active else "Rejected"
            ))

            conn.commit()
            cursor.execute('''INSERT INTO fin_registration_table (customer_id) VALUES (?)''', (next_user_id,))

            self.add_data(user_id=user_id, email=self.ids.email.text, password=hash_pashword,
                          name=self.ids.name.text, number=self.ids.mobile.text, enable=True)
            conn.commit()
        except sqlite3.Error as e:

            print(f"SQLite error: {e}")

    def add_data(self, user_id, email, password, name, number, enable):
        # Ensure 'YOUR_ANVIL_UPLINK_KEY' is replaced with your actual Anvil Uplink key
        anvil.server.call('add_data', user_id, email, password, name, number, enable)

    def animate_loading_text(self, loading_label, modal_height):
        # Define the animation to move the label vertically
        anim = Animation(y=modal_height - loading_label.height, duration=1) + \
               Animation(y=0, duration=5)
        anim.bind(on_complete=lambda *args: self.animate_loading_text(loading_label,
                                                                      modal_height))  # Bind to the completion event to repeat the animation
        anim.start(loading_label)

    def go_to_login(self):
        modal_view = ModalView(size_hint=(None, None), size=(500, 200), background_color=[0, 0, 0, 0])

        # Create MDLabel with white text color, increased font size, and bold text
        loading_label = MDLabel(text="Loading...", halign="center", valign="bottom",
                                theme_text_color="Custom", text_color=[1, 1, 1, 1],
                                font_size="25sp", bold=True)

        # Set initial y-position off-screen
        loading_label.y = -loading_label.height

        modal_view.add_widget(loading_label)
        modal_view.open()

        # Perform the animation
        self.animate_loading_text(loading_label, modal_view.height)

        # Perform the actual action (e.g., fetching loan requests)
        # You can replace the sleep with your actual logic
        Clock.schedule_once(lambda dt: self.perform_signup_action(modal_view), 2)


    def perform_signup_action(self, modal_view):
        # Close the modal view after
        modal_view.dismiss()
        name = self.ids.name.text
        mobile = self.ids.mobile.text
        email = self.ids.email.text
        password = self.ids.password.text
        password2 = self.ids.password2.text
        terms_checkbox = self.ids.terms_checkbox
        kyc_checkbox = self.ids.kyc_checkbox

        # Validation errors list
        validation_errors = []

        # Regular expression for email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # Check for existing email in the database
        conn = sqlite3.connect("fin_user_profile.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM fin_users
            WHERE email = ?
        ''', (email,))
        existing_user = cursor.fetchone()

        # Check if the email already exists in the database
        if existing_user:
            validation_errors.append((self.ids.email, "Email already exists"))

        # Other input validations
        # Name validation
        if not name or not re.match(r'^[a-zA-Z\s]{4,}$', name):
            validation_errors.append((self.ids.name, "Please enter a valid name"))

        # Mobile number validation
        if not mobile or not (len(mobile) == 10 or len(mobile) == 12) or not mobile.startswith(('6', '7', '8', '9')):
            validation_errors.append((self.ids.mobile, "Invalid mobile number"))

        # Email validation
        if not email or not re.match(email_regex, email):
            validation_errors.append((self.ids.email, "Invalid email address"))

        # Password validation
        if not password or not self.is_strong_password(password):
            validation_errors.append((self.ids.password, "Please set a strong password"))

        # Confirm password validation
        if not password2 or password != password2:
            validation_errors.append((self.ids.password2, "Passwords do not match"))

        # Terms and Conditions checkbox validation
        if not terms_checkbox.active:
            validation_errors.append((terms_checkbox, "Please accept the Terms and Conditions"))

        # KYC checkbox validation
        if not kyc_checkbox.active:
            validation_errors.append((kyc_checkbox, "Please authorize KYC details"))

        # Show validation errors if any
        for widget, error_text in validation_errors:
            self.show_validation_error(widget, error_text)

        if validation_errors:
            return

        # If no validation errors, proceed with saving to the database
        self.save_to_database()

        # Reset input fields
        self.ids.name.text = ""
        self.ids.mobile.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.password2.text = ""
        self.ids.terms_checkbox.active = False
        self.ids.kyc_checkbox.active = False

        snackbar = Snackbar(
            text="Signup Successful!",
            md_bg_color=[1, 1, 1, 1],
            pos_hint={'top': 1},
            duration=2
        )

        snackbar.open()
        self.share_email_with_anvil(email)
        # self.manager.current = 'LoginScreen'
        sm = self.manager
        lender_screen = DashScreen(name='DashScreen')
        sm.add_widget(lender_screen)
        sm.transition.direction = 'left'  # Set the transition direction explicitly
        sm.current = 'DashScreen'
    def share_email_with_anvil(self, email):
        # Make an API call to Anvil server to share the email
        anvil.server.call('share_email', email)
    def show_validation_error(self, widget, error_text):
        widget.error = True
        widget.helper_text_color = (1, 0, 0, 1)
        widget.helper_text = error_text
        widget.helper_text_mode = "on_error"
        if isinstance(widget, MDCheckbox):
            widget.theme_text_color = 'Error'

    def show_popup(self, message):
        Snackbar(text=message, md_bg_color=[1, 1, 1, 1], text_color=[0, 0, 0, 1]).open()

    def show_terms_dialog(self):
        dialog = MDDialog(
            title="Terms and Conditions",
            text="I agree with terms and conditions",
            size_hint=(0.8, 0.5),
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def is_strong_password(self, password):
        # Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter,
        # one digit, and one special character
        return len(password) >= 8 and bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=-])[A-Za-z\d!@#$%^&*()_+=-]+$', password))


    def on_pre_enter(self):
        Window.bind(on_keyboard=self.on_back_button)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.on_back_button)

    def on_back_button(self, instance, key, scancode, codepoint, modifier):

        if key == 27:
            self.go_back()
            return True
        return False

    def on_start(self):
        Window.softinput_mode = "below_target"

    def go_back(self):
        # Navigate to the previous screen with a slide transition
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'MainScreen'


class MyScreenManager(ScreenManager):
    pass