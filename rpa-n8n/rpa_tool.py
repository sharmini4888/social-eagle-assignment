import sys
import os
import time
from pywinauto import Desktop, Application

FILENAME = "automation_log.txt"
# Ensure we map to the script's directory (rpa-n8n), not the CWD
HEAD_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(HEAD_DIR, FILENAME)
print(f"Target File Path: {FILE_PATH}")

def automate_notepad(text):
    file_exists = os.path.exists(FILE_PATH)
    
    # 1. Look for existing relevant windows first
    main_window = None
    existing_windows = Desktop(backend="uia").windows()
    
    # Case A: automation_log.txt is already open
    for w in existing_windows:
        if FILENAME in w.window_text():
            print(f"Found existing target window: {w.window_text()}")
            main_window = w
            target_title_part = FILENAME
            break
            
    # Case B: Untitled/Notepad is open (and we accept it to start)
    if not main_window:
        for w in existing_windows:
            if "Untitled" in w.window_text() or "Notepad" == w.window_text().strip():
                 print(f"Found existing Untitled/Notepad window: {w.window_text()}")
                 main_window = w
                 target_title_part = "Notepad"
                 break

    # 2. If no window found, Launch appropriate one
    if not main_window:
        if file_exists:
            print(f"Opening existing file: {FILE_PATH}")
            Application(backend="uia").start(f"notepad.exe \"{FILE_PATH}\"")
            target_title_part = FILENAME
        else:
            print("Launching new Notepad...")
            Application(backend="uia").start("notepad.exe")
            target_title_part = "Notepad"

    # 3. Wait/Confirm Window
    if not main_window:
        print("Waiting for window...")
        for i in range(30):
            windows = Desktop(backend="uia").windows()
            for w in windows:
                if target_title_part in w.window_text() or "Notepad" in w.window_text():
                    main_window = w
                    print(f"Acquired window: {main_window.window_text()}")
                    break
            if main_window:
                break
            time.sleep(1)

    if not main_window:
        raise Exception("Could not find Notepad window")

    try:
        main_window.set_focus()
    except Exception as e:
        print(f"Focus warning: {e}")

    time.sleep(1)

    # 4. Navigate/Prep
    # If it's our file, go to end. If it's Untitled, we assume empty or we just append.
    main_window.type_keys("^{END}")
    main_window.type_keys("{ENTER}") 
    
    # 5. Type Text
    for char in text:
        if char == '\n':
            main_window.type_keys("{ENTER}")
        else:
            main_window.type_keys(char, with_spaces=True)
            
    # 6. Save
    print("Sending Save command...")
    main_window.type_keys("^s")
    
    # Check for Save As dialog
    try:
        # Wait a bit longer for the dialog
        save_as_window = Desktop(backend="uia").window(title="Save As")
        if save_as_window.exists(timeout=10):
            print("Save As dialog detected.")
            
            # Debug: print structure if we fail, but let's try standard IDs first
            # Windows 11 Notepad Save As is a modern dialog but often retains structure or accessible IDs
            # Typically "File name:" is a ComboBox (AppControlHost) -> Edit check
            
            entered_path = False
            
            # Try 1: Modern UIA name-based
            try:
                # Often the Edit control is named "File name:" directly in UIA
                save_as_window.child_window(title="File name:", control_type="Edit").set_edit_text(FILE_PATH)
                entered_path = True
            except:
                pass
            
            # Try 2: Classic ID 1001 (Edit) inside the Combo
            if not entered_path:
                try:
                     # Attempt to find the edit by ID (works in many common dialogs)
                     # Note: In UIA backend auto_id is string
                     save_as_window.child_window(auto_id="1001").set_text(FILE_PATH)
                     entered_path = True
                except:
                    pass

            # Try 3: First Edit control found
            if not entered_path:
                print("Fallback: finding first Edit control...")
                edits = save_as_window.descendants(control_type="Edit")
                if edits:
                    edits[0].set_text(FILE_PATH)
                    entered_path = True
            
            if entered_path:
                print(f"Path entered: {FILE_PATH}")
                time.sleep(0.5)
                # Click Save button (typically 'Save' or ID 1)
                save_as_window.type_keys("{ENTER}") # Enter usually triggers Save
            else:
                print("Could not find File Name field! Dumping identifiers:")
                save_as_window.print_control_identifiers()
            
            # Helper for Overwrite confirmation
            try:
                confirm_save = Desktop(backend="uia").window(title_re=".*Confirm Save As.*")
                if confirm_save.exists(timeout=2):
                    print("Handling overwrite confirmation...")
                    confirm_save.type_keys("%y") # Alt+Y
            except:
                pass

    except Exception as e:
        print(f"Save As interaction error: {e}")

    time.sleep(2) 

    # 7. Verification and Close
    if not os.path.exists(FILE_PATH):
        print(f"WARNING: File {FILE_PATH} was not found after saving!")
    else:
        print(f"Verified: File exists at {FILE_PATH}")

    print("Closing Notepad...")
    main_window.close()
    
    # Handle "Do you want to save changes?"
    try:
        # Check for generalized dialogs
        save_changes = Desktop(backend="uia").window(title_re=".*Notepad.*", found_index=0) 
        if save_changes.exists(timeout=2):
             # Look for "Don't Save" button specifically?
             # But if we are here, we FAILED to save or verified earlier.
             # Safe to discard to clean up.
             print("Closing 'Save Changes' dialog (discarding)...")
             save_changes.type_keys("%n") 
    except:
        pass

    print("Automation completed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rpa_tool.py \"Text to type\"")
        sys.exit(1)
    
    input_text = sys.argv[1]
    automate_notepad(input_text)
