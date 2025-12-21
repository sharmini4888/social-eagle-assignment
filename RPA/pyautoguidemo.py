import pyautogui
import time
Hi 

def main():
	# Example clicks (can be removed if not needed)
	pyautogui.click(100, 100)
	time.sleep(1)
	pyautogui.doubleClick(230, 450)

	# Give the user a moment to move the mouse if they want to capture a different position
	print("You have 3 seconds to move the mouse to the desired position...")
	time.sleep(3)

	x, y = pyautogui.position()
	print(f"Mouse position: ({x}, {y})")


if __name__ == "__main__":
	main()