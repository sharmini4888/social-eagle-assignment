# 1. Import statistics library
import statistics

# 2. Get student basic details
name = input("Enter Student Name: ")
age = int(input("Enter Student Age: "))
std_class = input("Enter Class (e.g., 5th, 10th): ")

# 3. Store 5 subjects inside a tuple
subjects = ("Maths", "Science", "English", "History", "Computer")

marks = []  # list to store marks

# Taking marks for each subject
print("\nEnter Marks for the Following Subjects:")
for sub in subjects:
    mark = float(input(f"Enter marks for {sub}: "))
    marks.append(mark)

# 4. Store student details inside dictionary
student = {
    "Name": name,
    "Age": age,
    "Class": std_class,
    "Subjects": subjects,
    "Marks": marks
}

# 5. Functions
def total_marks(marks):
    return sum(marks)

def average_marks(marks):
    return statistics.mean(marks)

# Grade as per user rule
def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "E"

# Calculations
total = total_marks(marks)
avg = average_marks(marks)
grade_result = calculate_grade(avg)

# 6. Beautiful Output
print("\n=============== STUDENT REPORT CARD ===============")
print(f"Name       : {student['Name']}")
print(f"Age        : {student['Age']}")
print(f"Class      : {student['Class']}")
print("---------------------------------------------------")
print("Subject-wise Marks:")
for i in range(len(subjects)):
    print(f"{subjects[i]} : {marks[i]}")
print("---------------------------------------------------")
print(f"Total Marks    : {total}")
print(f"Average Marks  : {avg:.2f}")
print(f"Final Grade    : {grade_result}")
print("===================================================")
