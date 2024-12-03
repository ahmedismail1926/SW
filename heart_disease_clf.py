from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split

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