import tkinter as tk
from tkinter import filedialog, messagebox
import joblib
import numpy as np
import pandas as pd
import os
from ai import ai_feedback

# Global Settings
MODEL_PATH = "student_regression_model.pkl" 
MASTER_CSV_FILE = "student_prediction.csv"
FEATURE_COLS = ["Attendance", "StudyHours", "InternalMarks", "Assignment", "PreviousPerformance"]
ALL_COLUMNS = ["StudentID", "Name", "Attendance", "StudyHours", "InternalMarks", "Assignment", "PreviousPerformance"]
RECORD_COLUMNS = ALL_COLUMNS + ["Predicted_Result", "Risk_Level"]

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model: {e}")

root = tk.Tk()
root.geometry("1200x850")
root.title("Smart Student Performance Prediction System")
root.resizable(True, True)

# ---  Functions ---

def calculate_risk(prediction_score):
    """Determine risk category based on the predicted score or grade."""
    if isinstance(prediction_score, (int, float, np.floating, np.integer)):
        if prediction_score < 50:
            return "High Risk"
        elif prediction_score < 65:
            return "Moderate Risk"
        else:
            return "Low Risk"
    else:
        if str(prediction_score).lower() in ["fail", "low", "poor", "at risk"]:
            return "High Risk"
        return "Low Risk"


def append_to_master_csv(df_to_add):
    """Safely append any DataFrame row-by-row to the unified master CSV file."""
    if not os.path.exists(MASTER_CSV_FILE):
        df_to_add.to_csv(MASTER_CSV_FILE, mode='w', header=True, index=False)
    else:
        df_to_add.to_csv(MASTER_CSV_FILE, mode='a', header=False, index=False)


def validate_inputs():
    """Validate entry fields and return a clean dictionary of values."""
    student_id = StuId.get().strip()
    student_name = StuName.get().strip()
    attendance = Atten.get().strip()
    study_hours = StdyHrs.get().strip()
    internal_marks = IAMarks.get().strip()
    assignment = Assg.get().strip()
    previous_performance = PrePerf.get().strip()

    # Check empty fields
    if not all([student_id, student_name, attendance, study_hours, internal_marks, assignment, previous_performance]):
        messagebox.showwarning("Missing Information", "Please fill in all the fields.")
        return None

    # Check ID is numeric
    if not student_id.isdigit():
        messagebox.showerror("Invalid Student ID", "Student ID must contain numbers only.")
        return None

    # Check Name is alphabetic
    if not all(char.isalpha() or char.isspace() for char in student_name):
        messagebox.showerror("Invalid Student Name", "Student Name must contain alphabets only.")
        return None

    # Validate numeric ranges
    try:
        attendance = float(attendance)
        study_hours = float(study_hours)
        internal_marks = float(internal_marks)
        assignment = float(assignment)
        previous_performance = float(previous_performance)
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Attendance, Study Hours, Internal Marks, Assignment Completion, "
            "and Previous Performance must be numbers."
        )
        return None

    if not (0 <= attendance <= 100):
        messagebox.showerror("Invalid Attendance", "Attendance must be between 0 and 100.")
        return None

    if not (0 <= internal_marks <= 100):
        messagebox.showerror("Invalid Internal Marks", "Internal marks must be between 0 and 100.")
        return None

    if not (0 <= assignment <= 100):
        messagebox.showerror("Invalid Assignment", "Assignment completion must be between 0 and 100.")
        return None

    if not (0 <= previous_performance <= 100):
        messagebox.showerror("Invalid Previous Performance", "Previous performance must be between 0 and 100.")
        return None

    if not (0 <= study_hours <= 24):
        messagebox.showerror("Invalid Study Hours", "Study hours must be between 0 and 24 hours.")
        return None

    return {
        "StudentID": student_id,
        "Name": student_name,
        "Attendance": attendance,
        "StudyHours": study_hours,
        "InternalMarks": internal_marks,
        "Assignment": assignment,
        "PreviousPerformance": previous_performance
    }


# --- Button Actions ---

def load_data_to_csv():
    """Manually append records to the master CSV file without running prediction."""
    has_single_input = any([
        StuId.get().strip(),
        StuName.get().strip(),
        Atten.get().strip(),
        StdyHrs.get().strip(),
        IAMarks.get().strip(),
        Assg.get().strip(),
        PrePerf.get().strip()
    ])

    if has_single_input:
        data = validate_inputs()
        if data is None:
            return

        try:
            new_row = pd.DataFrame([data])
            append_to_master_csv(new_row)
            messagebox.showinfo("Success", f"Student record added to '{MASTER_CSV_FILE}' successfully.")
        except Exception as err:
            messagebox.showerror("File Error", f"Failed to save data:\n{err}")

    else:
        file_path = filedialog.askopenfilename(
            title="Select Batch CSV File to Import",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)
            missing = [col for col in ALL_COLUMNS if col not in df.columns]
            if missing:
                messagebox.showerror(
                    "Missing Columns",
                    f"Selected file is missing required columns:\n{', '.join(missing)}"
                )
                return

            append_to_master_csv(df[ALL_COLUMNS])
            messagebox.showinfo("Success", f"{len(df)} records appended to '{MASTER_CSV_FILE}'.")
        except Exception as err:
            messagebox.showerror("Import Error", f"Failed to import batch file:\n{err}")


def predict_performance():
    """Predict performance, calculate risk level, and append to the master CSV."""
    if model is None:
        messagebox.showerror("Model Error", "ML Model (.pkl) is not loaded.")
        return

    data = validate_inputs()
    if data is None:
        return

    features = np.array([[
        data["Attendance"],
        data["StudyHours"],
        data["InternalMarks"],
        data["Assignment"],
        data["PreviousPerformance"]
    ]])

    try:
        prediction = model.predict(features)[0]

        if isinstance(prediction, (int, float, np.floating, np.integer)):
            pred_score = round(float(prediction), 2)
            pred_text = f"{pred_score:.2f}%"
        else:
            pred_score = prediction
            pred_text = f"{pred_score}"

        # Calculate Risk Level
        risk_level = calculate_risk(pred_score)
        advice = ai_feedback(risk_level=risk_level, attendance=data["Attendance"], study_hours=data["StudyHours"],internal_marks=data["InternalMarks"])

        prediction_value.config(text=f"Prediction ({data['Name']}): {pred_text}")
        risk_value.config(text=f"Risk Level: {risk_level}")
        recommendation_value.config(text=f"Recommendation: {advice}")
       

        record = dict(data)
        record["Predicted_Result"] = pred_score
        record["Risk_Level"] = risk_level
        
        df_single = pd.DataFrame([record])
        append_to_master_csv(df_single)

        messagebox.showinfo("Saved", f"Prediction and Risk Level saved to '{MASTER_CSV_FILE}'.")

    except Exception as err:
        messagebox.showerror("Prediction Error", f"Inference failed:\n{err}")


def predict_csv_file():
    """Predict performance & risk for an entire batch CSV and append to master CSV."""
    if model is None:
        messagebox.showerror("Model Error", "ML Model (.pkl) is not loaded.")
        return

    file_path = filedialog.askopenfilename(
        title="Select Batch CSV Dataset for Prediction",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)

        # Verify required feature columns
        missing_features = [col for col in FEATURE_COLS if col not in df.columns]
        if missing_features:
            messagebox.showerror(
                "Missing Columns",
                f"Selected CSV is missing required feature columns:\n{', '.join(missing_features)}"
            )
            return

        # Perform predictions and calculate risk
        features = df[FEATURE_COLS].values
        preds = model.predict(features)
        
        df["Predicted_Result"] = [
            round(float(p), 2) if isinstance(p, (int, float, np.floating, np.integer)) else p 
            for p in preds
        ]
        df["Risk_Level"] = [calculate_risk(p) for p in df["Predicted_Result"]]

        # Select columns to append to master CSV
        cols_to_save = [col for col in ALL_COLUMNS if col in df.columns] + ["Predicted_Result", "Risk_Level"]
        append_to_master_csv(df[cols_to_save])

        messagebox.showinfo(
            "Success",
            f"{len(df)} predictions with risk levels appended row-by-row into '{MASTER_CSV_FILE}'."
        )

    except Exception as err:
        messagebox.showerror("CSV Processing Error", f"Failed to process and append records:\n{err}")


def clear_fields():
    """Clear all input and output fields."""
    StuId.delete(0, tk.END)
    StuName.delete(0, tk.END)
    Atten.delete(0, tk.END)
    StdyHrs.delete(0, tk.END)
    IAMarks.delete(0, tk.END)
    Assg.delete(0, tk.END)
    PrePerf.delete(0, tk.END)

    prediction_value.config(text="Prediction:")
    risk_value.config(text="Risk Level:")
    recommendation_value.config(text="Recommendation:")
    StuId.focus()


def exit_application():
    """Ask confirmation before closing."""
    if messagebox.askyesno("Exit Application", "Are you sure you want to exit?"):
        root.destroy()


# --- UI Layout ---

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=40, pady=25)

heading1 = tk.Label(main_frame, text="Smart Student Performance Prediction System", font=("Times New Roman", 20, "bold"))
heading1.pack(pady=(10, 20))

input_frame = tk.Frame(main_frame)
input_frame.pack(fill="x", pady=10)

# Student Information Frame
student_frame = tk.LabelFrame(input_frame, text="Student Information", font=("Times New Roman", 14, "bold"), padx=20, pady=15)
student_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

student_id_frame = tk.Frame(student_frame)
student_id_frame.pack(fill="x", pady=8)
tk.Label(student_id_frame, text="Student ID", font=("Times New Roman", 11, "bold"), width=15, anchor="w").pack(side="left")
StuId = tk.Entry(student_id_frame, font=("Times New Roman", 11))
StuId.pack(side="left", fill="x", expand=True)

student_name_frame = tk.Frame(student_frame)
student_name_frame.pack(fill="x", pady=8)
tk.Label(student_name_frame, text="Name", font=("Times New Roman", 11, "bold"), width=15, anchor="w").pack(side="left")
StuName = tk.Entry(student_name_frame, font=("Times New Roman", 11))
StuName.pack(side="left", fill="x", expand=True)

# Academic Information Frame
academic_frame = tk.LabelFrame(input_frame, text="Academic Information", font=("Times New Roman", 14, "bold"), padx=20, pady=15)
academic_frame.pack(side="left", fill="both", expand=True, padx=(15, 0))

attendance_frame = tk.Frame(academic_frame)
attendance_frame.pack(fill="x", pady=5)
tk.Label(attendance_frame, text="Attendance (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w").pack(side="left")
Atten = tk.Entry(attendance_frame, font=("Times New Roman", 11))
Atten.pack(side="left", fill="x", expand=True)

study_frame = tk.Frame(academic_frame)
study_frame.pack(fill="x", pady=5)
tk.Label(study_frame, text="Study Hours (per Day)", font=("Times New Roman", 11, "bold"), width=25, anchor="w").pack(side="left")
StdyHrs = tk.Entry(study_frame, font=("Times New Roman", 11))
StdyHrs.pack(side="left", fill="x", expand=True)

internal_frame = tk.Frame(academic_frame)
internal_frame.pack(fill="x", pady=5)
tk.Label(internal_frame, text="Internal Marks (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w").pack(side="left")
IAMarks = tk.Entry(internal_frame, font=("Times New Roman", 11))
IAMarks.pack(side="left", fill="x", expand=True)

assignment_frame = tk.Frame(academic_frame)
assignment_frame.pack(fill="x", pady=5)
tk.Label(assignment_frame, text="Assignment Completion (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w").pack(side="left")
Assg = tk.Entry(assignment_frame, font=("Times New Roman", 11))
Assg.pack(side="left", fill="x", expand=True)

previous_frame = tk.Frame(academic_frame)
previous_frame.pack(fill="x", pady=5)
tk.Label(previous_frame, text="Previous Performance (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w").pack(side="left")
PrePerf = tk.Entry(previous_frame, font=("Times New Roman", 11))
PrePerf.pack(side="left", fill="x", expand=True)

# Button Frame
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=20)

load_btn = tk.Button(button_frame, text="Load to CSV", command=load_data_to_csv, font=("Times New Roman", 11, "bold"), width=14, fg="purple")
load_btn.pack(side="left", padx=8)

predict_btn = tk.Button(button_frame, text="Predict Entry", command=predict_performance, font=("Times New Roman", 11, "bold"), width=14, fg="blue")
predict_btn.pack(side="left", padx=8)

predict_file_btn = tk.Button(button_frame, text="Predict CSV File", command=predict_csv_file, font=("Times New Roman", 11, "bold"), width=16, fg="darkblue")
predict_file_btn.pack(side="left", padx=8)

clear_btn = tk.Button(button_frame, text="Clear", command=clear_fields, font=("Times New Roman", 11, "bold"), width=10, fg="green")
clear_btn.pack(side="left", padx=8)

exit_btn = tk.Button(button_frame, text="Exit", command=exit_application, font=("Times New Roman", 11, "bold"), width=10, fg="red")
exit_btn.pack(side="left", padx=8)

# Result Frame
result_frame = tk.LabelFrame(main_frame, text="Result", font=("Times New Roman", 14, "bold"), padx=30, pady=15)
result_frame.pack(fill="x", pady=10)

prediction_value = tk.Label(result_frame, text="Prediction:", font=("Times New Roman", 12), anchor="w")
prediction_value.pack(anchor="w", pady=4)

risk_value = tk.Label(result_frame, text="Risk Level:", font=("Times New Roman", 12), anchor="w")
risk_value.pack(anchor="w", pady=4)

recommendation_value = tk.Label(result_frame, text="Recommendation:", font=("Times New Roman", 12), anchor="w", wraplength=1050, justify="left")
recommendation_value.pack(anchor="w", pady=4)

root.mainloop()