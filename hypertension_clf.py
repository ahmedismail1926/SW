from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

print("hypertension")
df = pd.read_csv('hypertension.csv')

columns_to_drop = [1]
df = df.drop(df.columns[columns_to_drop], axis=1)

y = df['target'].values
X = df.drop('target', axis=1).values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

knn_clf = KNeighborsClassifier(n_neighbors=4)
knn_clf.fit(X_train, y_train)
train_score = knn_clf.score(X_train, y_train)
test_score = knn_clf.score(X_test, y_test)
print(train_score)
print(test_score)
ap=average_precision_score(y_test, knn_clf.predict_proba(X_test)[:, 1])
print(ap)

def classify_Patient_hypertension(age, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    """
    Convert string inputs to numerical values based on the mapping and classify hypertension.
    """
    # Mappings
    cp_mapping = {'asymptomatic': 0, 'typical angina': 1, 'atypical angina': 2, 'non-anginal': 3}
    fbs_mapping = {'Yes': 1, 'No': 0}
    restecg_mapping = {'normal': 0, 'ST-T wave abnormality': 1, 'left ventricular hypertrophy': 2}
    exang_mapping = {'Yes': 1, 'No': 0}
    slope_mapping = {'Upsloping': 0, 'Flat': 1, 'Downsloping': 2}
    thal_mapping = {'Normal': 0, 'Fixed defect': 1, 'Reversible defect': 2}

    # Convert string inputs to numbers
    cp = cp_mapping[cp]
    fbs = fbs_mapping[fbs]
    restecg = restecg_mapping[restecg]
    exang = exang_mapping[exang]
    slope = slope_mapping[slope]
    thal = thal_mapping[thal]

    # Convert inputs to numpy array
    features = np.array([age, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]).reshape(1, -1)

    # Predict using the model
    prediction = knn_clf.predict(features)
    return prediction[0]




