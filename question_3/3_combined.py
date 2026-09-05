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

print()

class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def display_details(self):
        print("Title:", self.title)
        print("Author:", self.author)
        print("Price:", self.price)


book1 = Book("To Kill a Mockingbird", "Harper Lee", 14.99)
book2 = Book("1984", "George Orwell", 12.50)

book1.display_details()
book2.display_details()
