import pyautogui
import time

# Small delay before starting
time.sleep(2)

# 1. Open Start Menu
pyautogui.press("win")
time.sleep(1)

# 2. Type Chrome
pyautogui.typewrite("chrome")
time.sleep(1)
pyautogui.press("enter")
time.sleep(3)
pyautogui.click(2216, 1235)      # Click on the address bar (change x,y for your screen)
time.sleep(4)



# 4. Click Compose (change the x,y position for your screen)
pyautogui.click(217, 430)   # <--- update these coordinates
time.sleep(2)

# 5. Type recipient email
pyautogui.typewrite("ashwinksa@gmail.com")
pyautogui.press("tab") 
pyautogui.press("tab") # move to subject box
time.sleep(1)

# 6. Type subject
pyautogui.typewrite("Good morning")
pyautogui.press("tab")  # move to message body
time.sleep(1)

# 7. Type message body
pyautogui.typewrite("Hi,\n\nWishing you a wonderful morning!\n\nRegards,\nShashwinthaa")
time.sleep(1)

# 8. Send mail (Gmail shortcut)
pyautogui.hotkey("ctrl", "enter")
