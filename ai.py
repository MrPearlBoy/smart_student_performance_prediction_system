def ai_feedback(risk_level, attendance, study_hours, internal_marks):
    suggestions = []

    # 1. Base advice on Risk Level
    if risk_level == "High Risk":
        suggestions.append("Need immediate coaching and remedial classes.")
    elif risk_level == "Moderate Risk":
        suggestions.append("Needs improvement; focus on core concepts.")
    else:
        suggestions.append("Good progress! Keep up the consistency.")

    # 2. Condition: Low Attendance
    if attendance < 80:
        suggestions.append("Improve attendance above 80%.")

    # 3. Condition: Low Study Hours
    if study_hours < 2:
        suggestions.append("Increase study time to at least 2-3 hours daily.")

    # 4. Condition: Low Internal Marks
    if internal_marks < 60:
        suggestions.append("Retake practice tests and review internal exam mistakes.")

    return " | ".join(suggestions)