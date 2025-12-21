import requests
import webbrowser

response = requests.get("https://api.github.com")
print(response.status_code)
print(response.json())

# Open a URL in default browser
webbrowser.open("https://www.google.com")

# Open in a new tab
webbrowser.open_new_tab("https://www.github.com")

# Open in a new window
webbrowser.open_new("https://www.python.org")