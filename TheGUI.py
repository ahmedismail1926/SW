from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QSpinBox
)
import database

class LoginPage(QWidget):
    """Login page."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Enter User ID")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.clicked.connect(self.parent.switch_to_sign_up)
        layout.addWidget(sign_up_button)

        self.setLayout(layout)

    def login(self):
        user_id = self.user_id_input.text().strip()
        password = self.password_input.text().strip()
        user_data = database.fetch_user_data(user_id, password)

        if user_data:
            QMessageBox.information(self, "Login Successful", f"Welcome {user_id}!")
            self.parent.current_user_id = user_id
            self.parent.switch_to_disease_choice()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid User ID or Password")


class SignUpPage(QWidget):
    """Sign-up page mimicking login experience."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("Create User ID")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Create Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.age_input = QSpinBox(self)
        self.age_input.setRange(1, 120)  
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_input)

        self.sex_input = QComboBox(self)
        self.sex_input.addItems(['1', '0'])  
        layout.addWidget(QLabel("Sex (1 for male   , 0 for female):"))
        layout.addWidget(self.sex_input)

        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.clicked.connect(self.sign_up)
        layout.addWidget(sign_up_button)

        self.setLayout(layout)
    def sign_up(self):
        user_id = self.user_id_input.text().strip()
        password = self.password_input.text().strip()
        age = self.age_input.value()
        sex = self.sex_input.currentText()

        if user_id and password:
            if database.insert_user_data(user_id, password, age, sex):
                QMessageBox.information(self, "Sign Up Successful", "You can now log in.")
                self.parent.switch_to_login()
            else:
                QMessageBox.warning(self, "Sign Up Failed", "User ID already exists. Please choose a different User ID.")
        else:
            QMessageBox.critical(self, "Error", "All fields are required!")


class DiseaseChoicePage(QWidget):
    """Page to choose disease."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Choose a disease to check:"))

        self.disease_combo = QComboBox(self)
        self.disease_combo.addItems(["Heart Disease", "Disease 2", "Disease 3"])
        layout.addWidget(self.disease_combo)

        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.next_page)
        layout.addWidget(next_button)

        self.setLayout(layout)

    def next_page(self):
        selected_disease = self.disease_combo.currentText()
        if selected_disease == "Heart Disease":
            self.parent.switch_to_heart_disease_form()


class HeartDiseaseFormPage(QWidget):
    """Form page for Heart Disease attributes."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

       
        self.cholesterol_input = QSpinBox(self)
        self.cholesterol_input.setRange(100, 500)
        layout.addRow(QLabel("Cholesterol Level:"), self.cholesterol_input)

        
        self.bp_input = QSpinBox(self)
        self.bp_input.setRange(80, 200)
        layout.addRow(QLabel("Blood Pressure:"), self.bp_input)

        
        self.heart_rate_input = QSpinBox(self)
        self.heart_rate_input.setRange(50, 200)
        layout.addRow(QLabel("Heart Rate:"), self.heart_rate_input)

       
        self.smoking_input = QComboBox(self)
        self.smoking_input.addItems(["Former", "Current", "Never"])
        layout.addRow(QLabel("Smoking Status:"), self.smoking_input)

        
        self.alcohol_input = QComboBox(self)
        self.alcohol_input.addItems(["Heavy", "Moderate", "None"])
        layout.addRow(QLabel("Alcohol Intake:"), self.alcohol_input)

        
        self.exercise_input = QSpinBox(self)
        self.exercise_input.setRange(1, 9)
        layout.addRow(QLabel("Exercise Level (1-9):"), self.exercise_input)

        
        self.family_history_input = QComboBox(self)
        self.family_history_input.addItems(["Yes", "No"])
        layout.addRow(QLabel("Family History:"), self.family_history_input)

        
        self.diabetes_input = QComboBox(self)
        self.diabetes_input.addItems(["Yes", "No"])
        layout.addRow(QLabel("Diabetes:"), self.diabetes_input)

        
        self.obesity_input = QComboBox(self)
        self.obesity_input.addItems(["Yes", "No"])
        layout.addRow(QLabel("Obesity:"), self.obesity_input)

        
        self.blood_sugar_input = QSpinBox(self)
        self.blood_sugar_input.setRange(70, 300)
        layout.addRow(QLabel("Blood Sugar Level:"), self.blood_sugar_input)

        
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_attributes)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_attributes(self):
        self.parent.heart_disease_data = {
            "cholesterol": self.cholesterol_input.value(),
            "blood_pressure": self.bp_input.value(),
            "heart_rate": self.heart_rate_input.value(),
            "smoking": self.smoking_input.currentText(),
            "alcohol": self.alcohol_input.currentText(),
            "exercise_level": self.exercise_input.value(),
            "family_history": self.family_history_input.currentText(),
            "diabetes": self.diabetes_input.currentText(),
            "obesity": self.obesity_input.currentText(),
            "blood_sugar": self.blood_sugar_input.value(),
        }
        QMessageBox.information(self, "Success", "Attributes saved!")
        print(self.parent.heart_disease_data)


class MainApp(QStackedWidget):
    """Main application managing multiple pages."""
    def __init__(self):
        super().__init__()
        self.current_user_id = None
        self.heart_disease_data = {}

        self.login_page = LoginPage(self)
        self.sign_up_page = SignUpPage(self)
        self.disease_choice_page = DiseaseChoicePage(self)
        self.heart_disease_form_page = HeartDiseaseFormPage(self)

        self.addWidget(self.login_page)
        self.addWidget(self.sign_up_page)
        self.addWidget(self.disease_choice_page)
        self.addWidget(self.heart_disease_form_page)

        self.setCurrentWidget(self.login_page)

    def switch_to_sign_up(self):
        self.setCurrentWidget(self.sign_up_page)

    def switch_to_login(self):
        self.setCurrentWidget(self.login_page)

    def switch_to_disease_choice(self):
        self.setCurrentWidget(self.disease_choice_page)

    def switch_to_heart_disease_form(self):
        self.setCurrentWidget(self.heart_disease_form_page)


if __name__ == "__main__":
    import sys
    database.create_table()  

    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle("Disease Diagnosis System")
    main_app.resize(400, 600)
    main_app.show()
    sys.exit(app.exec_())
