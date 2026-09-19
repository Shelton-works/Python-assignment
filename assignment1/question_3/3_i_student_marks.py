students = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "Diana": 95,
    "Ethan": 88
}

for name, mark in students.items():
    print(name, mark)

highest_mark = 0
top_student = ""

for name, mark in students.items():
    if mark > highest_mark:
        highest_mark = mark
        top_student = name

print("Top student:", top_student)
print("Highest mark:", highest_mark)
