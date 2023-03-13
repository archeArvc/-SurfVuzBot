import logging
from aiogram.types import InputFile, BotCommand
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from fsm.sql_handler import sql_handlers_registration
from fsm.start_updater import reg_hnfl
from config import classter
import asyncio
from modules.TelegramUtils.commands import reg_commands_handler
from modules.TelegramUtils.text_handler import register_all


async def main():
    # Инициализируем бота
    bote = Bot(token=classter["TOKEN"], parse_mode=types.ParseMode.HTML)
    
    # Создание выделеной памяти для сохранениея состояний (Обработчик состояний modules/memory.py)
    storage = MemoryStorage()
    dp = Dispatcher(bote, storage=storage)

    # Логирование
    logging.basicConfig(level=logging.INFO)

    await dp.bot.set_my_commands([
        types.BotCommand("start", "Обновить бота ♻"),
        types.BotCommand("menu", "Главное меню")
    ])

    reg_commands_handler(dp)
    register_all(dp)
    sql_handlers_registration(dp)
    reg_hnfl(dp)

    # Установка команд
    # await set_commands(bot) 

    await dp.skip_updates()
    await dp.start_polling(timeout=0)

if __name__ == "__main__":
    asyncio.run(main())