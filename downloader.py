import asyncio

async def downloader(url: str):
    download = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "--cookies-from-browser", "brave",
        "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-P", "~/Denkcays/Playwright/video/",
        url,
        # stdout=asyncio.subprocess.DEVNULL,
        # stderr=asyncio.subprocess.DEVNULL
    )

    await download.wait()

async def main_download(url: str):
    await downloader(url)
    #yt-dlp --cookies-from-browser brave --user-agent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" -P "~/Denkcays/Playwright/video/" "https://www.tiktok.com/@sythexnx/video/7648458864916057365"

if __name__ == "__main__":
    asyncio.run(main_download())