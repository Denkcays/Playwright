from database_tiktok import data_base
from downloader import main_download
from browser import work_browser
from dotenv import load_dotenv
from random import randint
from os import getenv
import asyncio

load_dotenv()

BROWSER_PROFILE_PATH = getenv("BROWSER_PROFILE_PATH")
BROWSER_EXECUTABLE = getenv("BROWSER_EXECUTABLE")  
tiktokuser = getenv("tiktokuser")
directory = getenv("directory")
get_browser = getenv("get_browser")

async def main():
    name, message, links_no_photo, name_no_photo = await work_browser(BROWSER_PROFILE_PATH, BROWSER_EXECUTABLE, tiktokuser)

    for url in links_no_photo:
        await main_download(url, get_browser ,directory)
        await asyncio.sleep(randint(2, 5))

    await data_base(name, message, links_no_photo, name_no_photo, tiktokuser)

if __name__ == "__main__":
    asyncio.run(main())