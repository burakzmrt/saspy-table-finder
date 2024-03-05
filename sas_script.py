import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class DataFrameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DataFrame Application")
        # Create label and entry for table name
        self.iconbitmap(r"C:\Users\burak\OneDrive\Masaüstü\Python\unnamed.ico")
        tk.Label(self, text="Enter the name of the table:").pack()
        self.table_entry = tk.Entry(self)
        self.table_entry.pack()
        # Create button to filter DataFrame
        tk.Button(self, text="Filter DataFrame", command=self.filter_dataframe).pack()
        # Create button to exit application
        tk.Button(self, text="Exit", command=self.stop_app).pack()
        # Create Treeview widget to display filtered DataFrame as table
        self.tree = ttk.Treeview(self, selectmode="extended")
        self.tree["columns"] = ("Member Name", "Library Name")
        self.tree.heading("Member Name", text="Member Name", anchor=tk.CENTER)
        self.tree.heading("Library Name", text="Library Name", anchor=tk.CENTER)
        self.tree.column("#0", stretch=tk.NO, minwidth=0, width=0)  # Hide the first column
        self.tree.pack(expand=True, fill="both")
        # Bind Ctrl+C to copy selected cells
        self.tree.bind("<Control-c>", self.copy_cells)

    def filter_dataframe(self):
        # Get the table name from the entry widget
        table_name = self.table_entry.get().strip()
        # Example DataFrame (replace this with your actual DataFrame)
        data = pd.read_excel('saspy_libraries.xlsx')
        df = pd.DataFrame(data)
        # Filter DataFrame based on the table name
        if table_name:
            filtered_df = df[df['Member Name'].str.contains(table_name.upper())][['Member Name', 'Library Name']]
            # Clear previous data in Treeview
            for record in self.tree.get_children():
                self.tree.delete(record)
           # Insert filtered data into Treeview
            for i, row in filtered_df.iterrows():
                self.tree.insert("", tk.END, values=(row["Member Name"], row["Library Name"]))
        else:
            messagebox.showinfo("Error", "Please enter a table name.")

    def stop_app(self):
        self.quit()
        
    def copy_cells(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            # Sadece ilk seçilen satırı al
            item = selected_items[0]
            values = self.tree.item(item, "values")
            
            # 'Library Name' değerini al
            library_name = values[1] if values[1] else ""  # Check if value is not None

            # Panoya sadece 'Library Name' değerini kopyala
            clipboard_text = library_name

            self.clipboard_clear()
            self.clipboard_append(clipboard_text)

if __name__ == '__main__':
    app = DataFrameApp()
    app.mainloop()
