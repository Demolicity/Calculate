import tkinter as tk
from tkinter import Entry, Label, Button, Text
import json

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        self.load_saved_data()
    
    def load_saved_data(self):
        try:
            with open('categories.json', 'r') as f:
                categories = json.load(f)
        except FileNotFoundError:
            categories = {}

        for category, details in categories.items():
            entry_set = self.add_entry_set()

            entry_set['category_entry'].insert(0, category)
            entry_set['assignments_taken_entry'].insert(0, details['assignments_taken'])
            entry_set['assignments_graded_entry'].insert(0, details['assignments_graded'])
            entry_set['total_assignments_entry'].insert(0, details['total_assignments'])
            entry_set['category_weightage_entry'].insert(0, details['category_weightage'])
            entry_set['current_grade_entry'].insert(0, details['current_grade'])
    
    def create_widgets(self):
        self.entries = []
        self.add_entry_set()
        self.new_column_label = Label(self, text="Add New Column")
        self.new_column_label.grid(column=0, row=1)  # Changed from pack() to grid()
        
        self.add_button = Button(self, text="+", command=self.add_entry_set)
        self.add_button.grid(column=0, row=0)  # Changed from pack() to grid()

        self.calculate_button = Button(self)
        self.calculate_button["text"] = "Calculate"
        self.calculate_button["command"] = self.calculate_remaining_assignment_weight
        self.calculate_button.grid(column=1, row=999)  # Changed from pack() to grid()

        self.result_box = Text(self, height=2, width=50)
        self.result_box.grid()
        self.result_box.grid(column=0, row=1000, columnspan=1000)
  # Changed from pack() to grid()

    def add_entry_set(self):
        entry_set = {}

        entry_set['category_label'] = Label(self, text="Grade-Catagory")
        entry_set['category_label'].grid(column=len(self.entries)*2, row=2)  # Changed from pack() to grid()
        entry_set['category_entry'] = Entry(self)
        entry_set['category_entry'].grid(column=len(self.entries)*2, row=3)  # Changed from pack() to grid()

        entry_set['assignments_taken_label'] = Label(self, text="Assignments Taken")
        entry_set['assignments_taken_label'].grid(column=len(self.entries)*2, row=4)  # Changed from pack() to grid()
        entry_set['assignments_taken_entry'] = Entry(self)
        entry_set['assignments_taken_entry'].grid(column=len(self.entries)*2, row=5)  # Changed from pack() to grid()

        entry_set['assignments_graded_label'] = Label(self, text="Assignments graded")
        entry_set['assignments_graded_label'].grid(column=len(self.entries)*2, row=6)  # Changed from pack() to grid()
        entry_set['assignments_graded_entry'] = Entry(self)
        entry_set['assignments_graded_entry'].grid(column=len(self.entries)*2, row=7)  # Changed from pack() to grid()

        entry_set['total_assignments_label'] = Label(self, text="Total assignments")
        entry_set['total_assignments_label'].grid(column=len(self.entries)*2, row=8)  # Changed from pack() to grid()
        entry_set['total_assignments_entry'] = Entry(self)
        entry_set['total_assignments_entry'].grid(column=len(self.entries)*2, row=9)  # Changed from pack() to grid()

        entry_set['category_weightage_label'] = Label(self, text="Weight%")
        entry_set['category_weightage_label'].grid(column=len(self.entries)*2, row=10)  # Changed from pack() to grid()
        entry_set['category_weightage_entry'] = Entry(self)
        entry_set['category_weightage_entry'].grid(column=len(self.entries)*2, row=11)  # Changed from pack() to grid()

        entry_set['current_grade_label'] = Label(self, text="Current grade In %")
        entry_set['current_grade_label'].grid(column=len(self.entries)*2, row=12)  # Changed from pack() to grid()
        entry_set['current_grade_entry'] = Entry(self)
        entry_set['current_grade_entry'].grid(column=len(self.entries)*2, row=13)  # Changed from pack() to grid()

        self.entries.append(entry_set)
        return entry_set  # Add this line
    
    
    def calculate_remaining_assignment_weight(self):
        for entry_set in self.entries:
            # Load the saved categories from the json file
            try:
                with open('categories.json', 'r') as f:
                    categories = json.load(f)
            except FileNotFoundError:
                categories = {}

            # Get the user input
            category = entry_set['category_entry'].get()
            assignments_taken = entry_set['assignments_taken_entry'].get()
            assignments_graded = entry_set['assignments_graded_entry'].get()
            total_assignments = entry_set['total_assignments_entry'].get()
            category_weightage = entry_set['category_weightage_entry'].get()
            current_grade = entry_set['current_grade_entry'].get()

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
            result_text = f"The weight of an individual ungraded assignment within the {category} category is: {individual_ungraded_assignment_weight}%"
            self.result_box.delete(1.0, tk.END)
            self.result_box.insert(tk.END, result_text)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
