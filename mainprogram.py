import tkinter as tk
from tkinter import messagebox
import sqlite3

class Student:
    def __init__(self, name, roll, contact):
        self.name = name
        self.roll = roll
        self.contact = contact

class StudentMarks(Student):
    def __init__(self, name, roll, contact, marks_python, marks_dsa, marks_dm, marks_statistics, marks_linux):
        super().__init__(name, roll, contact)
        self.marks_python = marks_python
        self.marks_dsa = marks_dsa
        self.marks_dm = marks_dm
        self.marks_statistics = marks_statistics
        self.marks_linux = marks_linux
        self.percentage = 0

    def calculate_percentage(self):
        total_marks = self.marks_python + self.marks_dsa + self.marks_dm + self.marks_statistics + self.marks_linux
        self.percentage = (total_marks / 500) * 100

    def convert_to_cgpa(self):
        return self.percentage / 9.0

class DatabaseManager:
    def __init__(self, db_name="student_data.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS student_marks
                     (id INTEGER PRIMARY KEY,
                      name TEXT,
                      roll_number TEXT,
                      contact_details TEXT,
                      marks_python REAL,
                      marks_dsa REAL,
                      marks_dm REAL,
                      marks_statistics REAL,
                      marks_linux REAL,
                      percentage REAL)''')
        conn.commit()
        conn.close()

    def insert_student(self, student_marks):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO student_marks (name, roll_number, contact_details, marks_python, marks_dsa, marks_dm, marks_statistics, marks_linux, percentage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (student_marks.name, student_marks.roll, student_marks.contact, student_marks.marks_python, student_marks.marks_dsa, student_marks.marks_dm, student_marks.marks_statistics, student_marks.marks_linux, student_marks.percentage))
        conn.commit()
        conn.close()

    def get_latest_record(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM student_marks ORDER BY rowid DESC LIMIT 1")
        last_entry = c.fetchone()
        conn.close()
        return last_entry

    def delete_last_entry(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM student_marks WHERE id=(SELECT max(id) FROM student_marks)")
        conn.commit()
        conn.close()

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Details")
        self.root.configure(bg="lightgrey")
        self.root.geometry('680x450+0+0')
        self.database = DatabaseManager()

        # Hide the main window initially
        self.root.withdraw()

        # Open input window to get student details
        self.open_input_window()

    def open_input_window(self):
        input_window = tk.Toplevel(self.root)
        input_window.title("Enter Details")
        input_window.geometry('300x200')

        tk.Label(input_window, text="Name:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
        entry_name = tk.Entry(input_window, font=("Arial", 12))
        entry_name.grid(row=0, column=1, pady=5)

        tk.Label(input_window, text="Roll Number:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        entry_roll = tk.Entry(input_window, font=("Arial", 12))
        entry_roll.grid(row=1, column=1, pady=5)

        tk.Label(input_window, text="Contact Details:", font=("Arial", 12)).grid(row=2, column=0, pady=5)
        entry_contact = tk.Entry(input_window, font=("Arial", 12))
        entry_contact.grid(row=2, column=1, pady=5)

        submit_button = tk.Button(input_window, text="Submit", font=("Arial", 12), command=lambda: self.save_details(entry_name.get(), entry_roll.get(), entry_contact.get(), input_window), bg='blue', fg='white')
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_details(self, name, roll, contact, window):
        self.student = Student(name, roll, contact)
        window.destroy()
        self.root.deiconify()
        self.create_main_interface()

    def create_main_interface(self):
        # Labels and entry fields for subject marks
        tk.Label(self.root, text="Marks (Python):", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, pady=5)
        self.entry_python = tk.Entry(self.root, font=("Arial", 12))
        self.entry_python.grid(row=0, column=1, pady=5)

        tk.Label(self.root, text="Marks (DSA):", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, pady=5)
        self.entry_dsa = tk.Entry(self.root, font=("Arial", 12))
        self.entry_dsa.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text="Marks (DM):", font=("Arial", 12), bg="lightgrey").grid(row=2, column=0, pady=5)
        self.entry_dm = tk.Entry(self.root, font=("Arial", 12))
        self.entry_dm.grid(row=2, column=1, pady=5)

        tk.Label(self.root, text="Marks (Statistics):", font=("Arial", 12), bg="lightgrey").grid(row=3, column=0, pady=5)
        self.entry_statistics = tk.Entry(self.root, font=("Arial", 12))
        self.entry_statistics.grid(row=3, column=1, pady=5)

        tk.Label(self.root, text="Marks (Linux):", font=("Arial", 12), bg="lightgrey").grid(row=4, column=0, pady=5)
        self.entry_linux = tk.Entry(self.root, font=("Arial", 12))
        self.entry_linux.grid(row=4, column=1, pady=5)

        # Button to calculate percentage
        tk.Button(self.root, text="Calculate Percentage", font=("Arial", 12), command=self.calculate_percentage, bg='blue', fg='white').grid(row=5, column=0, columnspan=2, pady=10)

        # Button to get details
        tk.Button(self.root, text="Get Details", font=("Arial", 12), command=self.get_details, bg='green', fg='white').grid(row=6, column=0, columnspan=2, pady=10)

        # Button to delete last entry
        tk.Button(self.root, text="Delete Last Entry", font=("Arial", 12), command=self.delete_last_entry, bg='red', fg='white').grid(row=7, column=0, columnspan=2, pady=10)

        # CGPA converter
        tk.Label(self.root, text="Enter Percentage:", font=("Arial", 12), bg="lightgrey").grid(row=8, column=0, pady=5)
        self.entry_cgpa = tk.Entry(self.root, font=("Arial", 12))
        self.entry_cgpa.grid(row=8, column=1, pady=5)
        tk.Button(self.root, text="Convert to CGPA", font=("Arial", 12), command=self.convert_to_cgpa, bg='orange', fg='white').grid(row=9, column=0, columnspan=2, pady=10)

    def calculate_percentage(self):
        try:
            # Retrieve marks for each subject
            marks_python = float(self.entry_python.get())
            marks_dsa = float(self.entry_dsa.get())
            marks_dm = float(self.entry_dm.get())
            marks_statistics = float(self.entry_statistics.get())
            marks_linux = float(self.entry_linux.get())
            
            # Check if marks are negative
            if marks_python < 0 or marks_dsa < 0 or marks_dm < 0 or marks_statistics < 0 or marks_linux < 0:
                raise ValueError("Marks cannot be negative.")
            
            # Calculate total marks and percentage
            student_marks = StudentMarks(self.student.name, self.student.roll, self.student.contact, marks_python, marks_dsa, marks_dm, marks_statistics, marks_linux)
            student_marks.calculate_percentage()
            
            # Display the percentage
            messagebox.showinfo("Percentage", f"Percentage: {student_marks.percentage:.2f}%")
            
            # Save data to SQLite database
            self.database.insert_student(student_marks)
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_details(self):
        last_entry = self.database.get_latest_record()
        if last_entry:
            messagebox.showinfo("Details", f"Name: {last_entry[1]}\nRoll Number: {last_entry[2]}\nContact: {last_entry[3]}\nPercentage: {last_entry[9]:.2f}%")

    def delete_last_entry(self):
        self.database.delete_last_entry()
        messagebox.showinfo("Delete", "Last entry deleted successfully.")

    def convert_to_cgpa(self):
        try:
            percentage = float(self.entry_cgpa.get())
            if percentage < 0 or percentage > 100:
                raise ValueError("Percentage should be between 0 and 100.")
            
            cgpa = percentage / 9.0
            messagebox.showinfo("CGPA", f"CGPA: {cgpa:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
app = Application(root)
root.mainloop()
