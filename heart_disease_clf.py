from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split

print("Heart disease")
def col_types(df):
    types = []
    for col in df.columns:
        if df[col].dtype == 'object':
            types.append('str')
        else:
            types.append('num')
    return types

df = pd.read_csv('heart_disease.csv')

types = col_types(df)
loc = 0
string_to_numeric_mapping = {}

for col in df.columns:
    if types[loc] == 'str':
        mapping = {val: idx for idx, val in enumerate(df[col].unique())}
        string_to_numeric_mapping[col] = mapping
        df[col] = df[col].map(mapping)
    loc += 1

for m in string_to_numeric_mapping:
    print(f"Column: {m}, Mapping: {string_to_numeric_mapping[m]}")


columns_to_drop = [3, 11, 13, 14]
df = df.drop(df.columns[columns_to_drop], axis=1)

y = df['Heart Disease'].values
X = df.drop('Heart Disease', axis=1).values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

RF_clf =RandomForestClassifier(max_depth=2,max_features=3, random_state=0)
RF_clf.fit(X_train, y_train)

train_score = RF_clf.score(X_train, y_train)
test_score = RF_clf.score(X_test, y_test)
print(f"Train Score: {train_score * 100:.2f}%")
print(f"Test Score: {test_score * 100:.2f}%")
ap=average_precision_score(y_test, RF_clf.predict_proba(X_test)[:, 1])
print(ap)

# def classify_Patient_heart_disease(age,gender, cholester,heart_rate, smoking, Alcohol_Intake,Exercise_Hours, Family_History, diabetes, obesity, Blood_sugar):
    
#     features = np.array([age,gender, cholester,heart_rate, smoking, Alcohol_Intake,Exercise_Hours, Family_History, diabetes, obesity, Blood_sugar]).reshape(1, -1)
#     prediction = RF_clf.predict(features)
#     return prediction[0]

# example_features = X_test[0]
# predicted_class = classify_Patient_heart_disease(*X[3])
# print(f"The predicted class is: {predicted_class}")

def classify_Patient_heart_disease(
    age, gender, cholester, heart_rate, smoking, Alcohol_Intake, 
    Exercise_Hours, Family_History, diabetes, obesity, Blood_sugar
):
    gender_map = {'Female': 0, 'Male': 1}
    smoking_map = {'Current': 0, 'Never': 1, 'Former': 2}
    alcohol_map = {'Heavy': 0, None: 1, 'Moderate': 2}
    family_history_map = {'No': 0, 'Yes': 1}
    diabetes_map = {'No': 0, 'Yes': 1}
    obesity_map = {'Yes': 0, 'No': 1}
    
    try:
        gender = gender_map[gender]
        smoking = smoking_map[smoking]
        Alcohol_Intake = alcohol_map.get(Alcohol_Intake, 1)  # Use default for missing
        Family_History = family_history_map[Family_History]
        diabetes = diabetes_map[diabetes]
        obesity = obesity_map[obesity]
    except KeyError as e:
        raise ValueError(f"Invalid input for categorical variable: {e}")
    
    try:
        age = float(age)
        cholester = float(cholester)
        heart_rate = float(heart_rate)
        Exercise_Hours = float(Exercise_Hours)
        Blood_sugar = float(Blood_sugar)
    except ValueError as e:
        raise ValueError(f"Invalid numerical input: {e}")
    
    # Prepare feature array
    features = np.array([
        age, gender, cholester, heart_rate, smoking, Alcohol_Intake,
        Exercise_Hours, Family_History, diabetes, obesity, Blood_sugar
    ]).reshape(1, -1)
    
    # Predict using the model
    prediction = RF_clf.predict(features)
    return prediction[0]



