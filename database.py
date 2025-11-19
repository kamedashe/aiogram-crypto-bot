import aiosqlite
import logging

DB_NAME = "shop.db"

async def init_db():
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER
                ) 
            """)
            # Давай сразу добавим товары, если их нет (чтобы было что тестить)
            # Я помогу с логикой проверки:
            cursor = await db.execute("SELECT count(*) FROM items")
            if (await cursor.fetchone())[0] == 0:
                await db.execute("INSERT INTO items (name, price) VALUES ('Хлеб', 50)")
                await db.execute("INSERT INTO items (name, price) VALUES ('Молоко', 80)")
                await db.execute("INSERT INTO items (name, price) VALUES ('Шоколадка', 100)")
                await db.commit()
                logging.info("Default items added.")
                
        logging.info(f"Database {DB_NAME} initialized.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

async def add_item(name, price):
    # ТУТ (INSERT)
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "INSERT INTO items (name, price) VALUES (?, ?)",
                (name, price)
            )
            await db.commit()
        logging.info(f"Item {name} added.")
    except Exception as e:
        logging.error(f"Error adding item: {e}")
    pass

async def get_all_items():
    """
    Получаем товары с  БД
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM items ORDER BY id ASC")
            rows = await cursor.fetchall()
    except Exception as e:
        logging.error(f"Error getting items from database: {e}")
    return rows

async def get_item(item_id):
    """
    Получаем цену конкретного товара
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM items WHERE id = ?", (item_id,))

            row = await cursor.fetchone()

            if row:
                return dict(row)
            return None
    
    except Exception as e:
        logging.error(f"Error getting item from database: {e}")
        return None
    pass