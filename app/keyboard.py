from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, ReplyKeyboardMarkup)
import aiosqlite, asyncio
import app.database.database as DB

def main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📝 Додати нотатку"), KeyboardButton(text="📂 Список нотаток")],
        [KeyboardButton(text='🔍 Пошук'), KeyboardButton(text="#️⃣ Теги")],
        [KeyboardButton(text='🗑 Видалити нотатку')]
    ],
    resize_keyboard=True)

async def list_tegs(user_id):
    buttons = []
    async with aiosqlite.connect(DB.DB_Main) as db:
        cursor = await db.execute('SELECT id, tags FROM main WHERE user_id = ?', (user_id,))
        tags = await cursor.fetchall()

        if len(tags) != 0:
            for tag_id, tag in tags:
                btn = KeyboardButton(text=f'{tag_id}: {tag}')
                buttons.append([btn])
        else:
            btn = KeyboardButton(text='Тегів ще не додано, введіть перший в чат')
            buttons.append([btn])
        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
