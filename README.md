## To-Do List Manager (Python)

A simple, yet powerful command-line interface tool written in **Python** for managing personal and professional tasks. Tasks are persistently stored in a local `todo.json` file.

The tool features robust command wrappers, advanced capabilities like status filtering, batch operations, and a clear instruction-first output structure.

### Features

* **CRUD Operations:** Easily `add`, `list`, `done`, `delete`, and `remark` tasks.
* **Batch Processing:** Execute multiple commands in a single line using the powerful `batch` command.
* **Status Filtering:** Filter the list by `pending`, `done`, or `all` tasks.
* **Data Persistence:** Tasks are automatically saved locally in a `todo.json` file.

***

### Installation & Setup

To get started, you only need **Python 3** installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/lochunghei5313-byte/todo.py.git](https://github.com/lochunghei5313-byte/todo.py.git)
    cd todo.py
    ```

2.  **Run the script:**
    All commands start with `python3 todo.py`.

***

### Usage Guide

The tool prioritizes instructions first, followed by the output. Use single quotes (`'...'`) for descriptions or remarks that contain spaces.

#### 1. Adding Tasks (`add`)

Creates a new task.

```bash
python3 todo.py add 'Prepare Friday presentation slides'
````

#### 2\. Listing Tasks (`list`)

Displays all tasks by default, or use the optional `--status` flag to filter.

| Command | Purpose |
| :--- | :--- |
| `python3 todo.py list` | Show **all** tasks. |
| `python3 todo.py list --status pending` | Show only **pending** tasks. |

#### 3\. Marking Tasks Complete (`done`)

Marks a task using its numerical ID.

```bash
# Marks task #1 as complete
python3 todo.py done 1
```

#### 4\. Adding Remarks/Notes (`remark`)

Adds or updates a note, deadline, or remark to a task ID.

```bash
# Adds a remark to task #2
python3 todo.py remark 2 'Deadline: End of Day'
```

#### 5\. Batch Processing (`batch`)

Execute multiple commands separated by a **semicolon** (`;`) in a single string. This is ideal for quick automation.

```bash
python3 todo.py batch "add 'Review team notes'; done 3; list"
```

-----

### Maintenance Commands

| Command | Purpose |
| :--- | :--- |
| `python3 todo.py doneall` | Marks **ALL** pending tasks as complete. |
| `python3 todo.py clear` | **Permanently deletes ALL tasks** (use with caution\!). |
| `python3 todo.py delete <id>` | Deletes a single task by ID. |

-----

### Contributing

Feel free to submit issues or suggest features\!

```
```
