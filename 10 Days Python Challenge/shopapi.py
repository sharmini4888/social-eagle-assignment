from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
import pyautogui
import threading

app = Flask(__name__)

def show_alert(title):
    pyautogui.alert(
        text=f"Website title fetched successfully!\n{title}",
        title="Automation Alert",
        button="OK"
    )

@app.route("/run-automation")
def run_automation():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com", timeout=60000)
            title = page.title()
            browser.close()

        # 🔥 PyAutoGUI runs INSIDE Flask
        threading.Thread(
            target=show_alert,
            args=(title,),
            daemon=True
        ).start()

        return jsonify({
            "status": "success",
            "website_title": title
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(port=5000, debug=False)
