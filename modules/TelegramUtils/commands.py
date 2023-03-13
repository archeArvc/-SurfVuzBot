from aiogram import types, Dispatcher
import asyncio as asy
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from keyboards.reply import main
from pathlib import Path

from fsm.start_updater import bs_inline, AnotherState
from modules.data_base import check_data

async def start_start(message: types.Message, state: FSMContext):
    res = await asy.gather(check_data(message.from_user.id))
    print(type(res[0]), res[0])
    await message.answer(f"Привет <a href='t.me/{message.from_user.username}'>{message.from_user.full_name}🤗</a>", parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
    await asy.sleep(0.5)
    await message.answer("Из какого ты города?\nОтправь в чат")
    await state.set_state(AnotherState.test.state)


async def menu(message: types.Message):
    photo = InputFile(f"{Path.cwd()}\\photos\\hello.png")
    await message.answer_photo(photo=photo, caption="Добро пожаловать!", reply_markup=main)

# async def delete(message: types.Message):
#     res = await asy.gather(upload_subject(message.from_user.id, "Физика"))
#     await message.answer(text=res)



def reg_commands_handler(dp: Dispatcher):
    dp.register_message_handler(start_start, commands=['start'])
    dp.register_message_handler(menu, commands=["menu"])
    
    # dp.register_message_handler(delete, commands=['delete'])