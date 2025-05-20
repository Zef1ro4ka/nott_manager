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

async def add_notes(user_id, text, tags):
    async with aiosqlite.connect(DB_Main) as db:
        await db.execute('''
                        INSERT INTO main (user_id, text, tags)
                        VALUES(?, ?, ?)
''', (user_id, text, tags,))
        await db.commit()

async def check_tags(tag):
    async with aiosqlite.connect(DB_Main) as db:
        cursor = await db.execute("ISELECT 1 FROM main WHERE tags = ?", (tag,))
        exist = await cursor.fetchone()

        if not exist:
            await db.execute("INSERT INTO main (tags) VALUES (?)", (tag,))
            await db.commit()
        else:
            print("Такий тег вже існує")