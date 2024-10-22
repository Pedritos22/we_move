from flask import Flask, render_template, request, redirect, url_for
import sys
import sqlite3
import time

from Journal_M import Journal
from Self_Goals import TaskList

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    journal = Journal()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mood = request.form['mood']
        journal.add_new_entry(title, content, mood)
        return redirect(url_for('journal'))

    entries = journal.get_all_entries()
    return render_template('journal.html', entries=entries)

@app.route('/self_goals', methods=['GET', 'POST'])
def self_goals():
    task_list = TaskList()
    if request.method == 'POST':
        task_description = request.form['task']
        task_list.add_task(task_description)
        return redirect(url_for('self_goals'))

    tasks = task_list.show_tasks()
    return render_template('self_goals.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
