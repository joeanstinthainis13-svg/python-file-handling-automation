"""
file_automation.py
-------------------
GOAL: Demonstrate Python file handling, automation logic, and exception
handling using simple, well-commented code.

WHAT THIS SCRIPT DOES
1. Writes and reads a CSV file (student records).
2. Writes and reads a TXT file (a log file).
3. Automates file operations: RENAME, MOVE, and DELETE.
4. Wraps every risky operation in try-except so the program never
   crashes—it reports the error and keeps going.

Run it with:
    python file_automation.py
"""

import csv
import os
import shutil

# --------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------

WORKSPACE = "workspace"
ARCHIVE_DIR = os.path.join(WORKSPACE, "archive")
CSV_FILE = os.path.join(WORKSPACE, "students.csv")
LOG_FILE = os.path.join(WORKSPACE, "activity_log.txt")
TEMP_FILE = os.path.join(WORKSPACE, "temp_cache.txt")


def setup_workspace():
    """Create workspace and archive folders."""
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    print(f"[SETUP] Workspace ready at '{WORKSPACE}/'\n")


# --------------------------------------------------------------------------
# CSV FILE HANDLING
# --------------------------------------------------------------------------

def write_csv_file():
    """Write sample student records to a CSV file."""

    sample_data = [
        ["Name", "Subject", "Marks"],
        ["Asha", "Python", 88],
        ["Ravi", "Python", 92],
        ["Meera", "Python", 79],
    ]

    try:
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)

        print(f"[CSV] Wrote {len(sample_data) - 1} records to '{CSV_FILE}'")

    except OSError as e:
        print(f"[ERROR] Could not write CSV file: {e}")


def read_csv_file():
    """Read and display the CSV file."""

    try:
        with open(CSV_FILE, mode="r", newline="") as f:
            reader = csv.reader(f)

            print(f"\n[CSV] Contents of '{CSV_FILE}':")

            for row in reader:
                print(" ", row)

            print()

    except FileNotFoundError:
        print(f"[ERROR] '{CSV_FILE}' does not exist.\n")


# --------------------------------------------------------------------------
# TEXT FILE HANDLING
# --------------------------------------------------------------------------

def write_log(message):
    """Append a line to the activity log."""

    try:
        with open(LOG_FILE, mode="a") as f:
            f.write(message + "\n")

    except OSError as e:
        print(f"[ERROR] Could not write to log file: {e}")


def read_log_file():
    """Display the activity log."""

    try:
        with open(LOG_FILE, mode="r") as f:

            print(f"[TXT] Contents of '{LOG_FILE}':")

            for line in f:
                print(" ", line.rstrip())

            print()

    except FileNotFoundError:
        print(f"[ERROR] '{LOG_FILE}' does not exist.\n")


# --------------------------------------------------------------------------
# RENAME FILE
# --------------------------------------------------------------------------

def rename_file(old_path, new_path):
    """Rename a file safely."""

    try:
        os.rename(old_path, new_path)

        print(f"[RENAME] '{old_path}' -> '{new_path}'")
        write_log(f"RENAMED: {old_path} -> {new_path}")

    except FileNotFoundError:
        print(f"[ERROR] Cannot rename: '{old_path}' not found.")

    except FileExistsError:
        print(f"[ERROR] Cannot rename: '{new_path}' already exists.")


# --------------------------------------------------------------------------
# MOVE FILE
# --------------------------------------------------------------------------

def move_file(src_path, dest_dir):
    """Move a file into another directory."""

    try:
        if not os.path.exists(src_path):
            raise FileNotFoundError(src_path)

        shutil.move(src_path, dest_dir)

        print(f"[MOVE] '{src_path}' -> '{dest_dir}/'")
        write_log(f"MOVED: {src_path} -> {dest_dir}")

    except FileNotFoundError as e:
        print(f"[ERROR] Cannot move: '{e}' not found.")

    except shutil.Error as e:
        print(f"[ERROR] Move failed: {e}")


# --------------------------------------------------------------------------
# DELETE FILE
# --------------------------------------------------------------------------

def delete_file(path):
    """Delete a file safely."""

    try:
        os.remove(path)

        print(f"[DELETE] Removed '{path}'")
        write_log(f"DELETED: {path}")

    except FileNotFoundError:
        print(f"[ERROR] Cannot delete: '{path}' does not exist.")

    except PermissionError:
        print(f"[ERROR] Cannot delete: No permission for '{path}'.")


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():

    setup_workspace()

    write_log("=== New session started ===")

    # CSV Demo
    write_csv_file()
    read_csv_file()

    write_log("CSV file created and read successfully")

    # Log Demo
    read_log_file()

    # Temporary file
    with open(TEMP_FILE, "w") as f:
        f.write("This is a temporary cache file.\n")

    print(f"[SETUP] Created temporary file '{TEMP_FILE}'\n")

    # Rename
    renamed_csv = os.path.join(WORKSPACE, "students_backup.csv")
    rename_file(CSV_FILE, renamed_csv)

    # Move
    move_file(renamed_csv, ARCHIVE_DIR)

    # Delete
    delete_file(TEMP_FILE)

    # Exception Handling Demo
    print("\n[DEMO] Intentionally triggering errors:\n")

    read_csv_file()                    # CSV no longer exists
    delete_file(TEMP_FILE)             # Already deleted
    rename_file("ghost_file.csv", "x.csv")   # Doesn't exist

    # Final Log
    print()
    read_log_file()

    print("[DONE] Script finished without crashing.")


if __name__ == "__main__":
    main()