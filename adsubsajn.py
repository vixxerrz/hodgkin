import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import os

class AbsenceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Absence Tracker")
        self.root.geometry("650x550")  # Increased height to accommodate new button
        self.root.configure(bg='#ecf0f1')
        
        # Load teacher data
        self.teachers = self.load_teacher_data()
        
        # Create GUI
        self.create_widgets()
        
    def load_teacher_data(self):
        """Load teacher data from the JavaScript file"""
        try:
            with open('leaderboard-data.js', 'r') as f:
                content = f.read()
            start_index = content.find('[')
            end_index = content.rfind(']') + 1
            if start_index != -1 and end_index != -1:
                js_array = content[start_index:end_index]
                teachers = json.loads(js_array)
                return teachers
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default teachers including the new ones
            return [
                {"name": "Hafeeza", "absences": 0},
                {"name": "Krishna", "absences": 0},
                {"name": "Seema", "absences": 0},
                {"name": "Amjadh", "absences": 0},
                {"name": "Vinoth", "absences": 0},
                {"name": "Abraham", "absences": 0},
                {"name": "Anthony", "absences": 0},
                {"name": "Sumathi", "absences": 0},
                {"name": "Azima", "absences": 0},
                {"name": "Hamzath", "absences": 0},
                {"name": "Sareena", "absences": 0},
                {"name": "Haritha", "absences": 0},
                {"name": "Raeshma", "absences": 0},
                {"name": "Sanika", "absences": 0},
                {"name": "Sudhesh", "absences": 0},
                {"name": "Adhu", "absences": 0}
            ]
    
    def save_teacher_data(self):
        """Save teacher data back to the JavaScript file"""
        js_content = f"const teachers = {json.dumps(self.teachers, indent=2)};"
        with open('leaderboard-data.js', 'w') as f:
            f.write(js_content)
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Teacher Absence Tracker", 
            font=("Arial", 20, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Teacher list frame
        list_frame = tk.Frame(self.root, bg='#ecf0f1')
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        # Treeview for teachers
        columns = ("name", "absences")
        self.tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            height=12,
            selectmode="browse"
        )
        
        self.tree.heading("name", text="Teacher Name")
        self.tree.heading("absences", text="Absences")
        
        self.tree.column("name", width=400, anchor=tk.W)
        self.tree.column("absences", width=150, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Populate table
        self.populate_treeview()
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#ecf0f1')
        button_frame.pack(pady=10)
        
        add_absence_btn = tk.Button(
            button_frame,
            text="+",
            command=self.increment_absence,
            bg='#27ae60',
            fg='white',
            font=("Arial", 14, "bold"),
            width=5,
            height=1,
            relief=tk.FLAT,
            cursor="hand2"
        )
        add_absence_btn.pack(side=tk.LEFT, padx=5)
        
        subtract_absence_btn = tk.Button(
            button_frame,
            text="-",
            command=self.decrement_absence,
            bg='#e67e22',
            fg='white',
            font=("Arial", 14, "bold"),
            width=5,
            height=1,
            relief=tk.FLAT,
            cursor="hand2"
        )
        subtract_absence_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(
            button_frame,
            text="Reset All",
            command=self.reset_absences,
            bg='#c0392b',
            fg='white',
            font=("Arial", 10, "bold"),
            width=10,
            height=1,
            relief=tk.FLAT,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # New button to add teachers
        add_teacher_btn = tk.Button(
            button_frame,
            text="Add Teacher",
            command=self.add_teacher,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            width=12,
            height=1,
            relief=tk.FLAT,
            cursor="hand2"
        )
        add_teacher_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "italic"),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.status_label.pack(pady=10)
    
    def populate_treeview(self):
        """Populate the treeview with teacher data"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        sorted_teachers = sorted(self.teachers, key=lambda x: x['absences'], reverse=True)
        for teacher in sorted_teachers:
            self.tree.insert("", tk.END, values=(teacher['name'], teacher['absences']))
    
    def increment_absence(self):
        """Increase absence count"""
        selected = self.tree.focus()
        if not selected:
            self.status_label.config(text="⚠ Please select a teacher first.")
            return
        teacher_name = self.tree.item(selected)['values'][0]
        for teacher in self.teachers:
            if teacher['name'] == teacher_name:
                teacher['absences'] += 1
                break
        self.save_teacher_data()
        self.populate_treeview()
        self.status_label.config(text=f"✅ Marked {teacher_name} as absent for today.")
    
    def decrement_absence(self):
        """Decrease absence count"""
        selected = self.tree.focus()
        if not selected:
            self.status_label.config(text="⚠ Please select a teacher first.")
            return
        teacher_name = self.tree.item(selected)['values'][0]
        for teacher in self.teachers:
            if teacher['name'] == teacher_name and teacher['absences'] > 0:
                teacher['absences'] -= 1
                break
        self.save_teacher_data()
        self.populate_treeview()
        self.status_label.config(text=f"➖ Removed one absence from {teacher_name}.")
    
    def reset_absences(self):
        """Reset all absence counts to zero (no popup confirm)"""
        for teacher in self.teachers:
            teacher['absences'] = 0
        self.save_teacher_data()
        self.populate_treeview()
        self.status_label.config(text="🔄 All absences have been reset to zero.")
    
    def add_teacher(self):
        """Add a new teacher to the list"""
        teacher_name = simpledialog.askstring("Add Teacher", "Enter teacher's name:")
        if teacher_name:
            # Check if teacher already exists
            for teacher in self.teachers:
                if teacher['name'].lower() == teacher_name.lower():
                    messagebox.showerror("Error", f"Teacher '{teacher_name}' already exists!")
                    return
            
            # Add new teacher with 0 absences
            self.teachers.append({"name": teacher_name, "absences": 0})
            self.save_teacher_data()
            self.populate_treeview()
            self.status_label.config(text=f"✅ Added {teacher_name} to the list.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AbsenceTracker(root)
    root.mainloop()
