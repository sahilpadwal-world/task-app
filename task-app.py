from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget,
    QLabel, QMessageBox, QTabWidget, QHBoxLayout
)
import json
import os

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 500, 450)
        
        self.layout = QVBoxLayout()
        
        # Tabs
        self.tabs = QTabWidget()
        self.tab_tasks = QWidget()
        self.tab_completed = QWidget()
        self.tabs.addTab(self.tab_tasks, "Tasks")
        self.tabs.addTab(self.tab_completed, "Completed")
        
        # Task Tab Layout
        self.task_layout = QVBoxLayout()
        
        self.task_label = QLabel("Task:")
        self.task_entry = QLineEdit()
        
        self.time_label = QLabel("Time (HH:MM):")
        self.time_entry = QLineEdit()
        
        self.task_list = QListWidget()
        
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        
        self.delete_button = QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete_task)
        
        self.complete_button = QPushButton("Mark Completed")
        self.complete_button.clicked.connect(self.complete_task)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_tasks)
        
        # Layout Setup
        self.task_layout.addWidget(self.task_label)
        self.task_layout.addWidget(self.task_entry)
        self.task_layout.addWidget(self.time_label)
        self.task_layout.addWidget(self.time_entry)
        self.task_layout.addWidget(self.task_list)
        
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.complete_button)
        self.button_layout.addWidget(self.clear_button)
        
        self.task_layout.addLayout(self.button_layout)
        self.tab_tasks.setLayout(self.task_layout)
        
        # Completed Tasks Tab Layout
        self.completed_layout = QVBoxLayout()
        self.completed_list = QListWidget()
        self.completed_layout.addWidget(self.completed_list)
        self.tab_completed.setLayout(self.completed_layout)
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        self.load_task_list()
    
    def load_task_list(self):
        self.task_list.clear()
        self.completed_list.clear()
        for task in tasks:
            item_text = f"{task['time']} - {task['task']}"
            if task.get("completed", False):
                self.completed_list.addItem("✅ " + item_text)
            else:
                self.task_list.addItem("❌ " + item_text)
    
    def add_task(self):
        task_text = self.task_entry.text().strip()
        task_time = self.time_entry.text().strip()
        if not task_text:
            QMessageBox.warning(self, "Warning", "Task cannot be empty!")
            return
        tasks.append({"task": task_text, "time": task_time, "completed": False})
        save_tasks()
        self.load_task_list()
        self.task_entry.clear()
        self.time_entry.clear()
    
    def delete_task(self):
        selected = self.task_list.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Warning", "No task selected!")
            return
        del tasks[selected]
        save_tasks()
        self.load_task_list()
    
    def complete_task(self):
        selected = self.task_list.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Warning", "No task selected!")
            return
        tasks[selected]["completed"] = True
        save_tasks()
        self.load_task_list()
    
    def clear_tasks(self):
        global tasks
        tasks = []
        save_tasks()
        self.load_task_list()

if __name__ == "__main__":
    app = QApplication([])
    tasks = load_tasks()
    window = TaskManager()
    window.show()
    app.exec()
