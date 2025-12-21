# Social Eagle — Python / RPA Examples

Short summary

This repository contains small Python scripts demonstrating simple automation and web scraping / browser automation (Playwright), UI automation (PyAutoGUI), and a few learning exercises from a "10 Days Python Challenge" (Flask, Streamlit demos).

---

## Repository layout

- `RPA/` — RPA and automation scripts
  - `social_eagle.py` — Playwright script: opens Chromium, navigates to a site, saves page body to `socialeagle_content.txt`.
  - `pyautoguidemo.py` — PyAutoGUI demo: performs simple clicks and prints mouse position.
  - Other helper scripts (e.g., `mailsending.py`, `position.py`) that use `pyautogui`.

- `10 Days Python Challenge/` — small learning projects and demos
  - `shopapi.py` — Flask endpoint (`/run-automation`) that runs a Playwright job and triggers a PyAutoGUI alert.
  - `shopapp.py` — Streamlit frontend that calls the Flask API to run automation.
  - Several one-off Python exercises and utilities.

- `.gitignore` — excludes common Python artifacts and virtualenv contents inside `RPA/` (so site-packages and venv files are not committed).

---

## Prerequisites

- Python 3.8+ (Windows instructions below are given as examples)
- pip
- Recommended: create and use a virtual environment

---

## Quick setup (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
# or
.\.venv\Scripts\activate.bat    # cmd.exe
```

2. Install required packages (example):

```powershell
pip install playwright pyautogui flask streamlit requests
```

3. Install Playwright browser binaries (required once after installing `playwright`):

```powershell
python -m playwright install
```

4. (Optional) Generate a `requirements.txt` once you have the environment set up:

```powershell
pip freeze > requirements.txt
```

---

## How to run the key demos

- Playwright script (save website text):

```powershell
python RPA/social_eagle.py
# Output: socialeagle_content.txt in repository root
```

- PyAutoGUI demo (mouse/GUI automation):

```powershell
python RPA/pyautoguidemo.py
```

Note: PyAutoGUI moves/clicks the mouse. Do not run this on a machine you aren't comfortable with it controlling.

- Flask + Streamlit automation demo:

1. Start the Flask API (run in one terminal):

```powershell
python "10 Days Python Challenge\shopapi.py"
```

2. Start the Streamlit UI (in another terminal):

```powershell
streamlit run "10 Days Python Challenge\shopapp.py"
```

Open the Streamlit app in your browser (it will show the local URL) and press **Run Automation** to trigger the Flask endpoint.

---

## Notes & best practices

- The repository intentionally ignores the `RPA/Lib/`, `RPA/Scripts/` and `RPA/pyvenv.cfg` files to avoid committing virtual environment files; keep the project source files (scripts) in the repo and *do not* commit site-packages or virtual envs.

- If you need to share environments or reproducible dependencies, add a `requirements.txt` (recommended) or `pyproject.toml`/`poetry.lock`.

- Be careful with automation scripts that control your UI (PyAutoGUI) — run them on a dedicated machine or after verifying coordinates and timeouts.

---

## If you'd like, I can:

- Add a `requirements.txt` generated from the current environment (recommended)
- Add small README badges or more detailed doc per script
- Add a CONTRIBUTING.md with guidance on what to commit to `RPA/`

---

If anything is missing or you'd like more detailed usage for a specific script, tell me which one and I'll add step-by-step instructions. ✅