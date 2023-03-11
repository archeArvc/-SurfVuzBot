from aiogram import types, Dispatcher
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from fsm.city import cc_inline
import json
from keyboards.reply import *
from keyboards.inline import ok_data, profiles_data
from modules.data_base import check_data, get_data
import asyncio as asy
from fsm.sql_handler import callabel_dop, stater
from trash.parser import vuzoteka
from pathlib import Path
from modules.TelegramUtils.topest import get_vuzes, top_your_city


async def calls(call: types.CallbackQuery, callback_data: dict):
    msg = callback_data.get("type")
    if msg == "ok":
        photo = InputFile(f"{Path.cwd()}\\photos\\hello.png")
        await call.message.delete()
        await call.message.answer_photo(photo=photo, caption="Добро пожаловать!", reply_markup=main)
    elif msg == "back_to_main":
        pass


async def text_s(message: types.Message, state: FSMContext):
    hnh = await asy.gather(check_data(message.from_user.id))
    if hnh[0] == 'also_have':
        if message.text == "Фильтры":
            photo = InputFile(f"{Path.cwd()}\\photos\\filters.png")
            result = await asy.gather(get_data(message.from_user.id))
            if result[0][3] == 1:
                dops = "Да"
            elif result[0][3] == 2:
                dops = "Нет"

            if result[0][4] == 2:
                math_profile = "База"
            elif result[0][4] == 1:
                math_profile = "Профильная"
            splited_subs = result[0][2].split(" ")
            await message.answer_photo(
                photo=photo,
                caption=f"Ваши фильтры:\n\n*Город:* {result[0][1]}\n*Предметы:* {', '.join(splited_subs)}\n*Входные экзамены:* {dops}\n*Математика:* {math_profile}",
                reply_markup=filters_mrk,
                parse_mode=types.ParseMode.MARKDOWN_V2
                )
        elif message.text == "Назад":
            photo = InputFile(f"{Path.cwd()}\\photos\\hello.png")
            await message.answer_photo(photo=photo, caption="Добро пожаловать!", reply_markup=main)
        elif message.text == "Топы вузов🆒":
            photo = InputFile(f"{Path.cwd()}\\photos\\top.png")
            await message.answer_photo(photo=photo, caption="Топы", reply_markup=toper)
        elif message.text == "Поиск🔬":
            photo = InputFile(f"{Path.cwd()}\\photos\\search.png")
            await message.answer_photo(photo=photo, caption="Поиск", reply_markup=searcing_bottom)
        elif message.text == "Поиск по фильтрам":
            await message.answer("*Ждите*", parse_mode=types.ParseMode.MARKDOWN_V2)
            get_dates = await asy.gather(get_data(message.from_user.id))
            print(get_dates, "sss")
            city = get_dates[0][1]
            subs = get_dates[0][2]
            print(city, subs.lower())
            result = await asy.gather(vuzoteka(city, subs.lower()))
            for res in result[0]:
                # photo = InputFile(f"https:{res['logo']}")
                await message.answer_photo(
                    photo=f"https:{res['logo']}",
                    caption=f"{res['title']}\n\n<b>Общежитие:</b> {res['social']}\n<b>Год основания:</b> {res['date']}\n<b>Студентов:</b> {res['students']}\n<b>Сред. балл ЕГЭ:</b> {res['ege']}\n<b>Рэйтинг вуза:</b> {res['rate']}\n<b>Ссылка на вуз:</b> {res['link']}",
                    parse_mode=types.ParseMode.HTML
                    )
        elif message.text == "Входные экз.":
            await message.answer("Искать с вузы/специальности с входными экзмаенами или без?", reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton("Да", callback_data=callabel_dop.new(
                    active = "1"
                )),
                InlineKeyboardButton("Нет", callback_data=callabel_dop.new(
                    active = "2"
                ))
            ))
        elif message.text == "Город":
            await message.answer("Введите ваш город: ")
            await state.set_state(state=stater.write_city.state)
        elif message.text == "Профиль":
            await message.answer("Какую математику вы будете сдавать?",
                                 reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                    InlineKeyboardButton("Профильную", callback_data=profiles_data.new(act = 1)),
                                    InlineKeyboardButton("Базу", callback_data=profiles_data.new(act = 2))
                                 ))
        elif message.text == "Специальность":
            await message.answer("<b>Временно недоступно</b>")
        elif message.text == "Предметы":
            pass
        elif message.text == "Топ 10 вузов России":
            res = await asy.gather(get_vuzes())
            await message.answer(res[0], disable_web_page_preview=True)
        elif message.text == "Топ вузов вашего города":
            res = await asy.gather(get_data(message.from_user.id))
            city = res[0][1]
            result = await asy.gather(top_your_city(city))
            await message.answer(result[0])
    else:
        await message.answer("Вы не зарегестрировались!\nВведите /start")



def register_all(dp: Dispatcher):
    dp.register_message_handler(text_s, content_types=types.ContentType.TEXT)
    dp.register_callback_query_handler(calls, ok_data.filter(), state='*')
