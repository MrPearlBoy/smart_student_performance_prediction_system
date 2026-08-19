def calculate_performance(attendance, study_hours, internal_marks, assignment, previous_performance):

    study_score = min((study_hours / 8) * 100, 100)

    performance = ( attendance * 0.20 + study_score * 0.15 + internal_marks * 0.25 + assignment * 0.15 + previous_performance * 0.25 )

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