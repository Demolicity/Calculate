# Sure, I can help you translate this Tkinter code to PyQt5. However, please note that PyQt5 doesn't have a direct equivalent for Tkinter's grid layout manager. The closest is QGridLayout. Here's a rough translation of your code:




from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QGridLayout, QHBoxLayout 
import json

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.layout = QVBoxLayout()  # Initialize self.layout
        self.entry_layout = QHBoxLayout()
        self.layout.addLayout(self.entry_layout)
        self.create_widgets()
        self.load_saved_data()
        self.setLayout(self.layout)
        self.categories = {}
    def load_saved_data(self):
        try:
            with open('categories.json', 'r') as f:
                categories = json.load(f)
        except FileNotFoundError:
            categories = {}

        for category, details in categories.items():
            entry_set = self.add_entry_set()

            entry_set['category_entry'].setText(category)
            entry_set['assignments_taken_entry'].setText(str(details['assignments_taken']))
            entry_set['assignments_graded_entry'].setText(str(details['assignments_graded']))
            entry_set['total_assignments_entry'].setText(str(details['total_assignments']))
            entry_set['category_weightage_entry'].setText(str(details['category_weightage']))
            entry_set['current_grade_entry'].setText(str(details['current_grade']))

    def create_widgets(self):
        self.add_entry_set()
        self.new_column_label = QLabel("Add New Column")
        self.layout.addWidget(self.new_column_label)

        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_entry_set)
        self.layout.addWidget(self.add_button)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_remaining_assignment_weight)
        self.layout.addWidget(self.calculate_button)

        self.result_box = QTextEdit()
        self.layout.addWidget(self.result_box)

    def add_entry_set(self):
        entry_set = {}
        grid = QGridLayout()

        entry_set['category_label'] = QLabel("Grade-Category")
        grid.addWidget(entry_set['category_label'], 0, 0)
        entry_set['category_entry'] = QLineEdit()
        grid.addWidget(entry_set['category_entry'], 0, 1)

        entry_set['assignments_taken_label'] = QLabel("Assignments Taken")
        grid.addWidget(entry_set['assignments_taken_label'], 1, 0)
        entry_set['assignments_taken_entry'] = QLineEdit()
        grid.addWidget(entry_set['assignments_taken_entry'], 1, 1)

        entry_set['assignments_graded_label'] = QLabel("Assignments graded")
        grid.addWidget(entry_set['assignments_graded_label'], 2, 0)
        entry_set['assignments_graded_entry'] = QLineEdit()
        grid.addWidget(entry_set['assignments_graded_entry'], 2, 1)

        entry_set['total_assignments_label'] = QLabel("Total assignments")
        grid.addWidget(entry_set['total_assignments_label'], 3, 0)
        entry_set['total_assignments_entry'] = QLineEdit()
        grid.addWidget(entry_set['total_assignments_entry'], 3, 1)

        entry_set['category_weightage_label'] = QLabel("Weight%")
        grid.addWidget(entry_set['category_weightage_label'], 4, 0)
        entry_set['category_weightage_entry'] = QLineEdit()
        grid.addWidget(entry_set['category_weightage_entry'], 4, 1)

        entry_set['current_grade_label'] = QLabel("Current grade In %")
        grid.addWidget(entry_set['current_grade_label'], 5, 0)
        entry_set['current_grade_entry'] = QLineEdit()
        grid.addWidget(entry_set['current_grade_entry'], 5, 1)

        self.entries.append(entry_set)
        self.entry_layout.addLayout(grid)
        return entry_set

    def calculate_remaining_assignment_weight(self):
        for entry_set in self.entries:
            # Load the saved categories from the json file
            # Get the user input
            category = entry_set['category_entry'].text()
            assignments_taken = entry_set['assignments_taken_entry'].text()
            assignments_graded = entry_set['assignments_graded_entry'].text()
            total_assignments = entry_set['total_assignments_entry'].text()
            category_weightage = entry_set['category_weightage_entry'].text()
            current_grade = entry_set['current_grade_entry'].text()

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
            self.categories[category] = {
                'assignments_taken': assignments_taken,
                'assignments_graded': assignments_graded,
                'total_assignments': total_assignments,
                'category_weightage': category_weightage,
                'current_grade': current_grade
            }

            with open('categories.json', 'w') as f:
                    json.dump(self.categories, f)

            # Calculate the weight of the grade already earned.
            earned_weightage = (current_grade / 100) * category_weightage

            # Calculate the remaining weightage that can be earned from the ungraded assignments.
            remaining_weightage = category_weightage - earned_weightage

            # Calculate the weight of an individual ungraded assignment within the input category.
            individual_ungraded_assignment_weight = (remaining_weightage / (total_assignments - assignments_graded))

            # Display the calculated individual ungraded assignment weight.
            result_text = f"The weight of an individual ungraded assignment within the {category} category is: {individual_ungraded_assignment_weight}%"
            self.result_box.clear()
            self.result_box.append(result_text)

if __name__ == "__main__":
    app = QApplication([])
    application = Application()
    application.show()
    app.exec_()