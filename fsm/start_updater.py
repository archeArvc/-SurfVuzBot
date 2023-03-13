# Получение списка городов России с вузами
from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import lxml
from modules.data_base import insert_data, get_data
from keyboards.inline import subsidii, preset1, preset2, preset3, get_subs_array_one, get_subs_array_two, get_subs_array_three, convert, bs, bs_inline
from keyboards.inline import ok_mrk

class AnotherState(StatesGroup):
    test = State()
    count_subjects = State()


async def get_all_cities():
    async with aiohttp.ClientSession() as ses:
        # получаем html страницу с сайта
        response = await ses.get(url="https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B/%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%B0")
        # подключаем bs4 для разбора html'ки
        sp = BeautifulSoup(await response.text(), "lxml")

        all_cities = sp.find_all("div", class_="label-part main-top-region first")
        only_cyti = []

        for city in all_cities:
            links = city.find("a")
            s = getattr(city.find("a"), 'text', None)
            only_cyti.append(s)
        only_cyti = only_cyti[1:]
        await ses.close()
    return only_cyti


async def messaged(message: types.Message, state: FSMContext):
    get_cities_array = await asyncio.gather(get_all_cities())
    if message.text.capitalize() in get_cities_array[0]:
        await state.update_data(city=message.text.capitalize())
        await message.answer("Теперь выбери сколько предметов будешь сдавать👨‍🏫\n(до 3-х)", reply_markup=bs_inline)
    else:
        await message.answer("Такого города нет 🤔\nПопробуй ещё раз")
        return
        
async def couner(message: types.Message, state: FSMContext):
    if message.text == "один":
        await state.update_data(count=1)
        city = await asyncio.gather(get_data(message.from_user.id))
        await state.update_data(city=city[0][1])
        await message.answer("Выбери 1-ый предмет🧱", reply_markup=get_subs_array_one())
    elif message.text == "два":
        await state.update_data(count=2)
        city = await asyncio.gather(get_data(message.from_user.id))
        await state.update_data(city=city[0][1])
        await message.answer("Выбери 1-ый предмет🧱", reply_markup=get_subs_array_one())
    elif message.text == "три":
        await state.update_data(count=3)
        city = await asyncio.gather(get_data(message.from_user.id))
        await state.update_data(city=city[0][1])
        await message.answer("Выбери 1-ый предмет🧱", reply_markup=get_subs_array_one())

# Выбор количства сдаваемых предметов
async def count_chosen(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    msg = int(callback_data.get("cc"))

    if msg == 1:
        await state.update_data(count=msg)
        await call.message.edit_text("Выбери 1-ый предмет🧱", reply_markup=get_subs_array_one())
    elif msg == 2:
        await state.update_data(count=msg)
        await call.message.edit_text("Выбери 1-ый предмет🧱", reply_markup=get_subs_array_one())
    elif msg == 3:
        await state.update_data(count=msg)
        await call.message.edit_text("Выбери 1-ый предмет🧱", reply_markup=get_subs_array_one())


async def preset_handle(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(sub1=callback_data.get("sub1"))
    cso = await state.get_data()
    if cso['count'] == 1:
        dt = convert(cso['sub1'])
        await asyncio.gather(insert_data(call.from_user.id, cso['city'], dt))
        await call.message.edit_text(f"Твои данные успешно записаны!!\nГород: {cso['city']}\nПредмет: {dt}", reply_markup=ok_mrk)
        await state.finish()
        
    elif cso['count'] == 2:
        print(2)
        await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=get_subs_array_two())
    elif cso['count'] == 3:
        print(3)
        await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=get_subs_array_two())


async def preset_two_handle(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(sub2=callback_data.get("sub2"))
    cso = await state.get_data()
    if cso['count'] == 2:
        if cso['city'] != "":
            dt = convert(cso['sub1'], cso['sub2'])
            result = await asyncio.gather(insert_data(call.from_user.id, cso['city'], dt))
            await call.message.edit_text(f"Твои данные успешно записаны!!\nГород: {cso['city']}\nПредметы: {dt}", reply_markup=ok_mrk)
            await state.finish()
        else:
            pass
    elif cso['count'] == 3:
        print(33)
        await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=get_subs_array_three())



async def preset_three_handle(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(sub3=callback_data.get("sub3"))
    cso = await state.get_data()
    if cso['city'] != "":
        dt = convert(cso['sub1'], cso['sub2'], cso['sub3'])
        result = await asyncio.gather(insert_data(call.from_user.id, cso['city'], dt))
        await call.message.edit_text(f"Твои данные успешно записаны!!\nГород: {cso['city']}\nПредметы: {dt}", reply_markup=ok_mrk)
        await state.finish()
    else:
        pass


def reg_hnfl(dp: Dispatcher):
    dp.register_message_handler(messaged, state=AnotherState.test)
    dp.register_message_handler(couner, state=AnotherState.count_subjects)
    dp.register_callback_query_handler(preset_handle, preset1.filter(), state="*")
    dp.register_callback_query_handler(preset_two_handle, preset2.filter(), state="*")
    dp.register_callback_query_handler(preset_three_handle, preset3.filter(), state="*")
    dp.register_callback_query_handler(count_chosen, bs.filter(), state="*")
