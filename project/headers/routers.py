from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F
import aiosqlite as sq

router = Router()

class tiktok(StatesGroup):
    username = State()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Hi, it's bot to show your messages in tiktok")

@router.message(Command("show_messages"))
async def show_messages(message: Message, state: FSMContext):
    await message.answer("Please, send a tiktok username")
    await state.set_state(tiktok.username)

@router.message(tiktok.username ,F.text)
async def verification(message: Message):
    tiktokuser = message.text
    async with sq.connect("tiktok.db") as con:
        cur = await con.cursor()
        await cur.execute("""SELECT chat_id FROM tiktok_messages WHERE chat_id = ?""", (tiktokuser,))
        ver = await cur.fetchone()

        if ver is not None:
            await cur.execute("""SELECT name, message FROM tiktok_messages WHERE chat_id = ?""", (tiktokuser,))            
            messages = await cur.fetchall()
            some_text = ""
            
            for item in messages:
                some = list(item)
                del item
                name = some[0]
                some_text += "\n" + name[1: -1] + ": " + some[1]
                del name
                del some

            await message.answer(some_text)
        else:
            await message.answer("This user isn't in db")

@router.message(Command("show_video"))
async def show_video(message: Message):
    pass