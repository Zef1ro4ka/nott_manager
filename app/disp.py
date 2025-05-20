import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboard as kb
import app.database.database as DB

router = Router()
logger = logging.getLogger(__name__)

class add_categories(StatesGroup):
    text = State()
    tags = State()

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
    


@router.message(F.text == '📂 Список нотаток')
async def list_notes(message: Message):
    await message.reply("Тут буде ваш список нотаток")

@router.message(F.text == '🔍 Пошук')
async def cmd_search(message: Message):
    await message.reply("Тут зможете шукати нотатки за назвою або за тегами")

@router.message(F.text == '#️⃣ Теги')
async def cmd_tegs(message: Message):
    await message.reply("Тут будуть ваші теги")

@router.message(F.text == '🗑 Видалити нотатку')
async def cmd_delete(message: Message):
    await message.reply("Тут зможете видаляти повідомлення")