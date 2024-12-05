from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QSpinBox,QTableWidget, QTableWidgetItem
)
import database,heart_disease_clf,hypertension_clf,stroke_clf

user_id=None

class LoginPage(QWidget):
    """Login page."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.user_id_input = QLineEdit(self)
        user_id=self.user_id_input
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
        # back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.parent.go_back)
        layout.addWidget(back_button)


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
        self.disease_combo.addItems(["Heart Disease", "hypertension", "stroke"])
        layout.addWidget(self.disease_combo)

        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.next_page)
        layout.addWidget(next_button)
        #back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.parent.go_back)
        layout.addWidget(back_button)  # Add at the end of the layout
        #diagnosis his
        # Diagnosis history label
        self.historyTable = QTableWidget(self)
        self.historyTable.setColumnCount(3)  # 3 columns: Disease Type, Diagnosis, Date
        self.historyTable.setHorizontalHeaderLabels(["Disease Type", "Diagnosis", "Date"])
        layout.addWidget(self.historyTable)



        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_diagnosis_history()

    def load_diagnosis_history(self):
        user_id = self.parent.current_user_id
        history = database.fetch_diagnosis_history(user_id)
        
        
        self.historyTable.clearContents()
        self.historyTable.setRowCount(len(history))
        for row_index, entry in enumerate(history):
            self.historyTable.setItem(row_index, 0, QTableWidgetItem(entry['disease_type']))
            self.historyTable.setItem(row_index, 1, QTableWidgetItem(str(entry['diagnosis'])))
            self.historyTable.setItem(row_index, 2, QTableWidgetItem(entry['date']))
        
        
        self.historyTable.resizeColumnsToContents()
    def next_page(self):
        selected_disease = self.disease_combo.currentText()
        if selected_disease == "Heart Disease":
            self.parent.switch_to_heart_disease_form()
        elif selected_disease == "hypertension":
            self.parent.switch_to_hypertension_form()
        elif selected_disease== "stroke":
            self.parent.switch_to_stroke_form()


class HeartDiseaseFormPage(QWidget):
    """Form page for Heart Disease attributes."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.advice_messages = {
            1: "Maintain a healthy diet, avoid smoking, exercise regularly, and consult your doctor.",
            0: "Maintain regular health check-ups and a healthy lifestyle."
        }
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

        #back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.parent.go_back)  # Connect to parent’s back method
        layout.addWidget(back_button)  # Add button to layout
        

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
        
        try:
            prediction = heart_disease_clf.classify_Patient_heart_disease(
            age=21,
            gender="Male",  # Add 'gender' to your inputs
            cholester=self.parent.heart_disease_data["cholesterol"],
            heart_rate=self.parent.heart_disease_data["heart_rate"],
            smoking=self.parent.heart_disease_data["smoking"],
            Alcohol_Intake=self.parent.heart_disease_data["alcohol"],
            Exercise_Hours=self.parent.heart_disease_data["exercise_level"],
            Family_History=self.parent.heart_disease_data["family_history"],
            diabetes=self.parent.heart_disease_data["diabetes"],
            obesity=self.parent.heart_disease_data["obesity"],
            Blood_sugar=self.parent.heart_disease_data["blood_sugar"]
            )
            # Determine advice based on the prediction result
            advice = self.advice_messages[int(prediction)]  # Access the advice dictionary
            
            # Insert the diagnosis result into the database
            database.insert_diagnosis_result(self.parent.current_user_id, "Heart Disease", int(prediction))
            
            # Display prediction result and advice
            QMessageBox.information(self, "Prediction Result", f"The model predicts: {'Positive' if int(prediction) == 1 else 'Negative'}\nAdvice: {advice}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            print("Error:", e)


class HypertensionFormPage(QWidget):
    """Form page for Hypertension attributes."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.advice_messages = {
            1: "Reduce salt intake, manage stress, exercise regularly, and monitor your blood pressure.",
            0: "Maintain a balanced diet and regular check-ups to prevent hypertension."
        }
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

       
        self.cp = QComboBox(self)
        self.cp.addItems(["asymptomatic","typical angina","atypical angina","non-anginal"])
        layout.addRow(QLabel("Chest pain:"), self.cp)

        
        self.trestbps = QSpinBox(self)
        self.trestbps.setRange(80, 200)
        layout.addRow(QLabel("resting blood pressure:"), self.trestbps)

        
        self.chol = QSpinBox(self)
        self.chol.setRange(50, 200)
        layout.addRow(QLabel("Chol level:"), self.chol)

       
        self.fbs = QComboBox(self)
        self.fbs.addItems(['No','Yes'])
        layout.addRow(QLabel("fasting blood sugar:"), self.fbs)

        
        self.restecg = QComboBox(self)
        self.restecg.addItems(['normal','ST-T wave abnormality','left ventricular hypertrophy'])
        layout.addRow(QLabel("Resting ECG"), self.restecg)

        
        self.thelach = QSpinBox(self)
        self.thelach.setRange(80,200)
        layout.addRow(QLabel("Minimum heart rate achieved"), self.thelach)
        
        self.exang = QComboBox(self)
        self.exang.addItems(['No','Yes'])
        layout.addRow(QLabel("Exercise induced angina:"), self.exang)
        self.oldpeak = QSpinBox(self)
        self.oldpeak.setRange(0,5)
        layout.addRow(QLabel("ST depression induced by exercise relative to rest:"), self.oldpeak)

        
        self.slope = QComboBox(self)
        self.slope.addItems(["Upsloping","Flat"," Downsloping"])
        layout.addRow(QLabel(" peak exercise ST segment:"), self.slope)
        
        self.ca=QSpinBox(self)
        self.ca.setRange(0,3)
        layout.addRow(QLabel("Calcium:"),self.ca)
        
        self.thal = QComboBox(self)
        self.thal.addItems(["Normal","Fixed defect"," Reversible defect"])
        layout.addRow(QLabel("Thalassemia type:"), self.thal)

        
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_attributes)
        layout.addWidget(save_button)
        #back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.parent.go_back)  # Connect to parent’s back method
        layout.addWidget(back_button)  # Add button to layout
        

        self.setLayout(layout)

    def save_attributes(self):
        self.parent.hypertension_data ={
            "chest pain":self.cp.currentText(),
            "trestbps":self.trestbps.value(),
            "cholestrol level":self.chol.value(),
            "fbs":self.fbs.currentText(),
            "Resting ECG":self.restecg.currentText(),
            "the lach":self.thelach.value(),
            "exang":self.exang.currentText(),
            "oldpeak":self.oldpeak.value(),
            "slope":self.slope.currentText(),
            "ca":self.ca.value(),
            "thal":self.thal.currentText()
        }
        QMessageBox.information(self, "Success", "Attributes saved!")
        print(self.parent.heart_disease_data)
        # try:
        prediction = hypertension_clf.classify_Patient_hypertension(
        age=57,  # Example: Assuming age is 20
        cp=self.parent.hypertension_data["chest pain"],
        trestbps=self.parent.hypertension_data["trestbps"],
        chol=self.parent.hypertension_data["cholestrol level"],
        fbs=self.parent.hypertension_data["fbs"],
        restecg=self.parent.hypertension_data["Resting ECG"],
        thalach=self.parent.hypertension_data["the lach"],
        exang=self.parent.hypertension_data["exang"],
        oldpeak=self.parent.hypertension_data["oldpeak"],
        slope=self.parent.hypertension_data["slope"],
        ca=self.parent.hypertension_data["ca"],
        thal=self.parent.hypertension_data["thal"]
        )
            # Determine advice based on the prediction result
        advice = self.advice_messages[int(prediction)]  # Access the advice dictionary

        # Insert the diagnosis result into the database
        database.insert_diagnosis_result(self.parent.current_user_id, "Hypertension", int(prediction))
        
        # Display prediction result and advice
        QMessageBox.information(self, "Prediction Result", f"The model predicts: {'Positive' if int(prediction) == 1 else 'Negative'}\nAdvice: {advice}")


class StrokeFormPage(QWidget):
    """Form page for Stroke attributes."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.advice_messages = {
            1: "Control risk factors like hypertension and diabetes, avoid smoking, and stay physically active.",
            0: "Maintain a healthy lifestyle to prevent stroke risks in the future."
        }
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.hypertension_input = QComboBox(self)
        self.hypertension_input.addItems(["No", "Yes"])
        layout.addRow(QLabel("Hypertension:"), self.hypertension_input)

        self.heart_disease_input = QComboBox(self)
        self.heart_disease_input.addItems(["No", "Yes"])
        layout.addRow(QLabel("Heart Disease:"), self.heart_disease_input)

        self.married_input = QComboBox(self)
        self.married_input.addItems(["No", "Yes"])
        layout.addRow(QLabel("Ever Married:"), self.married_input)

        self.avg_glucose_input = QSpinBox(self)
        self.avg_glucose_input.setRange(50, 400)
        layout.addRow(QLabel("Average Glucose Level:"), self.avg_glucose_input)

        self.work_type_input = QComboBox(self)
        self.work_type_input.addItems(["Never_worked", "children", "Govt_job", "Self-employed", "Private"])
        layout.addRow(QLabel("Work Type:"), self.work_type_input)

        self.residence_type_input = QComboBox(self)
        self.residence_type_input.addItems(["Rural", "Urban"])
        layout.addRow(QLabel("residence Type:"), self.residence_type_input)


        self.bmi_input = QSpinBox(self)
        self.bmi_input.setRange(10, 50)
        layout.addRow(QLabel("BMI:"), self.bmi_input)

        self.smoking_status_input = QComboBox(self)
        self.smoking_status_input.addItems(["No", "Yes"])
        layout.addRow(QLabel("Smoking Status:"), self.smoking_status_input)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_attributes)
        layout.addWidget(save_button)
        #back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.parent.go_back)  # Connect to parent’s back method
        layout.addWidget(back_button)  # Add button to layout
        
        self.setLayout(layout)

    def save_attributes(self):
        self.parent.stroke_data = {
            "hypertension": self.hypertension_input.currentText(),
            "heart_disease": self.heart_disease_input.currentText(),
            "ever_married": self.married_input.currentText(),
            "work type":self.work_type_input.currentText(),
            "residence": self.residence_type_input.currentText(),
            "avg_glucose_level": self.avg_glucose_input.value(),
            "bmi": self.bmi_input.value(),
            "smoking_status": self.smoking_status_input.currentText(),
        }
        QMessageBox.information(self, "Success", "Attributes saved!")
        print(self.parent.stroke_data)
        prediction=stroke_clf.classify_Patient_stroke(
        sex="male",
        age =63,
        hypertension = self.parent.stroke_data["hypertension"],
        heart_disease = self.parent.stroke_data["heart_disease"],
        ever_married = self.parent.stroke_data["ever_married"],
        work_type=self.parent.stroke_data["work type"],
        Residence_type=self.parent.stroke_data["residence"],
        avg_glucose_level = self.parent.stroke_data["avg_glucose_level"],
        bmi = self.parent.stroke_data["bmi"],
        smoking_status = self.parent.stroke_data["smoking_status"])
        # Determine advice based on the prediction result
        advice = self.advice_messages[int(prediction)]  # Access the advice dictionary

        # Insert the diagnosis result into the database
        database.insert_diagnosis_result(self.parent.current_user_id, "Stroke", int(prediction))
        
        # Display prediction result and advice
        QMessageBox.information(self, "Prediction Result", f"The model predicts: {'Positive' if int(prediction) == 1 else 'Negative'}\nAdvice: {advice}")

class MainApp(QStackedWidget):
    """Main application managing multiple pages."""
    def __init__(self):
        super().__init__()
        self.current_user_id = None
        self.heart_disease_data = {}
        self.hypertension_data={}
        self.stroke_data={}
        self.page_history=[] # teh stack to store the his
        self.login_page = LoginPage(self)
        self.sign_up_page = SignUpPage(self)
        self.disease_choice_page = DiseaseChoicePage(self)
        self.heart_disease_form_page = HeartDiseaseFormPage(self)
        self.hypertension_form_page=HypertensionFormPage(self)
        self.stroke_form_page=StrokeFormPage(self)

        self.addWidget(self.login_page)
        self.addWidget(self.sign_up_page)
        self.addWidget(self.disease_choice_page)
        self.addWidget(self.heart_disease_form_page)
        self.addWidget(self.hypertension_form_page)
        self.addWidget(self.stroke_form_page)
        self.setCurrentWidget(self.login_page)

    def switch_to_sign_up(self):
        self.setCurrentWidget(self.sign_up_page)

    def switch_to_login(self):
        self.setCurrentWidget(self.login_page)

    def switch_to_disease_choice(self):
        self.setCurrentWidget(self.disease_choice_page)

    def switch_to_heart_disease_form(self):
        self.setCurrentWidget(self.heart_disease_form_page)

    def switch_to_hypertension_form(self):
        self.setCurrentWidget(self.hypertension_form_page)
    def switch_to_stroke_form(self):
        self.setCurrentWidget(self.stroke_form_page)
    def setCurrentWidget(self, widget):
        """Override setCurrentWidget to store history."""
        if self.currentWidget() != widget:
            self.page_history.append(self.currentWidget())  # Store current page before switching
        super().setCurrentWidget(widget)
    def go_back(self):
        """Switch to the previous page."""
        if self.page_history:
            previous_page = self.page_history.pop()
            super().setCurrentWidget(previous_page)
        else:
            print("No previous page to go back to.")  # Or handle differently
if __name__ == "__main__":
    import sys
    database.create_table()  

    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle("Disease Diagnosis System")
    main_app.resize(400, 600)
    main_app.show()
   # print("user age is ",database.get_user_age(self.user_id))
   # print("user sex is",database.get_user_sex)
    sys.exit(app.exec_())