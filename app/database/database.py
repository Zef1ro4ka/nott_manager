import aiosqlite

DB_Main = 'main.sql'

async def create_db():
    async with aiosqlite.connect(DB_Main) as db:
        await db.execute('''
                    CREATE TABLE IF NOT EXISTS main(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        text TEXT,
                        tags TEXT,
                        date_created TEXT)
''')
        await db.commit()

async def add_notes(user_id, text, tags, date):
    async with aiosqlite.connect(DB_Main) as db:
        await db.execute('''
                        INSERT INTO main (user_id, text, tags, date_created)
                        VALUES(?, ?, ?, ?)
''', (user_id, text, tags, date))
        await db.commit()

async def check_tags(tag):
    async with aiosqlite.connect(DB_Main) as db:
        cursor = await db.execute("SELECT 1 FROM main WHERE tags = ?", (tag,))
        exist = await cursor.fetchone()

        if not exist:
            await db.execute("INSERT INTO main (tags) VALUES (?)", (tag,))
            await db.commit()
        else:
            print("Такий тег вже існує")

async def clear_tag(user_id):
    async with aiosqlite.connect(DB_Main) as db:
        await db.execute("UPDATE main SET tags = '' WHERE user_id = ?", (user_id,))
        await db.commit()

async def del_text(user_id, text):
    async with aiosqlite.connect(DB_Main) as db:
        await db.execute("DELETE FROM main WHERE user_id = ? AND text = ?", (user_id, text,))  
        await db.commit()