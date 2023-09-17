from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QGridLayout
import json

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
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

        # Add the rest of your labels and entries here...

        self.entries.append(entry_set)
        self.layout.addLayout(grid)
        return entry_set

    def calculate_remaining_assignment_weight(self):
        # Your calculation logic here...

if __name__ == "__main__":
    app = QApplication([])
    application = Application()
    application.show()
    app.exec_()