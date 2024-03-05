import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
import pandas as pd
from PyQt5 import QtGui

class DataFrameApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DataFrame Application")

        # Create label and entry for table name
        self.label = QLabel("Enter the name of the table:")
        self.table_entry = QLineEdit()
        self.filter_button = QPushButton("Filter DataFrame")
        self.exit_button = QPushButton("Exit")

        # Create TableWidget to display filtered DataFrame as table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Member Name", "Library Name"])

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table_entry)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        
        self.setWindowIcon(QtGui.QIcon('sas.ico'))
        # set the title
        self.setWindowTitle("Table & Library Finder")

        # Connect buttons to functions
        self.filter_button.clicked.connect(self.filter_dataframe)
        self.exit_button.clicked.connect(self.stop_app)

    def filter_dataframe(self):
        # Get the table name from the entry widget
        table_name = self.table_entry.text().strip()

        # Example DataFrame (replace this with your actual DataFrame)
        data = pd.read_excel('saspy_libraries.xlsx')
        df = pd.DataFrame(data)

        # Filter DataFrame based on the table name
        if table_name:
            filtered_df = df[df['Member Name'].str.contains(table_name.upper())][['Member Name', 'Library Name']]
            
            # Clear previous data in TableWidget
            self.table_widget.setRowCount(0)
            
            # Insert filtered data into TableWidget
            for i, (index, row) in enumerate(filtered_df.iterrows()):
                self.table_widget.insertRow(i)
                self.table_widget.setItem(i, 0, QTableWidgetItem(str(row["Member Name"])))
                self.table_widget.setItem(i, 1, QTableWidgetItem(str(row["Library Name"])))
        else:
            QMessageBox.information(self, "Error", "Please enter a table name.")

    def stop_app(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataFrameApp()
    window.show()
    sys.exit(app.exec_())
