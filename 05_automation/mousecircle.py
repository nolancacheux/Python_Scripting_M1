import pyautogui
import math
import time

# Set the radius of the circle
radius = 400

# Set the center of the circle (x, y)
center_x, center_y = pyautogui.size()
center_x //= 2
center_y //= 2

# Number of steps to complete the circle
steps = 100

# Delay between each step
delay = 0.01

for i in range(steps):
    angle = 2 * math.pi * i / steps
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    pyautogui.moveTo(x, y)
    time.sleep(delay)