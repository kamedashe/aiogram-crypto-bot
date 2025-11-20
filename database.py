from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from models import Base, Item

# Подключаемся к файлу bot.db (SQLAlchemy создаст его сама)
engine = create_async_engine(url='sqlite+aiosqlite:////bot.db')
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    """Создаем таблицы и наполняем тестовыми данными"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Проверка: если товаров нет, добавим их
    async with async_session() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        
        if not items:
            session.add(Item(name='MacBook Air', price=1000))
            session.add(Item(name='iPhone 15', price=800))
            session.add(Item(name='AirPods Pro', price=200))
            await session.commit()
            print("✅ Тестовые товары добавлены в базу")

async def get_all_items():
    """Получить все товары"""
    async with async_session() as session:
        query = select(Item)
        result = await session.execute(query)
        return result.scalars().all()

async def get_item(item_id):
    """Получить один товар по ID"""
    async with async_session() as session:
        query = select(Item).where(Item.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()