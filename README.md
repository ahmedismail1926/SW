# SW
# Disease Prediction PyQt5 Application
#By Team 2
Mohamed Elsemary, 5561467
Loay Othman,5561470
Ahmed Mohamed,5561469
Youssef Tolba,5561472
Overview
This application is a PyQt5-based GUI for user registration, login, and disease-specific diagnosis prediction. It integrates machine learning models for heart disease, hypertension, and stroke classification. The system stores user data and diagnosis history in an SQLite database and provides personalized advice based on diagnosis results.

Features:
1. User Authentication
Login: Users can log in using their User ID and password.
Sign-Up: New users can create an account, specifying their age and sex.
Session Management: Users stay logged in during their session.
2. Disease Selection
After logging in, users can select one of the following diseases for prediction:

Heart Disease
Hypertension
Stroke
3. Diagnosis Forms
Each disease has its own form to input specific attributes. Upon submission, the system classifies the risk and displays personalized advice.

4. History Management
Users can view their previous diagnosis results, including disease type, diagnosis (positive or negative), and date.
Installation
Prerequisites:
Python 3.x
PyQt5
SQLite
Machine learning models (heart_disease_clf, hypertension_clf, and stroke_clf) trained and saved.
