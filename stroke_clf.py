import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import EditedNearestNeighbours
import numpy as np

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

old_X = X
old_y = y

# Apply Edited Nearest Neighbors (ENN) to remove noise
enn = EditedNearestNeighbours(n_neighbors=3)  # Using 3 nearest neighbors
X, y = enn.fit_resample(X, y)

# Print data sizes before and after noise removal
print("Original data size:", old_X.shape)
print("After noise removal:", X.shape)

# Check class distribution
original_counts = dict(zip(*np.unique(old_y, return_counts=True)))
cleaned_counts = dict(zip(*np.unique(y, return_counts=True)))
print("Class distribution before cleaning:", original_counts)
print("Class distribution after cleaning:", cleaned_counts)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

RF_clf =RandomForestClassifier(max_depth=12,max_features=7, random_state=0)
RF_clf.fit(X_train, y_train)
train_score = RF_clf.score(X_train, y_train)
val_score = RF_clf.score(X_test, y_test)
ap=average_precision_score(y_test, RF_clf.predict_proba(X_test)[:, 1])
print(train_score)
print(val_score)
print(ap)