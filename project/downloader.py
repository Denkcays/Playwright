import asyncio

async def downloader(url: str, browser: str, directory: str):
    download = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "--cookies-from-browser", browser,
        "--user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-P", directory,
        url,
        # stdout=asyncio.subprocess.DEVNULL,
        # stderr=asyncio.subprocess.DEVNULL
    )

    await download.wait()

async def main_download(url: str, browser: str, directory: str):
    await downloader(url, browser, directory)