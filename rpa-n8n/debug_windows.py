from pywinauto import Desktop, Application
import time

print("Launching Notepad...")
Application(backend="uia").start("notepad.exe")
time.sleep(3)
print("Listing Windows:")
windows = Desktop(backend="uia").windows()
for w in windows:
    txt = w.window_text()
    if txt:
        print(f"Window: '{txt}'")
