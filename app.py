from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

from flask import Flask, redirect, render_template, request, url_for, flash

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_DIR, "data")
TASKS_PATH = os.path.join(DATA_DIR, "tasks.json")

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # do flash message


@dataclass
class Task:
    id: str
    title: str
    done: bool
    created_at: str  # ISO datetime string


def ensure_storage() -> None:
    """Ensure data directory and tasks file exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TASKS_PATH):
        with open(TASKS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_tasks() -> List[Task]:
    ensure_storage()
    with open(TASKS_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    tasks: List[Task] = []
    for item in raw:
        # defensywnie na wypadek braków w pliku
        tasks.append(
            Task(
                id=str(item.get("id", "")),
                title=str(item.get("title", "")),
                done=bool(item.get("done", False)),
                created_at=str(item.get("created_at", "")),
            )
        )
    return tasks


def save_tasks(tasks: List[Task]) -> None:
    ensure_storage()
    with open(TASKS_PATH, "w", encoding="utf-8") as f:
        json.dump([asdict(t) for t in tasks], f, ensure_ascii=False, indent=2)


def find_task(tasks: List[Task], task_id: str) -> Optional[Task]:
    for t in tasks:
        if t.id == task_id:
            return t
    return None


@app.get("/")
def index():
    tasks = load_tasks()

    view = request.args.get("view", "all")  # all | active | done
    if view == "active":
        tasks_view = [t for t in tasks if not t.done]
    elif view == "done":
        tasks_view = [t for t in tasks if t.done]
    else:
        tasks_view = tasks

    # sort: newest first
    tasks_view.sort(key=lambda t: t.created_at, reverse=True)

    counts = {
        "all": len(tasks),
        "active": sum(1 for t in tasks if not t.done),
        "done": sum(1 for t in tasks if t.done),
    }

    return render_template("index.html", tasks=tasks_view, view=view, counts=counts)


@app.post("/add")
def add_task():
    title = (request.form.get("title") or "").strip()
    if len(title) < 2:
        flash("Tytuł jest za krótki (min. 2 znaki).", "danger")
        return redirect(url_for("index", view=request.args.get("view", "all")))

    tasks = load_tasks()
    new_task = Task(
        id=str(uuid.uuid4()),
        title=title,
        done=False,
        created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
    )
    tasks.append(new_task)
    save_tasks(tasks)

    flash("Dodano zadanie.", "success")
    return redirect(url_for("index", view=request.args.get("view", "all")))


@app.post("/toggle/<task_id>")
def toggle_task(task_id: str):
    tasks = load_tasks()
    t = find_task(tasks, task_id)
    if not t:
        flash("Nie znaleziono zadania.", "warning")
        return redirect(url_for("index", view=request.args.get("view", "all")))

    t.done = not t.done
    save_tasks(tasks)

    flash("Zmieniono status zadania.", "info")
    return redirect(url_for("index", view=request.args.get("view", "all")))


@app.post("/delete/<task_id>")
def delete_task(task_id: str):
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    after = len(tasks)

    if after == before:
        flash("Nie znaleziono zadania do usunięcia.", "warning")
    else:
        save_tasks(tasks)
        flash("Usunięto zadanie.", "success")

    return redirect(url_for("index", view=request.args.get("view", "all")))


@app.post("/clear_done")
def clear_done():
    tasks = load_tasks()
    tasks = [t for t in tasks if not t.done]
    save_tasks(tasks)
    flash("Usunięto wszystkie wykonane zadania.", "success")
    return redirect(url_for("index", view=request.args.get("view", "all")))


if __name__ == "__main__":
    ensure_storage()
    app.run(debug=True)
