from playwright.async_api import async_playwright
#from downloader import main_download
from dotenv import load_dotenv
from random import randint
from os import getenv
import sqlite3 as sq
import asyncio

load_dotenv()

BROWSER_PROFILE_PATH = getenv("BROWSER_PROFILE_PATH")
BROWSER_EXECUTABLE = getenv("BROWSER_EXECUTABLE")  
tiktokuser = getenv("tiktokuser")

name = []
message = []
name_video = []
links = []

async def fix(captcha, page):
    if await captcha.is_visible():
        await page.locator("#captcha_close_button").click() #Sometimes it can be break

async def main():
    async with async_playwright() as browser:
        context = await browser.chromium.launch_persistent_context(
            user_data_dir=BROWSER_PROFILE_PATH,
            executable_path=BROWSER_EXECUTABLE,
            headless=False,  
            args=["--no-sandbox", "--disable-extensions-except=", "--disable-extensions"] 
        )
        
        page = context.pages[0] if context.pages else context.new_page()

        await page.goto("https://www.tiktok.com/")

        await page.locator("button[data-e2e='nav-messages']").click()
        await page.locator("button[data-testid='dm-new-drawer-expand-btn']").click()
        await page.wait_for_selector("[data-e2e='dm-new-conversation-item']")
        await page.locator("[data-e2e='dm-new-conversation-item']").filter(has_text = tiktokuser).click()

        await page.wait_for_timeout(randint(3000, 5000))
        for _ in range(2):
            first_message = page.locator('[data-e2e="dm-new-message-text"]').first
            await first_message.scroll_into_view_if_needed()
            await page.wait_for_timeout(randint(2000, 5000))

        # for _ in range(10):
        #     await page.keyboard.press("PageDown")
        #     await page.wait_for_timeout(1000)

        info = await page.locator('[data-e2e="dm-new-message-text"]').all()
        for item in info:
            grandparent = item.locator("..").locator("..")
            some_href = await grandparent.locator("a").get_attribute("href") 
            name.append(some_href)
            some_text = await item.text_content()
            message.append(some_text)

        for _ in range(15):
            first_video = page.locator(selector = "[data-e2e='dm-new-shared-video']").first
            supergrandparent = first_video.locator("..").locator("..").locator("..").locator("..").locator("..")
            video_href = await supergrandparent.locator("a").get_attribute("href")
            name_video.append(video_href)

            captcha = page.locator("#captcha-verify-container-main-page")

            if await first_video.count() == 0:
                break

            await fix(captcha, page)

            await first_video.click()
            await page.wait_for_timeout(randint(1900, 2100))
            links.append(page.url)

            await fix(captcha, page)

            #links.add(page.url)
            await page.locator(selector = "[data-e2e='browse-close']").click()
            await page.wait_for_timeout(randint(1700, 2500))

            await fix(captcha, page)

            await first_video.evaluate("el => el.remove()")
            await page.wait_for_timeout(randint(1500, 2400))

        print(f"{name}\n{message}\n{links}\n{name_video}")

        await context.close()

        # with sq.connect("tiktok.db") as con:
        #     cur = con.cursor()
        #     cur.execute("""CREATE TABLE IF NOT EXISTS tiktok  
        #             (
        #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 name TEXT,
        #                 message TEXT,
        #                 chat_id TEXT,
        #                 UNIQUE(name, message)
        #             ) 
        #     """)

        #     for n, m in zip(name, message):
        #         cur.execute("INSERT OR IGNORE INTO tiktok (name, message, chat_id) VALUES (?, ?, ?)", (n, m, tiktokuser))
        
        # page.click("[data-e2e='dm-new-input-editor']")
        # page.type(selector = "[data-e2e='dm-new-input-editor']", text = "Это сообщение отправленно кодом на python", delay = 100)
        # page.press("[data-e2e='dm-new-input-editor']", "Enter")

if __name__ == "__main__":
    asyncio.run(main())