import sqlite3

class Journal:
    def __init__(self):
        self.conn = sqlite3.connect('your_database.db')  # Update with your database
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                mood TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_new_entry(self, title, content, mood):
        self.cursor.execute('''
            INSERT INTO entries (title, content, mood)
            VALUES (?, ?, ?)
        ''', (title, content, mood))
        self.conn.commit()

    def get_all_entries(self):
        self.cursor.execute('SELECT * FROM entries')
        return self.cursor.fetchall()

    def edit_entry(self, entry_id, title, content, mood):
        self.cursor.execute('''
            UPDATE entries
            SET title = ?, content = ?, mood = ?
            WHERE id = ?
        ''', (title, content, mood, entry_id))
        self.conn.commit()

    def get_entry_by_id(self, entry_id):
        self.cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()
