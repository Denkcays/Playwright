import aiosqlite as sq

async def data_base(name, message, links_no_photo, name_no_photo, tiktokuser): 
    async with sq.connect("tiktok.db") as con:
        cur = await con.cursor()
        # await cur.execute("""DROP TABLE tiktok_messages""")
        # await cur.execute("""DROP TABLE tiktok_videos""")
        await cur.execute("""CREATE TABLE IF NOT EXISTS tiktok_messages 
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    message TEXT,
                    chat_id TEXT,
                    UNIQUE(name, message)
                ) 
        """)

        await cur.execute("""CREATE TABLE IF NOT EXISTS tiktok_videos
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video TEXT,
                    name_video TEXT,
                    chat_id TEXT,
                    UNIQUE(video, name_video)
                ) 
        """)

        for n, m in zip(name, message):
            await cur.execute("INSERT OR IGNORE INTO tiktok_messages (name, message, chat_id) VALUES (?, ?, ?)", (n, m, tiktokuser))

        for v, nv in zip(links_no_photo, name_no_photo):
            await cur.execute("INSERT OR IGNORE INTO tiktok_videos (video, name_video, chat_id) VALUES (?, ?, ?)", (v, nv, tiktokuser))

        await con.commit()