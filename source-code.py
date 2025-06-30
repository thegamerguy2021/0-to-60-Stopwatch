# stopwatch_app.py

import tkinter as tk
from pynput import keyboard
import threading
import time

# Stopwatch state
running = False
minutes = 0
seconds = 0
milliseconds = 0

# GUI Setup
window = tk.Tk()
window.title("0 to 60 Stopwatch")
window.geometry("250x260")
window.attributes("-topmost", True)  # Always on top

timer_label = tk.Label(window, text="00:00:000", font=("Arial", 24))
timer_label.pack(pady=10)

status_label = tk.Label(window, text="Click 'Start' or press your key.", font=("Arial", 10))
status_label.pack()

def update_timer():
    global minutes, seconds, milliseconds, running
    while running:
        time.sleep(0.01)
        milliseconds += 10
        if milliseconds >= 1000:
            milliseconds = 0
            seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}")

def toggle_stopwatch():
    global running
    running = not running
    if running:
        threading.Thread(target=update_timer, daemon=True).start()
        status_label.config(text="⏱️ Stopwatch running...")
        start_stop_button.config(text="Stop")
    else:
        status_label.config(text="⏸️ Stopwatch stopped.")
        start_stop_button.config(text="Start")

def reset_stopwatch():
    global running, minutes, seconds, milliseconds
    running = False
    minutes = 0
    seconds = 0
    milliseconds = 0
    timer_label.config(text="00:00:000")
    start_stop_button.config(text="Start")
    status_label.config(text="🔄 Stopwatch reset.")

def on_key_press(key):
    try:
        if key.char == start_key.get().lower() and not running:
            toggle_stopwatch()
        elif key.char == stop_key.get().lower() and running:
            toggle_stopwatch()
    except AttributeError:
        pass  # Handles special keys (like shift)

# Start/Stop button
start_stop_button = tk.Button(window, text="Start", command=toggle_stopwatch)
start_stop_button.pack(pady=5)

# Reset button
reset_button = tk.Button(window, text="Reset", command=reset_stopwatch)
reset_button.pack(pady=5)

# Dropdowns for selecting keys
start_key = tk.StringVar(value='w')
stop_key = tk.StringVar(value='s')

key_list = list("abcdefghijklmnopqrstuvwxyz")

tk.Label(window, text="Start Key:").pack()
start_dropdown = tk.OptionMenu(window, start_key, *key_list)
start_dropdown.pack()

tk.Label(window, text="Stop Key:").pack()
stop_dropdown = tk.OptionMenu(window, stop_key, *key_list)
stop_dropdown.pack()

# Keyboard listener (runs in the background)
listener = keyboard.Listener(on_press=on_key_press)
listener.start()

# Run the GUI
window.mainloop()

# All of this what written by chatgpt. 
