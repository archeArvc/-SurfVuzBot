from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from modules.data_base import edit_dops, get_data, update, updata_math_profile
from keyboards.reply import main
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
from keyboards.inline import profiles_data


class stater(StatesGroup):
    filter_drop = State()
    write_city = State()


callabel_dop = CallbackData("dop", "active")

async def call_dop_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    print(callback_data)
    if callback_data.get("@") == "dop":
        if callback_data.get("active") == "1":
            result = await asyncio.gather(edit_dops(call.from_user.id, 1))
            if result[0] == "succes":
                res = await asyncio.gather(get_data(call.from_user.id))
                print(res)
                splited_subs = res[0][2].split(" ")
                if res[0][3] == 1:
                    dops = "Да"
                elif res[0][3] == 2:
                    dops = "Нет"
                
                if res[0][4] == 2:
                    math_profile = "База"
                elif res[0][4] == 1:
                    math_profile = "Профильная"
                await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                photo = InputFile(f"{Path.cwd()}\\photos\\filters.png")
                await call.message.answer_photo(
                    photo=photo,
                    caption=f"Ваши фильтры:\n\n*Город:* {res[0][1]}\n*Предметы:* {', '.join(splited_subs)}\n*Входные экзамены:* {dops}\n*Математика:* {math_profile}", 
                    parse_mode=types.ParseMode.MARKDOWN_V2
                    )
            else:
                print(result[0])
        elif callback_data.get("active") == "2":
            result = await asyncio.gather(edit_dops(call.from_user.id, 2))
            if result[0] == "succes":
                res = await asyncio.gather(get_data(call.from_user.id))
                splited_subs = res[0][2].split(" ")
                if res[0][3] == 1:
                    dops = "Да"
                elif res[0][3] == 2:
                    dops = "Нет"
                
                if res[0][4] == 2:
                    math_profile = "База"
                elif res[0][4] == 1:
                    math_profile = "Профильная"
                await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                photo = InputFile(f"{Path.cwd()}\\photos\\filters.png")
                await call.message.answer_photo(
                    photo=photo,
                    caption=f"Ваши фильтры:\n\n*Город:* {res[0][1]}\n*Предметы:* {', '.join(splited_subs)}\n*Входные экзамены:* {dops}\n*Математика:* {math_profile}", 
                    parse_mode=types.ParseMode.MARKDOWN_V2
                    )
            else:
                print(result[0])


async def wrt_ct(message: types.Message, state: FSMContext):
    print(message.text.capitalize())
    get_cities_array = await asyncio.gather(get_all_cities())
    if message.text.capitalize() not in get_cities_array[0]:
        await message.answer("Такого города нет 🤔\nПопробуй ещё раз")
        return
    get_data_for_update = message.text.capitalize()
    updated = await asyncio.gather(update(message.from_user.id, get_data_for_update))
    print(updated[0])

    if updated[0] == "succes":
        res = await asyncio.gather(get_data(message.from_user.id))
        splited_subs = res[0][2].split(" ")
        if res[0][3] == 1:
            dops = "Да"
        elif res[0][3] == 2:
            dops = "Нет"

        if res[0][4] == 2:
            math_profile = "База"
        elif res[0][4] == 1:
            math_profile = "Профильная"
        photo = InputFile(f"{Path.cwd()}\\photos\\filters.png")
        await message.answer_photo(
            photo=photo,
            caption=f"Ваши фильтры:\n\n*Город:* {res[0][1]}\n*Предметы:* {', '.join(splited_subs)}\n*Входные экзамены:* {dops}\n*Математика:* {math_profile}",
            parse_mode=types.ParseMode.MARKDOWN_V2
            )
    await state.finish()

async def get_all_cities():
    async with aiohttp.ClientSession() as ses:
        # получаем html страницу с сайта
        response = await ses.get(url="https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B/%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%B0")
        # подключаем bs4 для разбора html'ки
        sp = BeautifulSoup(await response.text(), "lxml")

        all_cities = sp.find_all("div", class_="label-part main-top-region first")
        only_cyti = []

        for city in all_cities:
            s = getattr(city.find("a"), 'text', None)
            only_cyti.append(s)
        only_cyti.append("Питер")
        only_cyti = only_cyti[1:]
        await ses.close()
    return only_cyti


async def profiles_update(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("act") == "1":
        await asyncio.gather(updata_math_profile(call.from_user.id, 1))
        res = await asyncio.gather(get_data(call.from_user.id))
        splited_subs = res[0][2].split(" ")
        if res[0][3] == 1:
            dops = "Да"
        elif res[0][3] == 2:
            dops = "Нет"
        print(res[0][4])
        if res[0][4] == 2:
            math_profile = "База"
        elif res[0][4] == 1:
            math_profile = "Профильная"
        await call.message.edit_text("Данные успешно обновленны!")
        await asyncio.sleep(1)
        await call.message.delete()
        photo = InputFile(f"{Path.cwd()}\\photos\\filters.png")
        await call.message.answer_photo(
            photo=photo,
            caption=f"Ваши фильтры:\n\n*Город:* {res[0][1]}\n*Предметы:* {', '.join(splited_subs)}\n*Входные экзамены:* {dops}\n*Математика:* {math_profile}",
            parse_mode=types.ParseMode.MARKDOWN_V2
            )
        
            
    elif callback_data.get("act") == "2":
        await asyncio.gather(updata_math_profile(call.from_user.id, 2))
        res = await asyncio.gather(get_data(call.from_user.id))
        splited_subs = res[0][2].split(" ")
        if res[0][3] == 1:
            dops = "Да"
        elif res[0][3] == 2:
            dops = "Нет"
        print(res[0][4])
        if res[0][4] == 2:
            math_profile = "База"
        elif res[0][4] == 1:
            math_profile = "Профильная"
        await call.message.edit_text("Данные успешно обновленны!")
        await asyncio.sleep(1)
        await call.message.delete()
        photo = InputFile(f"{Path.cwd()}\\photos\\filters.png")
        await call.message.answer_photo(
            photo=photo,
            caption=f"Ваши фильтры:\n\n*Город:* {res[0][1]}\n*Предметы:* {', '.join(splited_subs)}\n*Входные экзамены:* {dops}\n*Математика:* {math_profile}",
            parse_mode=types.ParseMode.MARKDOWN_V2
            )


def sql_handlers_registration(dp: Dispatcher):
    dp.register_callback_query_handler(call_dop_handler, callabel_dop.filter(), state="*")
    dp.register_message_handler(wrt_ct, state=stater.write_city)
    dp.register_callback_query_handler(profiles_update, profiles_data.filter(), state="*")