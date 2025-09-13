import tkinter as tk
from tkinter import simpledialog
import csv
import os
from datetime import datetime, timedelta
import time
import schedule
import threading
from PIL import Image, ImageDraw
from pystray import MenuItem as item, Icon

# create requirements.txt

# --- Edit your popup configurations here  ----
LOG_FILE = 'work_log.csv' # Logs will be saved to this file
START_HOUR = 8  # Start : Morning 8o'clock
END_HOUR = 18 # End : Evening 6o'clock
INTERVAL_MINUTES = 30 # Interval in minutes
CSV_HEADER = ['date', 'day', 'time', 'task']

# --- Core Functions ---
def create_log_file_if_not_exists():
    """Checks for the log file and creates it with a header if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)

def log_task(task_description):
    """Appends a new task entry to the CSV log file."""
    now = datetime.now()
    log_entry = [
        now.strftime('%Y-%m-%d'), now.strftime('%A'), now.strftime('%H:%M'), task_description
    ]
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_entry)
    print(f"Logged at {log_entry[2]}: {task_description}") # This will only be visible if run with python.exe

def prompt_for_task():
    """Creates a custom pop-up window to ask the user what they are working on."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # --- Create a custom pop-up window (Toplevel) ---
    popup = tk.Toplevel(root)
    popup.title("Work Tracker")

    # --- Set the Width and Height here ---
    # Format is 'widthxheight'
    popup.geometry('400x150')

    # Center the window on the screen
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f'{width}x{height}+{x}+{y}')
    
    # Keep the pop-up on top of other windows
    popup.attributes("-topmost", True)

    # --- Widgets inside the pop-up ---
    tk.Label(popup, text="What are you working on?", font=("Arial", 12)).pack(pady=10)

    task_entry = tk.Entry(popup, width=50)
    task_entry.pack(pady=5, padx=10)
    task_entry.focus() # Set focus to the text box

    user_task = ""
    def on_submit():
        nonlocal user_task
        user_task = task_entry.get()
        popup.destroy()

    submit_button = tk.Button(popup, text="OK", command=on_submit)
    submit_button.pack(pady=10)
    
    # Make the Enter key trigger the submit button
    popup.bind('<Return>', lambda event: on_submit())

    # Wait until the popup is closed before continuing the script
    root.wait_window(popup)

    if user_task:  # User entered text and clicked OK
        log_task(user_task)
    else:  # User closed the dialog without submitting
        print("Prompt cancelled. No task logged for this interval.")
    
    root.destroy()

# --- functions for background operation ---
def run_schedule():
    """Sets up and runs the scheduler loop."""
    today = datetime.now().date()
    current_time_to_schedule = datetime.combine(today, datetime.min.time()).replace(hour=START_HOUR)
    end_time = current_time_to_schedule.replace(hour=END_HOUR)

    while current_time_to_schedule <= end_time:
        time_str = current_time_to_schedule.strftime('%H:%M')
        schedule.every().day.at(time_str).do(prompt_for_task)
        current_time_to_schedule += timedelta(minutes=INTERVAL_MINUTES)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def create_image():
    """Creates a simple 16x16 icon image for the system tray."""
    width = 64
    height = 64
    color1 = 'black'
    color2 = 'white'
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

def exit_action(icon):
    """Stops the icon and exits the application."""
    icon.stop()
    os._exit(0) # Force exit to ensure the scheduler thread also closes

def main():
    """Main function to run the tracker with a system tray icon."""
    create_log_file_if_not_exists()

    # Run the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Create and run the system tray icon
    image = create_image()
    menu = (item('Exit', exit_action),)
    icon = Icon("WorkTracker", image, "Work Tracker", menu)
    icon.run()

if __name__ == "__main__":
    main()