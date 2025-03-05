from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

todo_file = "todo_list.json"

def load_tasks():
    if os.path.exists(todo_file):
        with open(todo_file, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(todo_file, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get("task")
    if task:
        tasks = load_tasks()
        tasks.append({"task": task, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route('/mark_done/<int:task_index>')
def mark_done(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index]["done"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route('/delete/<int:task_index>')
def delete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
        save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
