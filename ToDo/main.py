import sys

from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QCalendarWidget,
                             QVBoxLayout,
                             QWidget,
                             QListWidget,
                             QPushButton,
                             QLineEdit,
                             QHBoxLayout,
                             )
from PyQt5.QtCore import QDate
import psycopg2 as psql
from decouple import config


class DataBase:
    
    def __init__(self):
        super(DataBase, self).__init__()
    
    def checkConnection(self):
        try:
            c = psql.connect(user=config("user"),host=config("host"),password=config("password"))
            return c
        except Exception as e:
            return e

    def checkTable(self):
        try:
            c = psql.connect(user=config("user"),host=config("host"),password=config("password"),database="todo")
            c.autocommit = True
            q = """CREATE TABLE task (ID SERIAL PRIMARY KEY NOT NULL, title TEXT NOT NULL, day DATE NOT NULL)"""
            curs = c.cursor()
            curs.execute(query=q)
            return c.status
        except Exception as e:
            return e
    
    def readToDo(self, day:str):
        try:
            c = psql.connect(user=config("user"),host=config("host"),password=config("password"),database="todo")
            c.autocommit = True
            curs = c.cursor()
            q = f"""SELECT title FROM task WHERE day=%s"""
            curs.execute(q, (day,))
            x = curs.fetchall()
            return x
        except Exception as e:
            return e
    
    def addToDo(self, day, title):
        try:
            c = psql.connect(user=config("user"), host=config("host"), password=config("password"), database="todo")
            c.autocommit = True
            curs = c.cursor()
            q = "INSERT INTO task (title, day) VALUES (%s, %s)"
            curs.execute(q, (title, day))
            return "Task added successfully"
        except Exception as e:
            return e
    
    def deleteToDo(self, day, title):
        try:
            pass
        except Exception as e:
            raise e


class TodoCalendar(QMainWindow):

    def __init__(self):
        super(TodoCalendar, self).__init__()

        self.db = DataBase()

        print(self.db.checkTable())

        self.setWindowTitle("TODO Calendar")
        self.setGeometry(100, 100, 900, 750)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_todos)
        self.layout.addWidget(self.calendar)

        self.todo_list = QListWidget(self)
        self.layout.addWidget(self.todo_list)

        self.input_layout = QHBoxLayout()
        self.todo_input = QLineEdit(self)
        self.add_button = QPushButton("Add TODO", self)
        self.add_button.clicked.connect(self.add_todo)

        self.input_layout.addWidget(self.todo_input)
        
        self.input_layout.addWidget(self.add_button)
        
        self.layout.addLayout(self.input_layout)

        self.todos = {}

        self.delete_button = QPushButton("Delete Selected TODO", self)
        self.delete_button.clicked.connect(self.delete_todo)
        self.layout.addWidget(self.delete_button)
    
    def show_todos(self, date):
        self.todo_list.clear()
        date_str = date.toString("yyyy-MM-dd")
        x = self.db.readToDo(date_str)
        if x:
            for todo in x:
                self.todo_list.addItem(todo[0])

    def add_todo(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        todo = self.todo_input.text()
        
        if date not in self.todos:
            self.todos[date] = []
        
        print(self.db.addToDo(date, todo))
        self.todos[date].append(todo)
        self.todo_input.clear()
        self.show_todos(self.calendar.selectedDate())
    
    def delete_todo(self, day, title):
        try:
            pass
        except Exception as e:
            raise e


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoCalendar()
    window.show()
    sys.exit(app.exec())
