import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import EditedNearestNeighbours
import numpy as np
print("stroke")
def col_types(df):
    types = []
    for col in df.columns:
        if df[col].dtype == 'object':
            types.append('str')
        else:
            types.append('num')
    return types

df = pd.read_csv('stroke.csv')

# columns_to_drop = [0,5,6]
# df = df.drop(df.columns[columns_to_drop], axis=1)
print("Original shape:", df.shape)
df = df.dropna()  # Drop rows with missing values
df = df.drop_duplicates()  # Remove duplicate rows
# df = df.drop('Patient ID', axis=1)
print("Cleaned shape:", df.shape)

# Convert string/categorical columns to numeric
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

y = df['stroke'].values
X = df.drop('stroke', axis=1).values

counts = dict(zip(*np.unique(y, return_counts=True)))
print("Class distribution before cleaning:", counts)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

RF_clf =RandomForestClassifier(max_depth=12,max_features=7, random_state=0)
RF_clf.fit(X_train, y_train)
train_score = RF_clf.score(X_train, y_train)
val_score = RF_clf.score(X_test, y_test)
ap=average_precision_score(y_test, RF_clf.predict_proba(X_test)[:, 1])
print(train_score)
print(val_score)
print(ap)


def classify_Patient_stroke(sex, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status):
    # Convert sex to numerical value (assuming 'male' as 1 and 'female' as 0)
    sex = 1 if sex == "Male" else 0
    
    # Convert hypertension and heart_disease to 1 or 0 (Yes: 1, No: 0)
    hypertension = 1 if hypertension == "Yes" else 0
    heart_disease = 1 if heart_disease == "Yes" else 0
    
    # Convert ever_married to 1 or 0 (married: 1, not married: 0)
    ever_married = 1 if ever_married == "Yes" else 0
    
    # Convert work_type to corresponding numeric values based on the given mapping
    work_type_mapping = {
        "Never_worked": 0,
        "children": 1,
        "Govt_job": 2,
        "Self-employed": 3,
        "Private": 4
    }
    work_type = work_type_mapping.get(work_type, -1)  # Default to -1 if invalid input
    
    # Convert Residence_type to 1 for Urban, 0 for Rural
    Residence_type = 1 if Residence_type == "Urban" else 0
    
    # Convert smoking_status to 1 (smokes) or 0 (never smoked)
    smoking_status = 1 if smoking_status == "smokes" else 0
    
    sample = np.array([sex, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status]).reshape(1, -1)
    prediction = RF_clf.predict(sample)
    
    return prediction[0]


