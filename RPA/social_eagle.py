from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to the website
        page.goto("https://google.com")

        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")

        # Extract all visible text from the page
        page_text = page.inner_text("body")

        # Save the text into a new file
        with open("socialeagle_content.txt", "w", encoding="utf-8") as f:
            f.write(page_text)

        print("✔ Text copied and saved into socialeagle_content.txt")

        browser.close()

if __name__ == "__main__":
    run()
