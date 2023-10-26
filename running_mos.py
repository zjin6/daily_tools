import win32api
import win32con
import time
import random


start_time = time.time()  # Get current time
close_time = start_time + int(input("Enter close time in minutes: ")) * 60

while time.time() < close_time:
    print("Moving mouse at", time.strftime("%H:%M:%S"))
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
    interval = random.randint(180, 360)  # Random interval between 3 and 6 minutes
    time.sleep(interval)

print('running closed.')