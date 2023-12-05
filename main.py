import time
from threading import Thread
from plyer import notification
import keyboard


# Function to simulate waiting period and send notification
def wait_and_notify(wait_time):
    print("Waiting period of {} seconds started.".format(wait_time))
    time.sleep(wait_time)  # Wait for the specified time
    message = "Waiting period is over. Time to get back to work!"
    print(message)
    try:
        notification.notify(
            title='QuantumQueue Alert',
            message='Waiting period is over. Time to get back to work!',
            app_name='QuantumQueue'
        )
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

# Run the listener in a separate thread
t = Thread(target=listen_for_shortcut)
t.daemon = True  # Set the thread as a daemon thread
t.start()

# Keep the main thread running
while True:
    time.sleep(1)