import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv("Students_Performance_Data_2.csv")

print("Dataset loaded successfully!")
print("Number of students:", len(data))

X = data[[ "Attendance","Study_Hours_per_Day", "Internal_marks", "Assignments_Avg", "Previous_preformance"]]

# Select target
y = data["Performance"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

print("Training data:", len(X_train))
print("Testing data:", len(X_test))

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create ML model
model = LogisticRegression( max_iter=50000, random_state=42 )
    
# Train model
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Regression Model Accuracy:", accuracy)

# Save trained model
joblib.dump(model, "student_regression_model.pkl")

print("Model saved successfully!")