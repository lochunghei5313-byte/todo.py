import json
import os
import argparse
import sys

# --- Configuration ---
DATA_FILE = 'todo.json'

# --- Core Functions: Instructions ---

def print_full_instructions():
    """Prints a detailed guide to all commands and their purpose."""
    print("\n📜 Available Commands:")
    print("-----------------------------------------------------------------------")
    print("1. list [--status]:") 
    print("   Purpose: Displays all tasks. Can filter by status.")
    print("   Usage: python3 todo.py **list**")
    print("   Filter: python3 todo.py list **--status pending** (Options: pending, done, all)")
    print("-----------------------------------------------------------------------")
    print("2. add <description>:")
    print("   Purpose: Creates and saves a new task to your list.")
    print("   Usage: python3 todo.py **add** 'Your new task description here'")
    print("-----------------------------------------------------------------------")
    print("3. done <task_id>:")
    print("   Purpose: Marks an existing task as complete using its **numerical ID**.")
    print("   Usage: First run 'list' to find the ID, then use: python3 todo.py **done** 1")
    print("-----------------------------------------------------------------------")
    print("4. delete <task_id>:") 
    print("   Purpose: Permanently removes a task from the list using its **numerical ID**.")
    print("   Usage: First run 'list' to find the ID, then use: python3 todo.py **delete** 1")
    print("-----------------------------------------------------------------------")
    print("5. remark <task_id> <text>:") 
    print("   Purpose: Adds a note, deadline, or remark to an existing task by ID.")
    print("   Usage: python3 todo.py **remark** 2 'Deadline: Friday 5 PM'")
    print("-----------------------------------------------------------------------")
    print("6. doneall:") 
    print("   Purpose: **Marks ALL pending tasks as complete**.")
    print("   Usage: python3 todo.py **doneall**")
    print("-----------------------------------------------------------------------")
    print("7. clear:") 
    print("   Purpose: **Permanently deletes ALL tasks** (Use with caution!).")
    print("   Usage: python3 todo.py **clear**")
    print("-----------------------------------------------------------------------")
    print("8. batch <commands>:") 
    print("   Purpose: Executes multiple commands sequentially in one line (separated by ';').")
    print("   Usage: python3 todo.py **batch** \"add 'Task A'; done 1; delete 5\"")
    print("-----------------------------------------------------------------------")
    print("-" * 75)

# --- Core Functions: Data Handling ---

def load_tasks():
    """Loads the list of tasks. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks):
    """Saves the list of tasks to the JSON file."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving tasks: {e}")


# --- Core Functions: CRUD and Batch Operations ---

def add_task(description):
    """Adds a new task."""
    tasks = load_tasks()
    
    new_id = (tasks[-1]['id'] + 1) if tasks else 1

    new_task = {
        "id": new_id,
        "description": description,
        "completed": False,
        "remark": ""
    }
    tasks.append(new_task)
    save_tasks(tasks)
    
    # Output order: 1. Instructions first
    print_full_instructions()
    # 2. Success message
    print(f"✅ Added task #{new_id}: {description}")


def list_tasks(args, print_instructions=True):
    """Lists tasks, optionally filtered by status (pending, done, or all)."""
    tasks = load_tasks()
    
    filter_status = args.status if args and hasattr(args, 'status') else 'all'

    # 1. Print instructions (if allowed by the caller)
    if print_instructions:
        print_full_instructions()

    if not tasks:
        # 2. Print empty list message
        print("🎉 Your to-do list is empty!") 
        return
    
    # Filtering logic
    if filter_status == 'pending':
        filtered_tasks = [t for t in tasks if not t['completed']]
        title = "⏳ Pending To-Do List:"
    elif filter_status == 'done':
        filtered_tasks = [t for t in tasks if t['completed']]
        title = "✅ Completed To-Do List:"
    else: # 'all'
        filtered_tasks = tasks
        title = "📝 To-Do List (All):"

    if not filtered_tasks:
        # 2. Print filter error message
        print(f"⚠️ No tasks found with status: {filter_status}")
        return
    
    # 3. Print the list on successful display
    print(f"\n{title}")
    for task in filtered_tasks:
        status = "✅" if task['completed'] else "❌"
        remark = f" [REMARK: {task.get('remark')}]" if task.get('remark') else ""
        print(f"[{status}] #{task['id']}: {task['description']}{remark}") 
        
    print("-" * 20)


def complete_task(task_id):
    """Marks the task with the specified ID as complete, and lists all tasks."""
    try:
        target_id = int(task_id)
    except ValueError:
        # 1. Print instructions
        print_full_instructions()
        # 2. Print error message
        print(f"❌ Error: Task ID '{task_id}' must be a whole number.")
        return

    tasks = load_tasks()
    found = False
    already_done = False 
    
    for task in tasks:
        if task['id'] == target_id:
            if task['completed']:
                already_done = True 
            else:
                task['completed'] = True 
            found = True
            break
    
    # 1. Print instructions (Instructions first)
    print_full_instructions()
    
    if found:
        if already_done:
            # 2. Print "already done" message
            print(f"✅ Task #{target_id} was already marked as complete.")
        else:
            save_tasks(tasks)
            # 2. Print list (print_instructions=False to avoid double instructions)
            list_tasks(argparse.Namespace(status='all'), print_instructions=False) 
            # 3. Print success message
            print(f"🎊 Task #{target_id} marked as complete!")
        
    else:
        # 2. Print "not found" message
        print(f"⚠️ Task with ID {target_id} not found.")

def delete_task(task_id):
    """Deletes the task with the specified ID."""
    try:
        target_id = int(task_id)
    except ValueError:
        # 1. Print instructions
        print_full_instructions()
        # 2. Print error message
        print(f"❌ Error: Task ID '{task_id}' must be a whole number.")
        return

    tasks = load_tasks()
    initial_count = len(tasks)

    tasks[:] = [task for task in tasks if task['id'] != target_id]
    
    # 1. Print instructions (Instructions first)
    print_full_instructions()
    
    if len(tasks) < initial_count:
        save_tasks(tasks)
        # 2. Print success message
        print(f"🗑️ Task #{target_id} has been deleted.")
    else:
        # 2. Print failure message
        print(f"⚠️ Task with ID {target_id} not found. Nothing deleted.")

def remark_task(task_id, remark_text):
    """Adds or modifies a remark/deadline for the task with the specified ID."""
    try:
        target_id = int(task_id)
    except ValueError:
        # 1. Print instructions
        print_full_instructions()
        # 2. Print error message
        print(f"❌ Error: Task ID '{task_id}' must be a whole number.")
        return

    tasks = load_tasks()
    found = False
    
    # Join list elements into a single remark string
    remark_string = " ".join(remark_text)
    
    for task in tasks:
        if task['id'] == target_id:
            task['remark'] = remark_string
            found = True
            break
    
    # 1. Print instructions (Instructions first)
    print_full_instructions()
    
    if found:
        save_tasks(tasks)
        # 2. Print success message
        print(f"📝 Remark added/updated for Task #{target_id}: '{remark_string}'")
    else:
        # 2. Print failure message
        print(f"⚠️ Task with ID {target_id} not found. Could not add remark.")

def complete_all_tasks():
    """Marks all pending tasks as complete."""
    tasks = load_tasks()
    
    updated_count = 0
    for task in tasks:
        if not task['completed']:
            task['completed'] = True
            updated_count += 1
            
    # 1. Print instructions (Instructions first)
    print_full_instructions()

    if updated_count > 0:
        save_tasks(tasks)
        # 2. Print success message
        print(f"🎉 Success! Marked **{updated_count}** pending task(s) as complete.")
    else:
        # 2. Print "no pending tasks" message
        print("✅ No pending tasks found. Everything is already done!")


def delete_all_tasks():
    """Deletes all tasks by saving an empty list."""
    tasks = load_tasks()
    initial_count = len(tasks)
    
    # 1. Print instructions (Instructions first)
    print_full_instructions()
    
    if initial_count == 0:
        # 2. Print empty list message
        print("⚠️ The to-do list is already empty. Nothing to clear.")
        return

    # Perform deletion
    save_tasks([])
    
    # 2. Print success message
    print(f"🗑️ Success! **{initial_count}** task(s) have been permanently deleted.")


def process_batch_commands(batch_string):
    """Parses and executes multiple commands from a single string."""
    
    # 1. Print instructions (Instructions first)
    print_full_instructions()
    
    # Split commands by semicolon
    commands = [cmd.strip() for cmd in batch_string.split(';') if cmd.strip()]
    
    if not commands:
        print("⚠️ Batch command is empty. Nothing to process.")
        return

    print(f"\n⚙️ Executing {len(commands)} batch command(s)...")

    # Temporary namespace for the list function
    list_namespace = argparse.Namespace(status='all')

    for i, cmd in enumerate(commands, 1):
        
        parts = cmd.split()
        if not parts:
            continue
            
        command_name = parts[0].lower()
        
        print(f"\n--- Batch Command {i}/{len(commands)}: {cmd} ---")
        
        try:
            if command_name == 'add':
                # Get all content after 'add' as the description (remove surrounding quotes)
                description = cmd[len(command_name):].strip().strip("'\"")
                if not description:
                    raise IndexError("Missing description for 'add'.")
                add_task(description)
                
            elif command_name == 'done':
                task_id = parts[1]
                complete_task(task_id)
                
            elif command_name == 'delete':
                task_id = parts[1]
                delete_task(task_id)

            elif command_name == 'remark':
                task_id = parts[1]
                # Get all content after 'remark ID' as the remark text (remove surrounding quotes)
                remark_text_raw = cmd[len(command_name) + len(task_id) + 2:].strip().strip("'\"")
                if not remark_text_raw:
                    raise IndexError("Missing remark text.")
                # remark_task expects a list for remark_text
                remark_task(task_id, [remark_text_raw])

            elif command_name == 'list':
                # Handle list arguments but prevent list from printing instructions again
                if len(parts) == 3 and parts[1].startswith('--status'):
                     list_namespace.status = parts[2]
                else:
                     list_namespace.status = 'all'
                list_tasks(list_namespace, print_instructions=False)
                
            elif command_name == 'doneall':
                complete_all_tasks()
                
            elif command_name == 'clear':
                delete_all_tasks()
                
            else:
                print(f"❌ Error: Unknown command '{command_name}'. Skipping.")
                
        except IndexError as e:
            print(f"❌ Error: {e}")
        except ValueError:
            print(f"❌ Error: Invalid ID provided for command '{command_name}'.")
        except Exception as e:
            print(f"❌ Error executing '{command_name}': {e}")
            
    print("\n--- Batch Execution Finished ---")


# --- argparse Wrapper Functions ---
# These must be defined before main()

def add_task_wrapper(description):
    add_task(description) 

def complete_task_wrapper(task_id):
    complete_task(task_id)

def delete_task_wrapper(task_id):
    delete_task(task_id)

def remark_task_wrapper(task_id, remark_text):
    remark_task(task_id, remark_text)

def complete_all_tasks_wrapper():
    complete_all_tasks()

def delete_all_tasks_wrapper():
    delete_all_tasks()
    
def process_batch_wrapper(commands_list):
    # Argparse packs arguments into a list; join them into a single string for parsing
    process_batch_commands(" ".join(commands_list))


# --- Main Logic ---

def main():
    """Handles command-line arguments using argparse."""
    
    parser = argparse.ArgumentParser(allow_abbrev=True) 
    subparsers = parser.add_subparsers(dest="command", title="commands")

    # --- LIST Command Setup ---
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('--status', type=str, choices=['pending', 'done', 'all'], 
                            default='all', nargs='?',
                            help='Filter tasks by status: "pending", "done", or "all" (default).')
    parser_list.set_defaults(func=list_tasks)

    # --- ADD Command Setup ---
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('description', type=str, nargs='+', 
                            help='The description of the task to add.')
    parser_add.set_defaults(func=add_task_wrapper) 

    # --- DONE Command Setup ---
    parser_done = subparsers.add_parser('done')
    parser_done.add_argument('task_id', type=int, help='The ID number of the task to complete.')
    parser_done.set_defaults(func=complete_task_wrapper)
    
    # --- DELETE Command Setup ---
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('task_id', type=int, help='The ID number of the task to delete.')
    parser_delete.set_defaults(func=delete_task_wrapper)

    # --- REMARK Command Setup ---
    parser_remark = subparsers.add_parser('remark')
    parser_remark.add_argument('task_id', type=int, help='The ID number of the task to add the remark to.')
    parser_remark.add_argument('remark_text', type=str, nargs='+', help='The remark or deadline to add.')
    parser_remark.set_defaults(func=remark_task_wrapper)
    
    # --- DONEALL Command Setup ---
    parser_doneall = subparsers.add_parser('doneall')
    parser_doneall.set_defaults(func=complete_all_tasks_wrapper)
    
    # --- CLEAR/DELETEALL Command Setup ---
    parser_clear = subparsers.add_parser('clear')
    parser_clear.set_defaults(func=delete_all_tasks_wrapper)
    
    # --- BATCH Command Setup ---
    parser_batch = subparsers.add_parser('batch')
    parser_batch.add_argument('commands', type=str, nargs='+', 
                              help='The string containing multiple commands separated by ";".')
    parser_batch.set_defaults(func=process_batch_wrapper)

    # 3. Parse arguments and execute
    if len(sys.argv) == 1:
        args = parser.parse_args([])
    else:
        args = parser.parse_args()


    # --- Execution Logic ---
    if args.command is None:
        # Print welcome message and full instructions only when no command is provided
        print("\n👋 Welcome to the CLI To-Do List Tool!")
        print_full_instructions()
        print("🎉 Start by using the 'add' command above!")
        
    elif hasattr(args, 'func'):
        # Execute the command logic
        if args.command == 'list':
            args.func(args)
        elif args.command == 'remark':
            args.func(args.task_id, args.remark_text)
        elif args.command == 'add':
            # Join description list into a single string
            args.func(" ".join(args.description)) 
        elif args.command in ['done', 'delete']:
            args.func(args.task_id)
        elif args.command in ['doneall', 'clear']: 
            args.func()
        elif args.command == 'batch': 
            args.func(args.commands)


if __name__ == "__main__":
    main()