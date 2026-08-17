def get_student_data():
    name = input("Enter student name: ")
    marks = []

    for i in range(5):
        mark = float(input(f"Enter marks for subject {i + 1}: "))
        marks.append(mark)

    return name, marks


def calculate_average(marks):
    return sum(marks) / len(marks)


def calculate_performance(average):
    if average >= 90:
        return "Excellent"
    elif average >= 75:
        return "Good"
    elif average >= 60:
        return "Average"
    elif average >= 50:
        return "At Risk"
    else:
        return "Fail"


def display_result(name, average, performance):
    print("\n--- Student Result ---")
    print("Name:", name)
    print("Average:", round(average, 2))
    print("Performance:", performance)

name, marks = get_student_data()
average = calculate_average(marks)
performance = calculate_performance(average)
display_result(name, average, performance)
