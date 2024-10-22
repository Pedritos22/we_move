import sqlite3

class TaskList:
    def __init__(self):
        self.conn = sqlite3.connect('your_database.db')  # Update with your database
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_task(self, task_description):
        self.cursor.execute('''
            INSERT INTO tasks (description)
            VALUES (?)
        ''', (task_description,))
        self.conn.commit()

    def show_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        return self.cursor.fetchall()

    def mark_complete(self, task_id):
        self.cursor.execute('''
            UPDATE tasks
            SET completed = 1
            WHERE id = ?
        ''', (task_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
