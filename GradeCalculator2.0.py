import tkinter as tk
from tkinter import Entry, Label, Button
import json

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.category_label = Label(self, text="Enter the category (Quiz, Test, Assignment, etc.):")
        self.category_label.pack()
        self.category_entry = Entry(self)
        self.category_entry.pack()

        self.assignments_taken_label = Label(self, text="Enter the number of assignments taken by the student in this category:")
        self.assignments_taken_label.pack()
        self.assignments_taken_entry = Entry(self)
        self.assignments_taken_entry.pack()

        self.assignments_graded_label = Label(self, text="Enter the number of assignments graded in this category:")
        self.assignments_graded_label.pack()
        self.assignments_graded_entry = Entry(self)
        self.assignments_graded_entry.pack()

        self.total_assignments_label = Label(self, text="Enter the total number of assignments in this category:")
        self.total_assignments_label.pack()
        self.total_assignments_entry = Entry(self)
        self.total_assignments_entry.pack()

        self.category_weightage_label = Label(self, text="Enter the weightage of this category in the overall grading schema (out of 100%):")
        self.category_weightage_label.pack()
        self.category_weightage_entry = Entry(self)
        self.category_weightage_entry.pack()

        self.current_grade_label = Label(self, text="Enter your current grade in this category (out of 100%):")
        self.current_grade_label.pack()
        self.current_grade_entry = Entry(self)
        self.current_grade_entry.pack()

        self.calculate_button = Button(self)
        self.calculate_button["text"] = "Calculate"
        self.calculate_button["command"] = self.calculate_remaining_assignment_weight
        self.calculate_button.pack()

    def calculate_remaining_assignment_weight(self):
    # Load the saved categories from the json file
        try:
            with open('categories.json', 'r') as f:
                categories = json.load(f)
        except FileNotFoundError:
            categories = {}

        # Get the user input
        category = self.category_entry.get()
        assignments_taken = self.assignments_taken_entry.get()
        assignments_graded = self.assignments_graded_entry.get()
        total_assignments = self.total_assignments_entry.get()
        category_weightage = self.category_weightage_entry.get()
        current_grade = self.current_grade_entry.get()

    # Rest of your code...

    # Check that all fields have been filled in
        if not all([category, assignments_taken, assignments_graded, total_assignments, category_weightage, current_grade]):
            print("Please fill in all fields.")
            return
    
        # Convert the input to the appropriate types
        assignments_taken = int(assignments_taken)
        assignments_graded = int(assignments_graded)
        total_assignments = int(total_assignments)
        category_weightage = float(category_weightage)
        current_grade = float(current_grade)
    
        # Rest of your code...
            # Save the category details for future use
        categories[category] = {
                'assignments_taken': assignments_taken,
                'assignments_graded': assignments_graded,
                'total_assignments': total_assignments,
                'category_weightage': category_weightage,
                'current_grade': current_grade
            }
    
        with open('categories.json', 'w') as f:
                json.dump(categories, f)
    
        # Calculate the weight of the grade already earned.
        earned_weightage = (current_grade / 100) * category_weightage
    
        # Calculate the remaining weightage that can be earned from the ungraded assignments.
        remaining_weightage = category_weightage - earned_weightage
    
        # Calculate the weight of an individual ungraded assignment within the input category.
        individual_ungraded_assignment_weight = (remaining_weightage / (total_assignments - assignments_graded))
    
        # Display the calculated individual ungraded assignment weight.
        print(f"The weight of an individual ungraded assignment within the {category} category is: {individual_ungraded_assignment_weight}%")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
