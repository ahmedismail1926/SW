from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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