def get_student_data():
    name = input("Enter student name: ")
    attendance = float(input("Enter attendance: "))
    study_hours = float(input("Enter study hours: "))
    internal_marks = float(input("Enter internal marks: "))
    assignment = float(input("Enter assignment completion: "))

    return name, attendance, study_hours, internal_marks, assignment


def calculate_performance(attendance, study_hours, internal_marks, assignment):
    study_score = study_hours * 20

    performance = attendance * 0.20 + study_score * 0.20 + internal_marks * 0.40 + assignment * 0.20

    return performance


def calculate_level(score):
    if score >= 85:
        return "EXCELLENT"
    elif score >= 70:
        return "GOOD"
    elif score >= 50:
        return "AVERAGE"
    else:
        return "AT RISK"


def recommendation(level):
    if level == "EXCELLENT":
        return "Keep up the good work."

    elif level == "GOOD":
        return "Maintain attendance and continue regular study."

    elif level == "AVERAGE":
        return "Try to increase study hours and improve marks."

    else:
        return "Improve attendance and study regularly."


def display_result(name, score, level, advice):
    print("\nStudent Name:", name)
    print("Performance Score:", round(score, 2))
    print("Performance Level:", level)
    print("Recommendation:", advice)


if __name__ == "__main__":

    name, attendance, study_hours, internal_marks, assignment = get_student_data()

    score = calculate_performance(
        attendance,
        study_hours,
        internal_marks,
        assignment
    )

    level = calculate_level(score)

    advice = recommendation(level)

    display_result(name, score, level, advice)
