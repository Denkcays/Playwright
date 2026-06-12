from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from os import getenv
import sqlite3 as sq

load_dotenv()

BROWSER_PROFILE_PATH = getenv("BROWSER_PROFILE_PATH")
BROWSER_EXECUTABLE = getenv("BROWSER_EXECUTABLE")  
tiktokuser = getenv("tiktokuser")

name = []
message = []

with sync_playwright() as browser:
    context = browser.chromium.launch_persistent_context(
        user_data_dir=BROWSER_PROFILE_PATH,
        executable_path=BROWSER_EXECUTABLE,
        headless=False,  
        args=["--no-sandbox", "--disable-extensions-except=", "--disable-extensions"] 
    )
    
    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://www.tiktok.com/")

    page.locator("button[data-e2e='nav-messages']").click()
    page.locator("button[data-testid='dm-new-drawer-expand-btn']").click()
    page.wait_for_selector("[data-e2e='dm-new-conversation-item']")
    page.locator("[data-e2e='dm-new-conversation-item']").filter(has_text = tiktokuser).click()

    page.wait_for_timeout(10000)
    info = page.locator('[data-e2e="dm-new-message-text"]').all()

    for item in info:
        grandparent = item.locator("..").locator("..")
        name.append(grandparent.locator("a").get_attribute("href"))
        message.append(item.text_content())
    
    context.close()

    with sq.connect("tiktok.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS tiktok  
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    message TEXT,
                    UNIQUE(name, message)
                ) 
        """)

        for i in range(len(name)):
            cur.execute("INSERT INTO tiktok (name, message) VALUES (?, ?)", (name[i], message[i]))

    
    # page.click("[data-e2e='dm-new-input-editor']")
    # page.type(selector = "[data-e2e='dm-new-input-editor']", text = "Это сообщение отправленно кодом на python", delay = 100)
    # page.press("[data-e2e='dm-new-input-editor']", "Enter")