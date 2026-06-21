from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F
from pathlib import Path
import aiosqlite as sq

router = Router()

class tiktok(StatesGroup):
    message_username = State()
    video_username = State()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Hi, it's bot to show your messages in tiktok")

@router.message(Command("show_messages"))
async def show_messages(message: Message, state: FSMContext):
    await message.answer("Please, send a tiktok username")
    await state.set_state(tiktok.message_username)

@router.message(tiktok.message_username)
async def verification_message(message: Message, state: FSMContext):
    tiktokuser = message.text
    async with sq.connect("tiktok.db") as con:
        cur = await con.cursor()
        await cur.execute("""SELECT chat_id FROM tiktok_messages WHERE chat_id = ?""", (tiktokuser,))
        ver = await cur.fetchone()

        if ver is not None:
            await cur.execute("""SELECT name, message FROM tiktok_messages WHERE chat_id = ?""", (tiktokuser,))            
            messages = await cur.fetchall()

            del cur
            del ver
            del con
            del tiktokuser

            some_text = ""
            
            for item in messages:
                some = list(item)
                del item
                name = some[0]
                some_text += "\n" + name[1:] + ": " + some[1]
                del name
                del some

            await message.answer(some_text)
        else:
            await message.answer("This user isn't in db")

    await state.clear()

def get_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text = "⬅️ Назад", callback_data = "video_back"), 
            InlineKeyboardButton(text = "➡️ Вперёд", callback_data = "video_next")],
        ]
    )
    return keyboard

async def send_video_by_index(target_message: Message, data: dict, index: int):
    videos = data["videos"]
    names = data["names"]

    video_url = videos[index][0]
    video_num = video_url.split("/")[-1]

    video_dir = Path("~/Denkcays/Playwright/video/").expanduser()
    mp4_files = [file.name for file in video_dir.glob("*.mp4")]

    video_filename = None
    for i in mp4_files:
        if video_num in i:
            video_filename = i
            break

    if video_filename is None:
        await target_message.answer("Видео файл не найден")
        return

    fullvideo = video_dir / video_filename
    some = FSInputFile(str(fullvideo))

    await target_message.answer_video(
        some,
        caption=names[index][0][1:],
        reply_markup=get_keyboard()
    )

@router.message(Command("show_video"))
async def show_video(message: Message, state: FSMContext):
    await message.answer("Please, send a tiktok username")
    await state.set_state(tiktok.video_username)

@router.message(tiktok.video_username)
async def verification_video(message: Message, state: FSMContext):
    tiktokuser = message.text
    async with sq.connect("tiktok.db") as con:
        cur = await con.cursor()
        await cur.execute("""SELECT chat_id FROM tiktok_videos WHERE chat_id = ?""", (tiktokuser,))
        ver = await cur.fetchone()

        if ver is not None:
            await cur.execute("""SELECT name_video FROM tiktok_videos WHERE chat_id = ?""", (tiktokuser,))
            names = await cur.fetchall()
            await cur.execute("""SELECT video FROM tiktok_videos WHERE chat_id = ?""", (tiktokuser,))
            videos_url = await cur.fetchall()

            await state.update_data(videos = videos_url, names = names, index = 0)

            data = await state.get_data()
            await send_video_by_index(message, data, 0)
        else:
            await message.answer("This user isn't in db")
    await state.set_state(None)

@router.callback_query(F.data == "video_next")
async def next_video(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = min(data["index"] + 1, len(data["videos"]) - 1)
    await state.update_data(index=index)

    await send_video_by_index(callback.message, data, index)
    await callback.answer()


@router.callback_query(F.data == "video_back")
async def prev_video(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = max(data["index"] - 1, 0)
    await state.update_data(index=index)

    await send_video_by_index(callback.message, data, index)
    await callback.answer()