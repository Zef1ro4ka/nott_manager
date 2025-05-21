import logging, aiosqlite
from datetime import datetime, time, date
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboard as kb
import app.database.database as DB

router = Router()
logger = logging.getLogger(__name__)
date_now = datetime.now()
class add_categories(StatesGroup):
    text = State()
    tags = State()

class del_text(StatesGroup):
    text = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await DB.create_db()
    await message.answer("Hello", reply_markup=kb.main_kb())

@router.message(F.text == '📝 Додати нотатку')
async def add_notes(message: Message, state: FSMContext): 
    await message.reply("Тут ви можете додати нотатку")
    await message.answer("Напишіть свою нотатку")
    await state.set_state(add_categories.text)

@router.message(add_categories.text)
async def procces_add_notes(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(update_text = text)
    await message.answer("Тепер виберіть категорію або введіть нову якщо її немає в списку",
                        reply_markup= await kb.list_tegs(user_id=message.from_user.id))
    await state.set_state(add_categories.tags)

@router.message(add_categories.tags)
async def finis_add_notes(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text_old = await state.get_data()
    text = text_old.get("update_text")
    tags_1 = message.text
    await state.update_data(tags_new = tags_1)
    tags_old = await state.get_data()
    tags = tags_old.get("tags_new")
    await message.answer(f"{user_id},{text},{tags}")
    await DB.check_tags(user_id)
    await DB.add_notes(user_id, text, tags, date_now)
    await message.answer("Вашу нотатку успішно додано", reply_markup=kb.main_kb())
    await state.clear()
    


@router.message(Command('clear'))
async def cmd_clear_tags(message: Message):
    user_id = message.from_user.id
    await DB.clear_tag(user_id)
    await message.answer("Теги очищенно")


@router.message(F.text == '📂 Список нотаток')
async def list_notes(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect(DB.DB_Main) as db:
        cursor = await db.execute("SELECT text FROM main WHERE user_id = ?", (user_id,))
        exists = await cursor.fetchall()
        text_new = ''
        i = 1
        for text in exists:
            text_new += str(i) + ": " + str(text[0]) + "\n"
            i += 1
        await message.answer(text_new)


@router.message(F.text == '🔍 Пошук')
async def cmd_search(message: Message):
    await message.reply("Тут зможете шукати нотатки за назвою або за тегами")


@router.message(F.text == '#️⃣ Теги')
async def cmd_tegs(message: Message):
    user_id = message.from_user.id
    async with aiosqlite.connect(DB.DB_Main) as db:
        cursor = await db.execute("SELECT tags FROM main WHERE user_id = ?", (user_id,))
        exist = await cursor.fetchall()
        tags_list = [row[0] for row in exist if row[0].strip() != '']
        text_new = ''
        i = 1
        for text in tags_list:
            text_new += str(i) + ": " + str(text) + "\n"
            i += 1
        await message.answer(text_new)

@router.message(F.text == '🗑 Видалити нотатку')
async def cmd_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with aiosqlite.connect(DB.DB_Main) as db:
        cursor = await db.execute("SELECT text FROM main WHERE user_id = ?", (user_id,))
        exist = await cursor.fetchall()
        tags_list = [row[0] for row in exist if row[0].strip() != '']
        text_new = ''
        i = 1
        for text in tags_list:
            text_new += str(i) + ": " + str(text) + "\n"
            i += 1
        await message.answer(text_new)
    await message.answer("Виберіть нотатку")

    await state.set_state()

@router.message(del_text.text)
async def proccesing_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    tags = data.get("tags_list", [])

    try:
        index = int(message.text.strip()) - 1
        if index < 0 or index >= len(tags):
            raise ValueError
    except ValueError:
        await message.answer("Будь ласка, введіть правильний номер нотатки")
        return
    
    note_to_del = tags[index]

    await DB.del_text(user_id, note_to_del)
    await message.answer(f"нотатку видаленно: {note_to_del}")
    await state.clear()