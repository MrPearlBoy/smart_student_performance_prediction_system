import tkinter as tk
from tkinter import messagebox
from ssi import calculate_performance(attendance, study_hours, internal_marks, assignment), calculate_level(score), recommendation(level), display_result(name, score, level, advice)

root = tk.Tk()

root.geometry("1200x800")
root.title("Smart student performance prediction system")
root.resizable(True, True)

# Functions

def predict_performance():
    """Predict student performance based on entered academic data."""

    # Get values
    student_id = StuId.get().strip()
    student_name = StuName.get().strip()
    attendance = Atten.get().strip()
    study_hours = StdyHrs.get().strip()
    internal_marks = IAMarks.get().strip()
    assignment = Assg.get().strip()
    previous_performance = PrePerf.get().strip()

    # Check empty fields
    if not all([ student_id, student_name, attendance, study_hours, internal_marks, assignment, previous_performance ]):
        messagebox.showwarning( "Missing Information", "Please fill in all the fields.")
        return

    # check id is number only
    if not student_id.isdigit():
        messagebox.showerror( "Invalid Student ID", "Student ID must contain numbers only." )
        return

    # check name is alphabet only
    if not all(char.isalpha() or char.isspace() for char in student_name):
        messagebox.showerror( "Invalid Student Name", "Student Name must contain alphabets only." )
        return

    # Validate numeric fields
    try:
        attendance = float(attendance)
        study_hours = float(study_hours)
        internal_marks = float(internal_marks)
        assignment = float(assignment)
        previous_performance = float(previous_performance)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Attendance, Study Hours, Internal Marks,\n"
            "Assignment Completion and Previous Performance\n"
            "must contain numeric values."
        )
        return

    # Validate ranges
    if not 0 <= attendance <= 100:
        messagebox.showerror(
            "Invalid Attendance",
            "Attendance must be between 0 and 100."
        )
        return

    if not 0 <= internal_marks <= 100:
        messagebox.showerror(
            "Invalid Internal Marks",
            "Internal marks must be between 0 and 100."
        )
        return

    if not 0 <= assignment <= 100:
        messagebox.showerror(
            "Invalid Assignment",
            "Assignment completion must be between 0 and 100."
        )
        return

    if not 0 <= previous_performance <= 100:
        messagebox.showerror(
            "Invalid Previous Performance",
            "Previous performance must be between 0 and 100."
        )
        return

    if 0 < study_hours < 23 :
        messagebox.showerror(
            "Invalid Study Hours",
            "Study hours cannot be negative."
        )
        return

    score = calculate_performance (attendance, study_hours, internal_marks, assignment) 
    level = calculate_level (score)
    advice = recommendation (level)
    display_result (name, score, level, advice)


def clear_fields():
    """Clear all input and output fields."""

    StuId.delete(0, tk.END)
    StuName.delete(0, tk.END)
    Atten.delete(0, tk.END)
    StdyHrs.delete(0, tk.END)
    IAMarks.delete(0, tk.END)
    Assg.delete(0, tk.END)
    PrePerf.delete(0, tk.END)


    StuId.focus()


def exit_application():
    """Ask confirmation before closing the application."""

    answer = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()

# Main Frame

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=40, pady=30)

# Heading1

heading1 = tk.Label( main_frame, text="Smart Student Performance Prediction System", font=("Times New Roman", 20, "bold") )
heading1.pack(pady=(10, 30))

# Input Frame

input_frame = tk.Frame(main_frame)
input_frame.pack(fill="x", pady=10)

# Student Information Frame

student_frame = tk.LabelFrame( input_frame, text="Student Information", font=("Times New Roman", 14, "bold"), padx=20, pady=15 )
student_frame.pack( side="left", fill="both", expand=True, padx=(0, 15) )

# Student ID

student_id_frame = tk.Frame(student_frame)
student_id_frame.pack(fill="x", pady=8)

tk.Label( student_id_frame, text="Student ID", font=("Times New Roman", 11, "bold"), width=15, anchor="w" ).pack(side="left")
StuId = tk.Entry( student_id_frame, font=("Times New Roman", 11) )

StuId.pack( side="left", fill="x", expand=True )

# Student Name

student_name_frame = tk.Frame(student_frame)
student_name_frame.pack(fill="x", pady=8)

tk.Label( student_name_frame, text="Name", font=("Times New Roman", 11, "bold"), width=15, anchor="w" ).pack(side="left")
StuName = tk.Entry( student_name_frame, font=("Times New Roman", 11) )

StuName.pack( side="left", fill="x", expand=True )

#Academic Information Frame

academic_frame = tk.LabelFrame( input_frame, text="Academic Information", font=("Times New Roman", 14, "bold"), padx=20,pady=15 )
academic_frame.pack( side="left", fill="both", expand=True, padx=(15, 0) )


# Attendance

attendance_frame = tk.Frame(academic_frame)
attendance_frame.pack(fill="x", pady=5)

tk.Label( attendance_frame, text="Attendance (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w" ).pack(side="left")
Atten = tk.Entry( attendance_frame, font=("Times New Roman", 11) )

Atten.pack( side="left", fill="x", expand=True )

# Study Hours

study_frame = tk.Frame(academic_frame)
study_frame.pack(fill="x", pady=5)

tk.Label( study_frame, text="Study Hours (per Day)", font=("Times New Roman", 11, "bold"), width=25, anchor="w" ).pack(side="left")
StdyHrs = tk.Entry( study_frame, font=("Times New Roman", 11) )

StdyHrs.pack( side="left", fill="x", expand=True )

# Internal Marks

internal_frame = tk.Frame(academic_frame)
internal_frame.pack(fill="x", pady=5)

tk.Label( internal_frame, text="Internal Marks (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w" ).pack(side="left")
IAMarks = tk.Entry( internal_frame, font=("Times New Roman", 11) )

IAMarks.pack( side="left", fill="x", expand=True )

# Assignment

assignment_frame = tk.Frame(academic_frame)
assignment_frame.pack(fill="x", pady=5)

tk.Label( assignment_frame, text="Assignment Completion (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w" ).pack(side="left")
Assg = tk.Entry( assignment_frame, font=("Times New Roman", 11) )

Assg.pack( side="left", fill="x", expand=True )

# Previous Performance

previous_frame = tk.Frame(academic_frame)
previous_frame.pack(fill="x", pady=5)

tk.Label(  previous_frame, text="Previous Performance (%)", font=("Times New Roman", 11, "bold"), width=25, anchor="w" ).pack(side="left") 
PrePerf = tk.Entry( previous_frame, font=("Times New Roman", 11) )

PrePerf.pack( side="left", fill="x", expand=True )

# Button Frame

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=30)

predict_btn = tk.Button( button_frame, text="Predict Performance", command=predict_performance, font=("Times New Roman", 12, "bold"), width=20, fg="blue" )
predict_btn.pack(side="left", padx=15)

clear_btn = tk.Button( button_frame, text="Clear",command=clear_fields, font=("Times New Roman", 12, "bold"), width=12, fg="green" )
clear_btn.pack(side="left", padx=15)

exit_btn = tk.Button( button_frame, text="Exit", command=exit_application, font=("Times New Roman", 12, "bold"), width=12, fg="red" )
exit_btn.pack(side="left", padx=15)

# Result Frame

result_frame = tk.LabelFrame( main_frame, text="Predicted Result", font=("Times New Roman", 14, "bold"), padx=30, pady=20 )
result_frame.pack( fill="x", pady=10 )

prediction_value = tk.Label( result_frame, text="Prediction:", font=("Times New Roman", 12), anchor="w" )
prediction_value.pack( anchor="w", pady=5 )

risk_value = tk.Label( result_frame, text="Risk Level:", font=("Times New Roman", 12), anchor="w" )
risk_value.pack( anchor="w", pady=5 )

root.mainloop()