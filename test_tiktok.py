from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from os import getenv

load_dotenv()

BROWSER_PROFILE_PATH = getenv("BROWSER_PROFILE_PATH")
BROWSER_EXECUTABLE = getenv("BROWSER_EXECUTABLE")  
tiktokuser = getenv("tiktokuser")

with sync_playwright() as browser:
    context = browser.chromium.launch_persistent_context(
        user_data_dir=BROWSER_PROFILE_PATH,
        executable_path=BROWSER_EXECUTABLE,
        headless=False,  
        args=["--no-sandbox", "--disable-extensions-except=", "--disable-extensions"] 
    )
    
    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://www.tiktok.com/")

    page.get_by_role(role = "link", name = "Сообщения").click()
    page.wait_for_selector("[data-e2e='dm-new-conversation-item']")
    page.locator("[data-e2e='dm-new-conversation-item']").filter(has_text = tiktokuser).click()
    
    page.click("[data-e2e='dm-new-input-editor']")
    page.type(selector = "[data-e2e='dm-new-input-editor']", text = "Это сообщение отправленно кодом на python", delay = 100)
    page.press("[data-e2e='dm-new-input-editor']", "Enter")

    page.wait_for_timeout(10000)

    context.close()