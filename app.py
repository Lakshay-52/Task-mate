from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    deadline TEXT,
                    priority TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route("/")
def index():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    total = len(tasks)
    completed = sum(1 for task in tasks if task[2] == "Completed")
    progress = int((completed / total) * 100) if total > 0 else 0
    today = datetime.date.today().isoformat()

    return render_template("index.html", tasks=tasks, progress=progress, today=today)

# Add task
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    deadline = request.form["deadline"]
    priority = request.form["priority"]

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, status, deadline, priority) VALUES (?, ?, ?, ?)",
              (title, "Pending", deadline, priority))
    conn.commit()
    conn.close()
    return redirect("/")

# Mark complete
@app.route("/complete/<int:task_id>")
def complete(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", ("Completed", task_id))
    conn.commit()
    conn.close()
    return redirect("/")

# Delete task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Edit task (form page)
@app.route("/edit/<int:task_id>")
def edit(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()
    conn.close()
    return render_template("edit.html", task=task)

# Update after editing
@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    title = request.form["title"]
    deadline = request.form["deadline"]
    priority = request.form["priority"]

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, deadline=?, priority=? WHERE id=?",
              (title, deadline, priority, task_id))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
