import time
from threading import Thread
import keyboard
import subprocess


# Function to simulate waiting period and send notification
def wait_and_notify(wait_time):
    print("Waiting period of {} seconds started.".format(wait_time))
    time.sleep(wait_time)  # Wait for the specified time
    message = "Waiting period is over. Time to get back to work!"
    print(message)
    try:
        notify_send("QQ waiting is over", message)
    except Exception as e:
        print("Warning: Notification failed to send.")
        print(e)
        

start_waitint_shortcut = 'ctrl+alt+w'
wait_time_default = 3


# Thread function that waits for a global shortcut to start the wait_and_notify function
def listen_for_shortcut():
    print(f"Started thread listening for {start_waitint_shortcut} running.")
    while True:
        # You can change the hotkey combination as needed
        keyboard.wait(start_waitint_shortcut)
        print("Global shortcut to start waiting detected: {}.".format(start_waitint_shortcut))
        # Start the waiting and notification process
        wait_and_notify(wait_time_default)  # Replace 10 with your desired waiting time in seconds



# https://stackoverflow.com/questions/28195805/running-notify-send-as-root    
def notify_send(title, body):
    """
    Python version of the notify-send shell function.
    """
    # Detect the name of the display in use
    # display = f":{next(os.listdir('/tmp/.X11-unix')).replace('X', '')}"

    # # Detect the user using such display
    user = subprocess.check_output(
        # f"who | grep '({display})' | awk '{{print $1}}' | head -n 1", shell=True
        f"who | awk '{{print $1}}' | head -n 1", shell=True
    ).decode().strip()

    # # Detect the id of the user
    # uid = subprocess.check_output(f"id -u {user}", shell=True).decode().strip()

    # Construct the notify-send command with the gathered information
    # command = f"sudo -u {user} DISPLAY={display} DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{uid}/bus notify-send {' '.join(args)}"
    command = f"sudo -u {user} DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send '{title}' '{body}'"

    # Execute the command
    subprocess.run(command, shell=True)

# Run the listener in a separate thread
t = Thread(target=listen_for_shortcut)
t.daemon = True  # Set the thread as a daemon thread
t.start()

# Keep the main thread running to see the output log
while True:
    time.sleep(1)