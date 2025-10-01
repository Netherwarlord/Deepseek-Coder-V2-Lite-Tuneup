import tkinter as tk
from tkinter import messagebox
import os
import shutil
import subprocess
import re

# --- Core Functions ---

def move_batch_file():
    """Finds training_dataset.json in the parent project folder, renames it, and moves it here."""
    # *** CHANGE: Hardcoded the correct source file path as requested ***
    src_file = os.path.join("..", "Deepseek-Coder-v2-SwiftUI-Training", "training_dataset.json")
    data_dir = os.getcwd() # The current directory where the GUI is running.

    if not os.path.exists(src_file):
        messagebox.showerror("Error", f"Source file not found at:\n{src_file}")
        return

    try:
        batch_num = 1
        while os.path.exists(os.path.join(data_dir, f"training_dataset_batch_{batch_num:02d}.json")):
            batch_num += 1
        
        dest_filename = f"training_dataset_batch_{batch_num:02d}.json"
        dest_path = os.path.join(data_dir, dest_filename)

        # Move the file from the parent directory into the current directory with the new name
        shutil.move(src_file, dest_path)
        messagebox.showinfo("Success", f"Successfully moved and renamed batch to:\n{dest_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during move:\n{e}")


def run_combiner_and_get_count():
    """
    Runs the combiner.py script from the current directory and parses its output.
    """
    combiner_script = "combiner.py"

    try:
        if not os.path.exists(combiner_script):
            return None, f"Error: '{combiner_script}' not found in the current directory."

        result = subprocess.run(
            ['python3', combiner_script],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return None, f"Combiner script failed:\n{result.stderr}"

        match = re.search(r"Successfully combined (\d+) unique", result.stdout)
        if match:
            return int(match.group(1)), None
        else:
            return None, "Could not find unique pair count in script output."
            
    except Exception as e:
        return None, f"An error occurred while running the script:\n{e}"


def check_uniqueness():
    """Runs the combiner, updates the check count, and deletes the final file."""
    count, error = run_combiner_and_get_count()
    
    if error:
        messagebox.showerror("Check Error", error)
        return

    if count is not None:
        check_count_var.set(f"Last Check Count: {count}")
        messagebox.showinfo("Check Complete", f"Found {count} unique pairs.")
        
        final_file = "training_dataset_final.json"
        if os.path.exists(final_file):
            try:
                os.remove(final_file)
            except Exception as e:
                messagebox.showwarning("Cleanup Warning", f"Could not delete temporary file '{final_file}':\n{e}")
    else:
         messagebox.showerror("Check Error", "Failed to retrieve unique pair count.")


def build_final_dataset():
    """Runs the combiner and updates the final build count."""
    count, error = run_combiner_and_get_count()

    if error:
        messagebox.showerror("Build Error", error)
        return
        
    if count is not None:
        build_count_var.set(f"Final Build Count: {count}")
        messagebox.showinfo("Build Complete", f"Final dataset built with {count} unique pairs.\n'training_dataset_final.json' is ready.")
    else:
        messagebox.showerror("Build Error", "Failed to retrieve unique pair count.")

def validate_dataset():
    """Runs the validation script."""
    validation_script = "validate_dataset.py"
    if not os.path.exists(validation_script):
        messagebox.showerror("Error", f"Validation script '{validation_script}' not found.")
        return

    messagebox.showinfo("Validation Started", "The validation process will now begin.\nThis may take a long time. Please monitor the terminal for progress.")
    
    try:
        subprocess.run(['python3', validation_script], check=True)
        messagebox.showinfo("Validation Complete", "Validation finished. Check terminal for results and the 'clean'/'failed' files.")
    except Exception as e:
        messagebox.showerror("Validation Error", f"An error occurred while running the validation script:\n{e}")

# --- Focus Handling Functions ---

def on_focus_in(event):
    root.configure(bg=bg_color_focus)
    main_frame.configure(bg=bg_color_focus)
    button_frame.configure(bg=bg_color_focus)
    counter_frame.configure(bg=counter_bg_focus)
    check_label.configure(bg=counter_bg_focus)
    build_label.configure(bg=counter_bg_focus)
    for btn in all_buttons:
        btn.configure(bg=button_bg_focus)

def on_focus_out(event):
    root.configure(bg=bg_color_blur)
    main_frame.configure(bg=bg_color_blur)
    button_frame.configure(bg=bg_color_blur)
    counter_frame.configure(bg=counter_bg_blur)
    check_label.configure(bg=counter_bg_blur)
    build_label.configure(bg=counter_bg_blur)
    for btn in all_buttons:
        btn.configure(bg=button_bg_blur)

# --- GUI Setup ---

root = tk.Tk()
root.title("Dataset Manager")
root.geometry("580x250")

# Style variables
bg_color_blur = '#2E2E2E'
bg_color_focus = '#383838'
button_bg_blur = '#B0B0B0'
button_bg_focus = '#FFFFFF'
button_fg = '#000000'
counter_bg_blur = '#3C3C3C'
counter_bg_focus = '#464646'
font_main = ("Helvetica", 12)
font_counters = ("Helvetica", 14, "bold")

root.configure(bg=bg_color_blur)
root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out)

main_frame = tk.Frame(root, bg=bg_color_blur, padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

button_frame = tk.Frame(main_frame, bg=bg_color_blur)
button_frame.pack(pady=10)

move_button = tk.Button(button_frame, text="Move Batch", command=move_batch_file, bg=button_bg_blur, fg=button_fg, activebackground=button_bg_focus, activeforeground=button_fg, font=font_main, relief=tk.FLAT, padx=10, borderwidth=0, highlightthickness=0)
move_button.pack(side=tk.LEFT, padx=5)

check_button = tk.Button(button_frame, text="Check Uniqueness", command=check_uniqueness, bg=button_bg_blur, fg=button_fg, activebackground=button_bg_focus, activeforeground=button_fg, font=font_main, relief=tk.FLAT, padx=10, borderwidth=0, highlightthickness=0)
check_button.pack(side=tk.LEFT, padx=5)

build_button = tk.Button(button_frame, text="Build Final Dataset", command=build_final_dataset, bg=button_bg_blur, fg=button_fg, activebackground=button_bg_focus, activeforeground=button_fg, font=font_main, relief=tk.FLAT, padx=10, borderwidth=0, highlightthickness=0)
build_button.pack(side=tk.LEFT, padx=5)

validate_button = tk.Button(button_frame, text="Validate Dataset", command=validate_dataset, bg=button_bg_blur, fg=button_fg, activebackground=button_bg_focus, activeforeground=button_fg, font=font_main, relief=tk.FLAT, padx=10, borderwidth=0, highlightthickness=0)
validate_button.pack(side=tk.LEFT, padx=5)

all_buttons = [move_button, check_button, build_button, validate_button]

counter_frame = tk.Frame(main_frame, bg=counter_bg_blur, bd=2, relief=tk.GROOVE)
counter_frame.pack(pady=20, padx=10, fill=tk.X)

check_count_var = tk.StringVar(value="Last Check Count: 0")
check_label = tk.Label(counter_frame, textvariable=check_count_var, bg=counter_bg_blur, fg='#FFFFFF', font=font_counters, pady=10)
check_label.pack()

build_count_var = tk.StringVar(value="Final Build Count: 0")
build_label = tk.Label(counter_frame, textvariable=build_count_var, bg=counter_bg_blur, fg='#FFFFFF', font=font_counters, pady=10)
build_label.pack()

on_focus_in(None)
root.mainloop()

