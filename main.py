import time
import threading
import pygetwindow as gw
from pynput import keyboard
import subprocess

typing_speed_threshold = 15  # Adjust the threshold as per your requirements
exit_flag = False

def get_active_window():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return active_window.title
    return ""

def on_press(key):
    global keystrokes
    if hasattr(key, 'char'):
        keystrokes.append(key.char)

def detect_typing_speed():
    global keystrokes
    keystrokes = []
    start_time = time.time()

    # Start listening to keyboard events
    with keyboard.Listener(on_press=on_press) as listener:

        while not exit_flag:
            # Check if any keys were pressed
            if len(keystrokes) > 0:
                elapsed_time = time.time() - start_time
                typing_speed = len(keystrokes) / elapsed_time

                active_window = get_active_window()

                if typing_speed > typing_speed_threshold:
                    run_powershell_script()  # Run PowerShell script
                    print("Possible ducky detected!")
                    print("Typing speed:", typing_speed)
                    print("Active window:", active_window)
                    break

                # Reset keystrokes and start time for the next calculation
                keystrokes = []
                start_time = time.time()

            # Check for keyboard events without blocking
            if not listener.running:
                break

def run_powershell_script():
    script_path = r'C:fire.ps1'  # Replace with the actual path to your PowerShell script
    subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Bypass', script_path])

while not exit_flag:
    detect_typing_speed()
    time.sleep(1)  # Add a 1-second delay between each iteration
