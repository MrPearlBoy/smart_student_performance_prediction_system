import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv("Students Performance Dataset.csv")

print("Dataset loaded successfully!")
print("Number of students:", len(data))

X = data[[ "Attendance,Internal_marks,Assignments_Avg,Previous_preformance,Study_Hours_per_Day"]]

# Select target
y = data["Performance"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

print("Training data:", len(X_train))
print("Testing data:", len(X_test))

# Create ML model
model = RandomForestClassifier(n_estimators=100,random_state=42)

# Train model
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save trained model
joblib.dump(model, "student_model.pkl")

print("Model saved successfully!")