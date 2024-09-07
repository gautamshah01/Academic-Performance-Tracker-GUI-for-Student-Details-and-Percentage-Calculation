import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_input_window():
    input_window = tk.Toplevel(root)
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

    submit_button = tk.Button(input_window, text="Submit", font=("Arial", 12), command=lambda: save_details(entry_name.get(), entry_roll.get(), entry_contact.get(), input_window), bg='blue', fg='white')
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

def save_details(name, roll, contact, window):
    global student_name, student_roll, student_contact
    student_name = name
    student_roll = roll
    student_contact = contact
    window.destroy()
    root.deiconify()

def calculate_percentage():
    try:
        # Retrieve marks for each subject
        marks_python = float(entry_python.get())
        marks_dsa = float(entry_dsa.get())
        marks_dm = float(entry_dm.get())
        marks_statistics = float(entry_statistics.get())
        marks_linux = float(entry_linux.get())
        
        # Check if marks are negative
        if marks_python < 0 or marks_dsa < 0 or marks_dm < 0 or marks_statistics < 0 or marks_linux < 0:
            raise ValueError("Marks cannot be negative.")
        
        # Calculate total marks and percentage
        total_marks = marks_python + marks_dsa + marks_dm + marks_statistics + marks_linux
        percentage = (total_marks / 500) * 100
        
        # Display the percentage
        messagebox.showinfo("Percentage", f"Percentage: {percentage:.2f}%")
        
        # Save data to SQLite database
        conn = sqlite3.connect("student_data.db")
        c = conn.cursor()
        c.execute("INSERT INTO student_marks (name, roll_number, contact_details, marks_python, marks_dsa, marks_dm, marks_statistics, marks_linux, percentage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (student_name, student_roll, student_contact, marks_python, marks_dsa, marks_dm, marks_statistics, marks_linux, percentage))
        conn.commit()
        conn.close()
        
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to get name, roll number, and contact details
def get_details():
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM student_marks ORDER BY rowid DESC LIMIT 1")
    last_entry = c.fetchone()
    conn.close()
    
    messagebox.showinfo("Details", f"Name: {last_entry[1]}\nRoll Number: {last_entry[2]}\nContact: {last_entry[3]}\nPercentage: {last_entry[9]:.2f}%")

# Function to delete last entry
def delete_last_entry():
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM student_marks WHERE id=(SELECT max(id) FROM student_marks)")
    conn.commit()
    conn.close()
    messagebox.showinfo("Delete", "Last entry deleted successfully.")

# Function to convert percentage to CGPA
def convert_to_cgpa():
    try:
        percentage = float(entry_cgpa.get())
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage should be between 0 and 100.")
        
        cgpa = (percentage / 9.)
        messagebox.showinfo("CGPA", f"CGPA: {cgpa:.2f}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Student Details")

# Styling the main window
root.configure(bg="lightgrey")

# Hide the main window initially
root.withdraw()

# Open input window to get student details
open_input_window()

# Labels and entry fields for subject marks
tk.Label(root, text="Marks (Python):", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, pady=5)
entry_python = tk.Entry(root, font=("Arial", 12))
entry_python.grid(row=0, column=1, pady=5)

tk.Label(root, text="Marks (DSA):", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, pady=5)
entry_dsa = tk.Entry(root, font=("Arial", 12))
entry_dsa.grid(row=1, column=1, pady=5)

tk.Label(root, text="Marks (DM):", font=("Arial", 12), bg="lightgrey").grid(row=2, column=0, pady=5)
entry_dm = tk.Entry(root, font=("Arial", 12))
entry_dm.grid(row=2, column=1, pady=5)

tk.Label(root, text="Marks (Statistics):", font=("Arial", 12), bg="lightgrey").grid(row=3, column=0, pady=5)
entry_statistics = tk.Entry(root, font=("Arial", 12))
entry_statistics.grid(row=3, column=1, pady=5)

tk.Label(root, text="Marks (Linux):", font=("Arial", 12), bg="lightgrey").grid(row=4, column=0, pady=5)
entry_linux = tk.Entry(root, font=("Arial", 12))
entry_linux.grid(row=4, column=1, pady=5)

# Button to calculate percentage
tk.Button(root, text="Calculate Percentage", font=("Arial", 12), command=calculate_percentage, bg='blue', fg='white').grid(row=5, column=0, columnspan=2, pady=10)

# Button to get details
tk.Button(root, text="Get Details", font=("Arial", 12), command=get_details, bg='green', fg='white').grid(row=6, column=0, columnspan=2, pady=10)

# Button to delete last entry
tk.Button(root, text="Delete Last Entry", font=("Arial", 12), command=delete_last_entry, bg='red', fg='white').grid(row=7, column=0, columnspan=2, pady=10)

# CGPA converter
tk.Label(root, text="Enter Percentage:", font=("Arial", 12), bg="lightgrey").grid(row=8, column=0, pady=5)
entry_cgpa = tk.Entry(root, font=("Arial", 12))
entry_cgpa.grid(row=8, column=1, pady=5)
tk.Button(root, text="Convert to CGPA", font=("Arial", 12), command=convert_to_cgpa, bg='orange', fg='white').grid(row=9, column=0, columnspan=2, pady=10)

# Create SQLite database and table
conn = sqlite3.connect("student_data.db")
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

# Configure the main window size and position
root.geometry('680x450+0+0')
root.mainloop()
