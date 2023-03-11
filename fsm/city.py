# Получение списка городов России с вузами
from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
import aiohttp
import asyncio as asy
from bs4 import BeautifulSoup
import lxml
from modules.data_base import insert_data
from keyboards.inline import subsidii
from keyboards.inline import ok_mrk

class StartState(StatesGroup):
    city = State()
    count_subjects = State()


count_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
count1 = KeyboardButton("1")
count2 = KeyboardButton("2")
count3 = KeyboardButton("3")
count_keyboard.add(count1, count2, count3)


cc_inline = InlineKeyboardMarkup(row_width=3)
cc = CallbackData("count", "cc")

cc_inline.add(
    InlineKeyboardButton(f"1", callback_data=cc.new(
        cc = "1"
    )),
    InlineKeyboardButton(f"2", callback_data=cc.new(
        cc = "2"
    )),
    InlineKeyboardButton(f"3", callback_data=cc.new(
        cc = "3"
    ))
)


group = CallbackData("set", "subject", "action")


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


async def city_write(message: types.Message, state: FSMContext):
    get_cities_array = await asy.gather(get_all_cities())
    if message.text == "/start":
        await state.finish()
        await message.answer(f"Привет <a href='t.me/{message.from_user.username}'>{message.from_user.full_name}🤗</a>", parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
        await asy.sleep(0.5)
        await message.answer("Из какого ты города?\nОтправь в чат")
        await state.set_state(StartState.city.state)
    elif message.text.capitalize() in get_cities_array[0]:
        await state.update_data(city=message.text.capitalize())
        await message.answer("Теперь выбери сколько предметов будешь сдавать👨‍🏫\n(до 3-х)", reply_markup=cc_inline)
    # if message.text.capitalize() not in get_cities_array[0]:
    else:
        await message.answer("Такого города нет 🤔\nПопробуй ещё раз")
        return


# Выбор количства сдаваемых предметов
async def count_chosen(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    msg = int(callback_data.get("cc"))

    if msg == 1 or msg == 2 or msg == 3:
        await state.update_data(count=msg)
        user_data = await state.get_data()
        if user_data['count'] == 1:
            s1_1 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="1_1"
                ))) 
            s1_1.add(*array)

            await call.message.edit_text("Выбери предмет🧱", reply_markup=s1_1)
        elif user_data['count'] == 2:
            s2_1 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_1"
                ))) 
            s2_1.add(*array)

            await call.message.edit_text("Выбери 1-ый предмет🧱", reply_markup=s2_1)
        elif user_data['count'] == 3:
            s3_1 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_1"
                ))) 
            s3_1.add(*array)

            await call.message.edit_text("Выбери 1-ый предмет🧱", reply_markup=s3_1)


# Общий обработчик
async def group_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()

    # Физика
    if callback_data.get('subject') == 'phys':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Физика")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Физика")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет!", reply_markup=s2_2)
        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Физика":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Физика")
                await asy.gather(send_data_second(message=call.message, state=state))
        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Физика")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет!", reply_markup=s3_2)
        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Физика":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Физика")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)
        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Физика" or ssr["s2"] == "Физика":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Физика")
                await asy.gather(send_data_third(message=call.message, state=state))


    # Обществознание
    elif callback_data.get('subject') == 'social':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Обществознание")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Обществознание")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Обществознание":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Обществознание")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Обществознание")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Обществознание":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Обществознание")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Обществознание" or ssr["s2"] == "Обществознание":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Обществознание")
                await asy.gather(send_data_third(message=call.message, state=state))
    

    # Английский
    elif callback_data.get('subject') == 'eng':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Английский")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Английский")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Английский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Английский")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Английский")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Английский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Английский")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Английский" or ssr["s2"] == "Английский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Английский")
                await asy.gather(send_data_third(message=call.message, state=state))
        

    # Информатика
    elif callback_data.get('subject') == 'inf':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Информатика")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Информатика")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Информатика":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Информатика")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Информатика")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Информатика":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Информатика")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Информатика" or ssr["s2"] == "Информатика":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Информатика")
                await asy.gather(send_data_third(message=call.message, state=state))


    # Биология
    elif callback_data.get('subject') == 'bio':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Биология")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Биология")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Биология":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Биология")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Биология")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Биология":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Биология")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Биология" or ssr["s2"] == "Биология":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Биология")
                await asy.gather(send_data_third(message=call.message, state=state))


    # История
    elif callback_data.get('subject') == 'history':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="История")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="История")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "История":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="История")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="История")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "История":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="История")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "История" or ssr["s2"] == "История":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="История")
                await asy.gather(send_data_third(message=call.message, state=state))

    
    # Информатика
    elif callback_data.get('subject') == 'ximi':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Химия")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Химия")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Химия":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Химия")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Химия")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Химия":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Химия")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Химия" or ssr["s2"] == "Химия":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Химия")
                await asy.gather(send_data_third(message=call.message, state=state))
    

    # География
    elif callback_data.get('subject') == 'geo':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="География")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="География")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "География":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="География")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="География")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "География":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="География")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "География" or ssr["s2"] == "География":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="География")
                await asy.gather(send_data_third(message=call.message, state=state))

    
    # Немецкий
    elif callback_data.get('subject') == 'nec':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Немецкий")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Немецкий")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Немецкий":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Немецкий")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Немецкий")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Немецкий":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Немецкий")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Немецкий" or ssr["s2"] == "Немецкий":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Немецкий")
                await asy.gather(send_data_third(message=call.message, state=state))
    

    # Французский
    elif callback_data.get('subject') == 'franch':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Французский")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Французский")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Французский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Французский")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Французский")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Французский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Французский")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Французский" or ssr["s2"] == "Французский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Французский")
                await asy.gather(send_data_third(message=call.message, state=state))

    
    # Литература
    elif callback_data.get('subject') == 'litr':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Литература")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Литература")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Литература":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Литература")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Литература")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Литература":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Литература")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Литература" or ssr["s2"] == "Литература":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Литература")
                await asy.gather(send_data_third(message=call.message, state=state))

    
    # Испанский
    elif callback_data.get('subject') == 'spain':
        if callback_data.get('action') == '1_1':
            await state.update_data(s1="Испанский")
            await asy.gather(send_data_first(message=call.message, state=state))
        elif callback_data.get('action') == '2_1':
            await state.update_data(s1="Испанский")
            s2_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="2_2"
                ))) 
            s2_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s2_2)

        elif callback_data.get('action') == '2_2':
            ssr = await state.get_data()
            if ssr['s1'] == "Испанский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Испанский")
                await asy.gather(send_data_second(message=call.message, state=state))

        elif callback_data.get('action') == '3_1':
            await state.update_data(s1="Испанский")
            s3_2 = InlineKeyboardMarkup(row_width=3)
            array = []
            for sus in subsidii:
                array.append(
                    InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                    subject = f"{sus['strc']}",
                    action="3_2"
                ))) 
            s3_2.add(*array)
            await call.message.edit_text("Выберете 2-ой предмет 2️⃣", reply_markup=s3_2)

        elif callback_data.get('action') == '3_2':
            ssr = await state.get_data()
            if ssr["s1"] == "Испанский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s2="Испанский")
                s3_3 = InlineKeyboardMarkup(row_width=3)
                array = []
                for sus in subsidii:
                    array.append(
                        InlineKeyboardButton(f"{sus['subject']}", callback_data=group.new(
                        subject = f"{sus['strc']}",
                        action="3_3"
                    ))) 
                s3_3.add(*array)
                await call.message.edit_text("Выберете 3-ий предмет 3️⃣🤍", reply_markup=s3_3)

        elif callback_data.get('action') == '3_3':
            ssr = await state.get_data()
            if ssr["s1"] == "Испанский" or ssr["s2"] == "Испанский":
                await call.message.answer("Вы уже выбрали этот предмет!")
            else:
                await state.update_data(s3="Испанский")
                await asy.gather(send_data_third(message=call.message, state=state))

# Send first handler data
async def send_data_first(message: types.Message, state: FSMContext):
    dt = await state.get_data()
    mrk = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(f"Да", callback_data=sub_one.new(
            action='1'
        )),
        InlineKeyboardButton(f'Нет', callback_data=sub_one.new(
            action='2'
        )))
    await message.edit_text(f"Данные верны?\nГород: {dt['city']}\nПредмет: {dt['s1']}", reply_markup=mrk)


# Send second handler data
async def send_data_second(message: types.Message, state: FSMContext):
    dt = await state.get_data()
    mrk = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(f"Да", callback_data=sub_one.new(
            action='1'
        )),
        InlineKeyboardButton(f'Нет', callback_data=sub_one.new(
            action='2'
        )))
    await message.edit_text(f"Данные верны?\nГород: {dt['city']}\nПредмет: {dt['s1']}, {dt['s2']}", reply_markup=mrk)


# Send third handler data
async def send_data_third(message: types.Message, state: FSMContext):
    dt = await state.get_data()
    mrk = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(f"Да", callback_data=sub_one.new(
            action='1'
        )),
        InlineKeyboardButton(f'Нет', callback_data=sub_one.new(
            action='2'
        )))
    await message.edit_text(f"Данные верны?\nГород: {dt['city']}\nПредметы: {dt['s1']}, {dt['s2']}, {dt['s3']}", reply_markup=mrk)


# Ввод генераторов
sub_one = CallbackData("one_sub", "action")


# Обработчик первых колбеков
async def callback_checker(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    if callback_data.get('action') == '1':
        data = await state.get_data()
        await state.finish()

        if data['count'] == 1:
            dt = f"{data['s1']} "
            result_inserting = await asy.gather(insert_data(call.from_user.id, data['city'], dt))
            await call.message.edit_text(f"Твои данные успешно записаны!!\nГород: {data['city']} Предмет: {data['s1']}", reply_markup=ok_mrk)

        elif data['count'] == 2:
            dt = f"{data['s1']} {data['s2']}"
            result_inserting = await asy.gather(insert_data(call.from_user.id, data['city'], dt))
            await call.message.edit_text(f"Твои данные успешно записаны!!\nГород: {data['city']}\nПредметы: {data['s1']}, {data['s2']}", reply_markup=ok_mrk)

        elif data['count'] == 3:
            dt = f"{data['s1']} {data['s2']} {data['s3']}"
            result_inserting = await asy.gather(insert_data(call.from_user.id, data['city'], dt))
            await call.message.edit_text(f"Твои данные успешно записаны!!\nГород: {data['city']}\nПредметы: {data['s1']}, {data['s2']}, {data['s3']}", reply_markup=ok_mrk)

    elif callback_data.get('action') == '2':
        await call.message.edit_text("Введите ваш город")
        await state.set_state(StartState.city.state)
    

def reg_handlers_start(dp: Dispatcher):
    dp.register_message_handler(city_write, state=StartState.city)
    dp.register_callback_query_handler(count_chosen, cc.filter(), state="*")
    dp.register_callback_query_handler(callback_checker, sub_one.filter(), state=StartState.city.state)
    dp.register_callback_query_handler(group_callback, group.filter(), state="*")