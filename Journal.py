import sys
import sqlite3
import time
import pygame
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QMessageBox,
    QInputDialog, QWidget, QDialog, QListWidget, QListWidgetItem, QTextEdit
)
from PyQt5.QtCore import Qt, QSize  # Added QSize import
from PyQt5.QtGui import QFont


class Journal:
    DB_FILE = 'journal.db'

    def __init__(self):
        self.conn = self.create_connection()
        self.create_table()

    def create_connection(self):
        """Create a database connection."""
        try:
            return sqlite3.connect(Journal.DB_FILE)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return None

    def create_table(self):
        """Create the journal_entries table if it doesn't exist."""
        try:
            with self.conn:
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS journal_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        number INTEGER,
                        title TEXT,
                        content TEXT,
                        date TEXT
                    )
                ''')
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_new_entry(self, title, content):
        """Add a new journal entry."""
        entry_date = time.strftime("%d-%m-%Y", time.localtime())
        entry_number = self.get_next_entry_number()

        if entry_number:
            try:
                with self.conn:
                    self.conn.execute('''
                        INSERT INTO journal_entries (number, title, content, date)
                        VALUES (?, ?, ?, ?)
                    ''', (entry_number, title, content, entry_date))
                return f"Entry #{entry_number} added successfully."
            except sqlite3.Error as e:
                return f"Error saving entry to the database: {e}"
        else:
            return "Failed to determine next entry number."

    def get_next_entry_number(self):
        """Get the next available entry number from the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT MAX(number) FROM journal_entries')
            result = cursor.fetchone()
            return (result[0] or 0) + 1
        except sqlite3.Error as e:
            print(f"Error retrieving entry count: {e}")
            return None

    def get_all_entries(self):
        """Get all journal entries."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM journal_entries ORDER BY number')  # Order by number
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            return []

    def edit_entry(self, entry_number, new_title=None, new_content=None):
        """Edit the title or content of an existing entry."""
        try:
            with self.conn:
                self.conn.execute('''
                    UPDATE journal_entries
                    SET title = ?, content = ?
                    WHERE number = ?
                ''', (new_title, new_content, entry_number))
            return f"Entry #{entry_number} updated successfully."
        except sqlite3.Error as e:
            return f"Error updating entry: {e}"

    def delete_entry(self, entry_number):
        """Delete an entry by its number."""
        try:
            with self.conn:
                self.conn.execute('DELETE FROM journal_entries WHERE number = ?', (entry_number,))
            self.renumber_entries()  # Renumber entries after deletion
            return f"Entry #{entry_number} deleted successfully."
        except sqlite3.Error as e:
            return f"Error deleting entry: {e}"

    def renumber_entries(self):
        """Renumber the entries after a deletion."""
        try:
            entries = self.get_all_entries()
            for index, entry in enumerate(entries):
                new_number = index + 1
                with self.conn:
                    self.conn.execute('''
                        UPDATE journal_entries
                        SET number = ?
                        WHERE id = ?
                    ''', (new_number, entry[0]))  # entry[0] is the id
        except sqlite3.Error as e:
            print(f"Error renumbering entries: {e}")


class JournalApp(QMainWindow):
    TITLE_MAX_LENGTH = 50

    def __init__(self):
        super().__init__()

        self.journal = Journal()

        # Initialize pygame for playing music
        pygame.mixer.init()
        pygame.mixer.music.load("/Users/pedritos22/Desktop/relaxing_music.mp3")
        pygame.mixer.music.set_volume(0.5)  
        pygame.mixer.music.play(-1)  # Play the music indefinitely

        # Windows Dimensions
        self.setWindowTitle("Journal Manager")
        self.setGeometry(300, 200, 600, 400)
        self.setStyleSheet("background-color: #2C2C2C; color: #D3D3D3;")

        # Main layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Title Label
        self.title_label = QLabel("Journal Manager", self)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))  
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Add Entry Button
        self.add_entry_btn = QPushButton("Add Entry", self)
        self.add_entry_btn.setFont(QFont("Arial", 16))  
        self.add_entry_btn.setStyleSheet(
            "background-color: #4A90E2; color: white; border: 1px solid #3A80C2; border-radius: 10px;"
        )
        self.add_entry_btn.clicked.connect(self.add_entry)
        self.main_layout.addWidget(self.add_entry_btn)

        # Show Entries Button
        self.show_entries_btn = QPushButton("Show All Entries", self)
        self.show_entries_btn.setFont(QFont("Arial", 16))  
        self.show_entries_btn.setStyleSheet(
            "background-color: #4A90E2; color: white; border: 1px solid #3A80C2; border-radius: 10px;"
        )
        self.show_entries_btn.clicked.connect(self.show_entries)
        self.main_layout.addWidget(self.show_entries_btn)

        # Edit Entry Button
        self.edit_entry_btn = QPushButton("Edit Entry", self)
        self.edit_entry_btn.setFont(QFont("Arial", 16))  # Increased font size
        self.edit_entry_btn.setStyleSheet(
            "background-color: #F39C12; color: white; border: 1px solid #D68C10; border-radius: 10px;"
        )
        self.edit_entry_btn.clicked.connect(self.select_entry_for_edit)
        self.main_layout.addWidget(self.edit_entry_btn)

        # Delete Entry Button
        self.delete_entry_btn = QPushButton("Delete Entry", self)
        self.delete_entry_btn.setFont(QFont("Arial", 16))  # Increased font size
        self.delete_entry_btn.setStyleSheet(
            "background-color: #E74C3C; color: white; border: 1px solid #D43F3A; border-radius: 10px;"
        )
        self.delete_entry_btn.clicked.connect(self.select_entry_for_deletion)
        self.main_layout.addWidget(self.delete_entry_btn)

        # Footer Label
        self.footer_label = QLabel("Yournal™", self)
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setStyleSheet("color: #AAB8C2; font-size: 14px;")
        self.main_layout.addWidget(self.footer_label)

    def add_entry(self):
        """Show a dialog to add a new journal entry."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Entry")
        dialog.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(dialog)

        # Text edit for the title
        title_edit = QTextEdit()  
        title_edit.setFixedHeight(40)
        layout.addWidget(QLabel(f"Enter Title (Max {JournalApp.TITLE_MAX_LENGTH} characters):"))
        layout.addWidget(title_edit)

        # Text edit for the content
        content_edit = QTextEdit()  
        layout.addWidget(QLabel("Enter Content:"))
        layout.addWidget(content_edit)

        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(lambda: self.save_new_entry(title_edit.toPlainText(), content_edit.toPlainText(), dialog))
        layout.addWidget(save_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_new_entry(self, title, content, dialog):
        if len(title) > JournalApp.TITLE_MAX_LENGTH:
            QMessageBox.warning(self, "Title Too Long", f"Title must be less than {JournalApp.TITLE_MAX_LENGTH + 1} characters.")
            return
        if not title.strip() or not content.strip():
            QMessageBox.warning(self, "Input Error", "Title and content cannot be empty.")
            return

        result = self.journal.add_new_entry(title, content)
        QMessageBox.information(self, "Entry Added", result)
        dialog.close()

    def show_entries(self):
        """Show all journal entries in a new window."""
        entries_window = QDialog(self)
        entries_window.setWindowTitle("Journal Entries")
        entries_window.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout(entries_window)

        entries_list = QListWidget(entries_window)
        layout.addWidget(entries_list)

        entries = self.journal.get_all_entries()

        if not entries:
            entries_list.addItem("No entries found.")
        else:
            for entry in entries:
                entry_text = f"Entry #{entry[1]}: {entry[2]} - {entry[3]} on {entry[4]}"
                item = QListWidgetItem(entry_text)
                entries_list.addItem(item)

        close_button = QPushButton("Close", entries_window)
        close_button.clicked.connect(entries_window.close)
        layout.addWidget(close_button)

        entries_window.setLayout(layout)
        entries_window.exec_()  # Show the entries dialog

    def select_entry_for_edit(self):
        """Show a dialog to select an entry for editing."""
        entries = self.journal.get_all_entries()
        if not entries:
            QMessageBox.warning(self, "No Entries", "No entries found to edit.")
            return

        entry_selector = QDialog(self)
        entry_selector.setWindowTitle("Select Entry to Edit")
        entry_selector.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(entry_selector)

        # List widget to display the entries
        entries_list = QListWidget(entry_selector)
        for entry in entries:
            entry_text = f"Entry #{entry[1]}: {entry[2]}"
            item = QListWidgetItem(entry_text)
            entries_list.addItem(item)
        layout.addWidget(entries_list)

        # Edit Selected Entry
        edit_button = QPushButton("Edit Selected Entry")
        edit_button.clicked.connect(lambda: self.edit_entry(entries_list.currentRow(), entry_selector))
        layout.addWidget(edit_button)

        entry_selector.setLayout(layout)
        entry_selector.exec_()

    def edit_entry(self, index, dialog):
        """Edit the selected entry."""
        entries = self.journal.get_all_entries()
        selected_entry = entries[index]
        entry_number = selected_entry[1]

        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle(f"Edit Entry #{entry_number}")
        edit_dialog.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(edit_dialog)

        # Text edit for the title
        title_edit = QTextEdit()
        title_edit.setPlainText(selected_entry[2])  # Set current title
        title_edit.setFixedHeight(40)
        layout.addWidget(QLabel(f"Edit Title (Max {JournalApp.TITLE_MAX_LENGTH} characters):"))
        layout.addWidget(title_edit)

        # Text edit for the content
        content_edit = QTextEdit()
        content_edit.setPlainText(selected_entry[3])  # Set current content
        layout.addWidget(QLabel("Edit Content:"))
        layout.addWidget(content_edit)

        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(lambda: self.save_edit_entry(entry_number, title_edit.toPlainText(), content_edit.toPlainText(), edit_dialog))
        layout.addWidget(save_btn)

        edit_dialog.setLayout(layout)
        edit_dialog.exec_()
        dialog.close()  # Close the entry!!!!!

    def save_edit_entry(self, entry_number, new_title, new_content, dialog):
        if len(new_title) > JournalApp.TITLE_MAX_LENGTH:
            QMessageBox.warning(self, "Title Too Long", f"Title must be less than {JournalApp.TITLE_MAX_LENGTH + 1} characters.")
            return
        if not new_title.strip() or not new_content.strip():
            QMessageBox.warning(self, "Input Error", "Title and content cannot be empty.")
            return

        result = self.journal.edit_entry(entry_number, new_title, new_content)
        QMessageBox.information(self, "Entry Edited", result)
        dialog.close()

    def select_entry_for_deletion(self):
        """Show a dialog to select an entry for deletion."""
        entries = self.journal.get_all_entries()
        if not entries:
            QMessageBox.warning(self, "No Entries", "No entries found to delete.")
            return

        entry_selector = QDialog(self)
        entry_selector.setWindowTitle("Select Entry to Delete")
        entry_selector.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(entry_selector)

        # List widget to display the entries
        entries_list = QListWidget(entry_selector)
        for entry in entries:
            entry_text = f"Entry #{entry[1]}: {entry[2]}"
            item = QListWidgetItem(entry_text)
            entries_list.addItem(item)
        layout.addWidget(entries_list)

        # Button to delete the selected entry
        delete_button = QPushButton("Delete Selected Entry")
        delete_button.clicked.connect(lambda: self.delete_entry(entries_list.currentRow(), entry_selector))
        layout.addWidget(delete_button)

        entry_selector.setLayout(layout)
        entry_selector.exec_()

    def delete_entry(self, index, dialog):
        """Delete the selected entry."""
        entries = self.journal.get_all_entries()
        selected_entry = entries[index]
        entry_number = selected_entry[1]

        result = self.journal.delete_entry(entry_number)
        QMessageBox.information(self, "Entry Deletion", result)
        dialog.close()


#Window app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JournalApp()
    window.show()
    sys.exit(app.exec_())































